"""Tests for report generation and export."""

import json

import pytest
from click.testing import CliRunner

from benchmark.cli import main
from benchmark.models import CategoryScores, RunResults, TaskResult
from benchmark.report import generate_json_report, generate_markdown_report
from benchmark.results import save_results


@pytest.fixture
def runner():
    return CliRunner()


def _make_run(run_id: str, model: str, se: float = 80.0, plan: float = 60.0,
              prod: float = 70.0, start: float = 50.0, dry_run: bool = False,
              tasks: list[TaskResult] | None = None) -> RunResults:
    """Helper to create a RunResults instance."""
    cs = CategoryScores(
        software_engineering=se,
        planning=plan,
        product_mind=prod,
        startup_mind=start,
    )
    overall = se * 0.40 + plan * 0.25 + prod * 0.20 + start * 0.15
    if tasks is None:
        tasks = [
            TaskResult(task_id="SE-001", category="software-engineering", score=se),
            TaskResult(task_id="PLAN-001", category="planning", score=plan),
            TaskResult(task_id="PROD-001", category="product-mind", score=prod),
            TaskResult(task_id="START-001", category="startup-mind", score=start),
        ]
    return RunResults(
        run_id=run_id,
        model_name=model,
        timestamp="2026-04-12T12:00:00",
        overall_score=round(overall, 1),
        category_scores=cs,
        per_task_results=tasks,
        dry_run=dry_run,
    )


@pytest.fixture
def sample_results(tmp_path):
    """Create sample results files in tmp_path."""
    r1 = _make_run("run_001", "gpt-4o", se=85.0, plan=70.0, prod=75.0, start=60.0)
    r2 = _make_run("run_002", "claude-sonnet-4", se=90.0, plan=65.0, prod=80.0, start=55.0)
    r3 = _make_run("run_003", "gemini/gemini-2.5-pro", se=70.0, plan=80.0, prod=60.0, start=70.0)
    for r in [r1, r2, r3]:
        save_results(r, tmp_path)
    return tmp_path


# --- Unit tests for report module ---

class TestMarkdownReportSingleRun:
    def test_contains_all_sections(self, sample_results):
        md = generate_markdown_report(run_ids=["run_001"], results_dir=sample_results)
        assert "# LLM Benchmark Report" in md
        assert "## Executive Summary" in md
        assert "## Per-Category Analysis" in md
        assert "## Per-Model Breakdown" in md
        assert "## Recommendations" in md

    def test_model_name_in_report(self, sample_results):
        md = generate_markdown_report(run_ids=["run_001"], results_dir=sample_results)
        assert "gpt-4o" in md

    def test_scores_in_report(self, sample_results):
        md = generate_markdown_report(run_ids=["run_001"], results_dir=sample_results)
        assert "85.0" in md  # SE score

    def test_dry_run_note(self, tmp_path):
        r = _make_run("run_dry", "gpt-4o", dry_run=True)
        save_results(r, tmp_path)
        md = generate_markdown_report(run_ids=["run_dry"], results_dir=tmp_path)
        assert "dry-run" in md.lower()

    def test_empty_results(self, tmp_path):
        md = generate_markdown_report(results_dir=tmp_path)
        assert "No benchmark results found" in md


class TestMarkdownReportMultiRun:
    def test_all_models_in_executive_summary(self, sample_results):
        md = generate_markdown_report(results_dir=sample_results)
        assert "gpt-4o" in md
        assert "claude-sonnet-4" in md
        assert "gemini/gemini-2.5-pro" in md

    def test_ranking_order(self, sample_results):
        md = generate_markdown_report(results_dir=sample_results)
        # claude-sonnet-4 has highest overall score
        lines = md.split("\n")
        rank_lines = [line for line in lines if line.startswith("| 1 |")]
        assert "claude-sonnet-4" in rank_lines[0]

    def test_per_category_best_worst(self, sample_results):
        md = generate_markdown_report(results_dir=sample_results)
        # SE: claude-sonnet-4 best (90.0), gemini worst (70.0)
        assert "Best Model" in md
        assert "Worst Model" in md

    def test_score_distribution(self, sample_results):
        md = generate_markdown_report(results_dir=sample_results)
        assert "Score Distribution" in md

    def test_per_model_top_bottom_tasks(self, sample_results):
        md = generate_markdown_report(results_dir=sample_results)
        assert "Top 3 Tasks" in md
        assert "Bottom 3 Tasks" in md

    def test_recommendations_with_multiple_runs(self, sample_results):
        md = generate_markdown_report(results_dir=sample_results)
        assert "Best overall model" in md


