"""Tests for Pydantic models."""

from benchmark.models import (
    CATEGORY_MAP,
    CATEGORY_WEIGHTS,
    CategoryScores,
    GradingCriterion,
    Rubric,
    RunResults,
    TaskResult,
)


class TestCategoryScores:
    def test_default_scores(self):
        cs = CategoryScores()
        assert cs.software_engineering == 0.0
        assert cs.planning == 0.0
        assert cs.product_mind == 0.0
        assert cs.startup_mind == 0.0

    def test_custom_scores(self):
        cs = CategoryScores(software_engineering=85.5, planning=72.3, product_mind=65.0, startup_mind=50.0)
        assert cs.software_engineering == 85.5
        assert cs.planning == 72.3

    def test_scores_bounded(self):
        # Scores should be 0-100
        cs = CategoryScores(software_engineering=100.0)
        assert cs.software_engineering == 100.0


class TestCategoryMap:
    def test_all_categories_mapped(self):
        assert "software-engineering" in CATEGORY_MAP
        assert "planning" in CATEGORY_MAP
        assert "product-mind" in CATEGORY_MAP
        assert "startup-mind" in CATEGORY_MAP

    def test_mapping_values(self):
        assert CATEGORY_MAP["software-engineering"] == "software_engineering"
        assert CATEGORY_MAP["planning"] == "planning"
        assert CATEGORY_MAP["product-mind"] == "product_mind"
        assert CATEGORY_MAP["startup-mind"] == "startup_mind"


class TestCategoryWeights:
    def test_weights_sum_to_one(self):
        total = sum(CATEGORY_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_weight_values(self):
        assert CATEGORY_WEIGHTS["software_engineering"] == 0.40
        assert CATEGORY_WEIGHTS["planning"] == 0.25
        assert CATEGORY_WEIGHTS["product_mind"] == 0.20
        assert CATEGORY_WEIGHTS["startup_mind"] == 0.15


class TestRubric:
    def test_rubric_creation(self):
        criteria = [
            GradingCriterion(name="Test", weight=0.5, description="A test criterion", max_score=10),
            GradingCriterion(name="Test2", weight=0.5, description="Another test criterion", max_score=10),
        ]
        rubric = Rubric(criteria=criteria, passing_threshold=60)
        assert len(rubric.criteria) == 2
        assert rubric.passing_threshold == 60


class TestTaskResult:
    def test_task_result_creation(self):
        tr = TaskResult(task_id="SE-001", category="software-engineering", score=85.5, raw_output="test")
        assert tr.task_id == "SE-001"
        assert tr.score == 85.5
        assert tr.error is None
        assert tr.dry_run is False

    def test_task_result_with_error(self):
        tr = TaskResult(task_id="SE-001", category="software-engineering", score=0.0, error="API failed")
        assert tr.error == "API failed"

    def test_task_result_dry_run(self):
        tr = TaskResult(task_id="SE-001", category="software-engineering", score=50.0, dry_run=True)
        assert tr.dry_run is True


class TestRunResults:
    def test_run_results_creation(self):
        rr = RunResults(
            run_id="20260412_120000",
            model_name="gpt-4o",
            timestamp="2026-04-12T12:00:00",
            overall_score=75.0,
        )
        assert rr.run_id == "20260412_120000"
        assert rr.model_name == "gpt-4o"
        assert rr.overall_score == 75.0
        assert rr.per_task_results == []
        assert rr.dry_run is False

    def test_run_results_serialization(self):
        rr = RunResults(
            run_id="20260412_120000",
            model_name="gpt-4o",
            timestamp="2026-04-12T12:00:00",
            overall_score=75.0,
            category_scores=CategoryScores(software_engineering=80.0, planning=70.0),
            per_task_results=[
                TaskResult(task_id="SE-001", category="software-engineering", score=80.0),
            ],
        )
        json_str = rr.model_dump_json()
        assert "20260412_120000" in json_str
        assert "gpt-4o" in json_str
        assert "75.0" in json_str
