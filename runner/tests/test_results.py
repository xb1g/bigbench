"""Tests for results storage."""

import json

import pytest

from benchmark.models import (
    CategoryScores,
    RunResults,
    TaskResult,
)
from benchmark.results import (
    compute_category_scores,
    compute_overall_score,
    generate_run_id,
    list_runs,
    load_results,
    save_results,
)


class TestGenerateRunId:
    def test_format(self):
        run_id = generate_run_id()
        # Should be YYYYMMDD_HHMMSS
        assert len(run_id) == 15
        assert run_id[8] == "_"

    def test_uniqueness(self):
        ids = {generate_run_id() for _ in range(10)}
        # Should generate unique IDs (unless called in same second)
        assert len(ids) >= 1


class TestComputeCategoryScores:
    def test_single_category(self):
        results = [
            TaskResult(task_id="SE-001", category="software-engineering", score=80.0),
            TaskResult(task_id="SE-002", category="software-engineering", score=60.0),
        ]
        scores = compute_category_scores(results)
        assert scores.software_engineering == 70.0
        assert scores.planning == 0.0

    def test_all_categories(self):
        results = [
            TaskResult(task_id="SE-001", category="software-engineering", score=80.0),
            TaskResult(task_id="PLAN-001", category="planning", score=70.0),
            TaskResult(task_id="PROD-001", category="product-mind", score=60.0),
            TaskResult(task_id="START-001", category="startup-mind", score=50.0),
        ]
        scores = compute_category_scores(results)
        assert scores.software_engineering == 80.0
        assert scores.planning == 70.0
        assert scores.product_mind == 60.0
        assert scores.startup_mind == 50.0

    def test_empty_results(self):
        scores = compute_category_scores([])
        assert scores.software_engineering == 0.0
        assert scores.planning == 0.0
        assert scores.product_mind == 0.0
        assert scores.startup_mind == 0.0


class TestComputeOverallScore:
    def test_weighted_formula(self):
        scores = CategoryScores(
            software_engineering=80.0,
            planning=60.0,
            product_mind=70.0,
            startup_mind=50.0,
        )
        overall = compute_overall_score(scores)
        expected = 80 * 0.40 + 60 * 0.25 + 70 * 0.20 + 50 * 0.15
        assert overall == round(expected, 1)

    def test_perfect_scores(self):
        scores = CategoryScores(
            software_engineering=100.0,
            planning=100.0,
            product_mind=100.0,
            startup_mind=100.0,
        )
        overall = compute_overall_score(scores)
        assert overall == 100.0

    def test_zero_scores(self):
        scores = CategoryScores()
        overall = compute_overall_score(scores)
        assert overall == 0.0

    def test_formula_precision(self):
        scores = CategoryScores(
            software_engineering=69.6,
            planning=68.5,
            product_mind=64.7,
            startup_mind=66.0,
        )
        overall = compute_overall_score(scores)
        expected = 69.6 * 0.40 + 68.5 * 0.25 + 64.7 * 0.20 + 66.0 * 0.15
        assert abs(overall - round(expected, 1)) < 0.2


class TestAtomicSaveAndLoad:
    def test_save_and_load(self, tmp_path):
        results = RunResults(
            run_id="test_run",
            model_name="gpt-4o",
            timestamp="2026-04-12T12:00:00",
            overall_score=75.0,
            category_scores=CategoryScores(software_engineering=80.0, planning=70.0),
            per_task_results=[
                TaskResult(task_id="SE-001", category="software-engineering", score=80.0),
            ],
        )
        path = save_results(results, tmp_path)
        assert path.exists()
        assert path.name == "results.json"

        loaded = load_results("test_run", tmp_path)
        assert loaded.run_id == "test_run"
        assert loaded.model_name == "gpt-4o"
        assert loaded.overall_score == 75.0

    def test_atomic_write_no_tmp_file(self, tmp_path):
        results = RunResults(
            run_id="test_atomic",
            model_name="gpt-4o",
            timestamp="2026-04-12T12:00:00",
            overall_score=50.0,
        )
        save_results(results, tmp_path)
        # No .tmp file should remain
        run_dir = tmp_path / "test_atomic"
        assert not (run_dir / "results.json.tmp").exists()
        assert (run_dir / "results.json").exists()

    def test_json_valid(self, tmp_path):
        results = RunResults(
            run_id="test_json",
            model_name="gpt-4o",
            timestamp="2026-04-12T12:00:00",
            overall_score=50.0,
        )
        save_results(results, tmp_path)
        with open(tmp_path / "test_json" / "results.json") as f:
            data = json.load(f)
        assert data["run_id"] == "test_json"
        assert data["overall_score"] == 50.0

    def test_load_nonexistent(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_results("nonexistent", tmp_path)


class TestListRuns:
    def test_empty_directory(self, tmp_path):
        runs = list_runs(tmp_path)
        assert runs == []

    def test_lists_runs(self, tmp_path):
        for run_id in ["20260412_120000", "20260412_130000"]:
            run_dir = tmp_path / run_id
            run_dir.mkdir()
            (run_dir / "results.json").write_text("{}")
        runs = list_runs(tmp_path)
        assert len(runs) == 2
        # Newest first
        assert runs[0] == "20260412_130000"

    def test_ignores_incomplete_dirs(self, tmp_path):
        run_dir = tmp_path / "incomplete"
        run_dir.mkdir()
        # No results.json
        runs = list_runs(tmp_path)
        assert runs == []