class TestMarkdownReportSingleRunRecommendations:
    def test_identifies_weakest_category(self, tmp_path):
        r = _make_run("run_single", "gpt-4o", se=90.0, plan=40.0, prod=80.0, start=70.0)
        save_results(r, tmp_path)
        md = generate_markdown_report(run_ids=["run_single"], results_dir=tmp_path)
        assert "Planning" in md  # Should identify planning as weakest


class TestJsonReport:
    def test_valid_json(self, sample_results):
        content = generate_json_report(results_dir=sample_results)
        data = json.loads(content)
        assert isinstance(data, list)
        assert len(data) == 3

    def test_json_contains_run_data(self, sample_results):
        content = generate_json_report(run_ids=["run_001"], results_dir=sample_results)
        data = json.loads(content)
        assert len(data) == 1
        assert data[0]["model_name"] == "gpt-4o"
        assert data[0]["run_id"] == "run_001"

    def test_json_empty_results(self, tmp_path):
        content = generate_json_report(results_dir=tmp_path)
        data = json.loads(content)
        assert data == []


# --- CLI integration tests ---

class TestReportExportCLI:
    def test_help(self, runner):
        result = runner.invoke(main, ["report", "export", "--help"])
        assert result.exit_code == 0
        assert "--run-id" in result.output
        assert "--format" in result.output
        assert "--output" in result.output

    def test_report_group_help(self, runner):
        result = runner.invoke(main, ["report", "--help"])
        assert result.exit_code == 0
        assert "export" in result.output

    def test_report_no_subcommand_shows_help(self, runner):
        result = runner.invoke(main, ["report"])
        assert result.exit_code == 0
        assert "export" in result.output

    def test_export_markdown_single_run(self, runner, sample_results, tmp_path, monkeypatch):
        monkeypatch.setattr("benchmark.results.DEFAULT_RESULTS_DIR", sample_results)
        out_file = tmp_path / "test_report.md"
        result = runner.invoke(
            main,
            ["report", "export", "--run-id", "run_001", "--format", "markdown",
             "--output", str(out_file)],
        )
        assert result.exit_code == 0
        assert out_file.exists()
        content = out_file.read_text()
        assert "# LLM Benchmark Report" in content
        assert "gpt-4o" in content

    def test_export_json_single_run(self, runner, sample_results, tmp_path, monkeypatch):
        monkeypatch.setattr("benchmark.results.DEFAULT_RESULTS_DIR", sample_results)
        out_file = tmp_path / "test_report.json"
        result = runner.invoke(
            main,
            ["report", "export", "--run-id", "run_001", "--format", "json",
             "--output", str(out_file)],
        )
        assert result.exit_code == 0
        assert out_file.exists()
        data = json.loads(out_file.read_text())
        assert isinstance(data, list)

    def test_export_multiple_run_ids(self, runner, sample_results, tmp_path, monkeypatch):
        monkeypatch.setattr("benchmark.results.DEFAULT_RESULTS_DIR", sample_results)
        out_file = tmp_path / "multi_report.md"
        result = runner.invoke(
            main,
            ["report", "export", "--run-id", "run_001", "--run-id", "run_002",
             "--format", "markdown", "--output", str(out_file)],
        )
        assert result.exit_code == 0
        content = out_file.read_text()
        assert "gpt-4o" in content
        assert "claude-sonnet-4" in content

    def test_export_nonexistent_run(self, runner):
        result = runner.invoke(
            main,
            ["report", "export", "--run-id", "nonexistent_run", "--format", "markdown"],
        )
        assert result.exit_code != 0

    def test_export_all_runs(self, runner, sample_results, tmp_path, monkeypatch):
        monkeypatch.setattr("benchmark.results.DEFAULT_RESULTS_DIR", sample_results)
        out_file = tmp_path / "all_report.md"
        result = runner.invoke(
            main,
            ["report", "export", "--format", "markdown", "--output", str(out_file)],
        )
        assert result.exit_code == 0
        content = out_file.read_text()
        assert "gpt-4o" in content
        assert "claude-sonnet-4" in content
        assert "gemini/gemini-2.5-pro" in content


class TestReportExportWithErrors:
    def test_failed_tasks_in_breakdown(self, tmp_path):
        tasks = [
            TaskResult(task_id="SE-001", category="software-engineering", score=80.0),
            TaskResult(task_id="SE-002", category="software-engineering", score=30.0,
                       error="timeout"),
            TaskResult(task_id="PLAN-001", category="planning", score=60.0),
        ]
        r = _make_run("run_err", "test-model", tasks=tasks)
        save_results(r, tmp_path)
        md = generate_markdown_report(run_ids=["run_err"], results_dir=tmp_path)
        assert "Failed Tasks" in md
        assert "SE-002" in md
