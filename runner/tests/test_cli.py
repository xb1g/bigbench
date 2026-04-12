"""Tests for CLI commands."""


import pytest
from click.testing import CliRunner

from benchmark.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestMainHelp:
    def test_help_shows_all_commands(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "run" in result.output
        assert "results" in result.output
        assert "task" in result.output
        assert "report" in result.output

    def test_report_subcommand_help(self, runner):
        result = runner.invoke(main, ["report", "--help"])
        assert result.exit_code == 0
        assert "export" in result.output

    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestRunCommand:
    def test_run_requires_task_or_all(self, runner):
        result = runner.invoke(main, ["run", "--model", "gpt-4o"])
        assert result.exit_code != 0

    def test_run_single_task_dry_run(self, runner):
        result = runner.invoke(main, ["run", "--task", "SE-001", "--model", "gpt-4o", "--dry-run"])
        assert result.exit_code == 0
        assert "SE-001" in result.output

    def test_run_all_dry_run(self, runner):
        result = runner.invoke(main, ["run", "--all", "--model", "gpt-4o", "--dry-run"])
        assert result.exit_code == 0

    def test_run_nonexistent_task(self, runner):
        result = runner.invoke(main, ["run", "--task", "NONEXISTENT-999", "--model", "gpt-4o", "--dry-run"])
        assert result.exit_code != 0

    def test_run_with_different_models(self, runner):
        """Test multi-model support with dry-run."""
        for model in ["gpt-4o", "claude-sonnet-4", "gemini/gemini-2.5-pro"]:
            result = runner.invoke(main, ["run", "--task", "SE-001", "--model", model, "--dry-run"])
            assert result.exit_code == 0


class TestResultsCommand:
    def test_results_list_empty(self, runner, tmp_path, monkeypatch):
        monkeypatch.setattr("benchmark.results.DEFAULT_RESULTS_DIR", tmp_path)
        result = runner.invoke(main, ["results", "--list"])
        assert result.exit_code == 0

    def test_results_nonexistent_run(self, runner):
        result = runner.invoke(main, ["results", "nonexistent_run_id"])
        assert result.exit_code != 0


class TestTaskCommand:
    def test_task_default_lists_all(self, runner):
        """Invoking 'task' without subcommand defaults to listing."""
        result = runner.invoke(main, ["task"])
        assert result.exit_code == 0
        assert "42 tasks" in result.output

    def test_task_list(self, runner):
        result = runner.invoke(main, ["task", "list"])
        assert result.exit_code == 0
        assert "42 tasks" in result.output

    def test_task_create_invalid_category(self, runner):
        result = runner.invoke(main, ["task", "create", "--category", "invalid", "--id", "TEST-001"])
        assert result.exit_code != 0

    def test_task_validate_passes(self, runner):
        result = runner.invoke(main, ["task", "validate"])
        assert result.exit_code == 0
        assert "tasks passed validation" in result.output

    def test_task_validate_help(self, runner):
        result = runner.invoke(main, ["task", "validate", "--help"])
        assert result.exit_code == 0
        assert "Validate" in result.output
