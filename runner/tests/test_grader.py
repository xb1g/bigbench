"""Tests for grading engine."""

from benchmark.grader import _grade_reference, _text_similarity, grade_task
from benchmark.models import (
    GradingCriterion,
    ReferenceAnswer,
    Rubric,
    TaskDefinition,
)


def _make_rubric_task() -> TaskDefinition:
    """Create a test task with rubric grading."""
    return TaskDefinition(
        id="TEST-001",
        category="software-engineering",
        title="Test task",
        description="A test task for grading",
        difficulty="medium",
        estimated_minutes=10,
        language="Python",
        project_ref="test",
        prompt="Write a function to reverse a string",
        input_format="None",
        output_format="Python code",
        grading_type="rubric",
        rubric=Rubric(
            criteria=[
                GradingCriterion(name="Correctness", weight=0.4, description="Code correctly reverses string", max_score=10),
                GradingCriterion(name="Efficiency", weight=0.3, description="Uses efficient approach", max_score=10),
                GradingCriterion(name="Code Quality", weight=0.3, description="Clean, readable code", max_score=10),
            ],
            passing_threshold=60,
        ),
    )


def _make_reference_task() -> TaskDefinition:
    """Create a test task with reference answer grading."""
    return TaskDefinition(
        id="TEST-002",
        category="software-engineering",
        title="Test reference task",
        description="A test task with reference answer",
        difficulty="easy",
        estimated_minutes=5,
        language="Python",
        project_ref="test",
        prompt="What is 2+2?",
        input_format="None",
        output_format="Number",
        grading_type="reference_answer",
        reference_answer=ReferenceAnswer(
            method="exact_match",
            answer="4",
            key_elements=["4"],
        ),
    )


class TestGradeEmptyOutput:
    def test_empty_output_returns_zero(self):
        task = _make_rubric_task()
        result = grade_task(task, "")
        assert result.total_score == 0.0

    def test_whitespace_only_returns_zero(self):
        task = _make_rubric_task()
        result = grade_task(task, "   \n\n  ")
        assert result.total_score == 0.0


class TestRubricGrading:
    def test_dry_run_grading(self):
        task = _make_rubric_task()
        result = grade_task(task, "def reverse(s): return s[::-1]", dry_run=True)
        assert result.grading_method == "rubric"
        assert result.total_score > 0
        assert len(result.criterion_scores) == 3

    def test_dry_run_criterion_scores_bounded(self):
        task = _make_rubric_task()
        result = grade_task(task, "Some reasonable output here", dry_run=True)
        for cs in result.criterion_scores:
            assert 0 <= cs.score <= cs.max_score

    def test_dry_run_weighted_score(self):
        task = _make_rubric_task()
        result = grade_task(task, "A longer response that discusses the solution in detail with code examples", dry_run=True)
        # Check that weighted score matches
        expected_total = sum(cs.score / cs.max_score * cs.weight for cs in result.criterion_scores) * 100
        assert abs(result.total_score - round(min(expected_total, 100.0), 1)) < 0.2


class TestReferenceGrading:
    def test_exact_match(self):
        ref = ReferenceAnswer(method="exact_match", answer="4", key_elements=["4"])
        result = _grade_reference(ref, "4")
        assert result.total_score == 100.0
        assert result.reference_match_type == "exact"

    def test_no_match(self):
        ref = ReferenceAnswer(method="exact_match", answer="4", key_elements=["4"])
        result = _grade_reference(ref, "The answer is five")
        assert result.reference_match_type == "none"
        assert result.total_score < 50

    def test_key_elements_match(self):
        ref = ReferenceAnswer(
            method="structural_similarity",
            answer="Full answer text",
            key_elements=["set -euo pipefail", "nullglob", "exit 1"],
        )
        output = "set -euo pipefail\nshopt -s nullglob\nexit 1"
        result = _grade_reference(ref, output)
        assert result.reference_match_type == "structural"
        assert result.total_score >= 80

    def test_partial_key_elements(self):
        ref = ReferenceAnswer(
            method="structural_similarity",
            answer="Full answer",
            key_elements=["element1", "element2", "element3", "element4"],
        )
        output = "element1 and element2 are present"
        result = _grade_reference(ref, output)
        assert result.reference_match_type == "partial"


class TestTextSimilarity:
    def test_identical_texts(self):
        score = _text_similarity("hello world", "hello world")
        assert score == 100.0

    def test_completely_different(self):
        score = _text_similarity("aaa bbb", "xxx yyy")
        assert score == 0.0

    def test_partial_overlap(self):
        score = _text_similarity("hello world foo", "hello world bar")
        assert 0 < score < 100

    def test_empty_strings(self):
        score = _text_similarity("", "")
        assert score == 0.0


class TestGradingIntegration:
    def test_reference_task_grading(self):
        task = _make_reference_task()
        result = grade_task(task, "4")
        assert result.grading_method == "auto"
        assert result.total_score == 100.0

    def test_reference_task_wrong_answer(self):
        task = _make_reference_task()
        result = grade_task(task, "5")
        assert result.grading_method == "auto"
        assert result.total_score < 100
