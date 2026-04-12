"""Tests for task loader."""

from pathlib import Path

import pytest
import yaml

from benchmark.loader import (
    get_tasks_by_category,
    load_all_tasks,
    load_task_by_id,
    validate_all_tasks,
    TaskValidationResult,
)

# Path: runner/tests/test_loader.py -> project root is 2 levels up from runner/
# runner/tests/ -> runner/ -> llm-benchmark/
TASKS_DIR = Path(__file__).resolve().parents[2] / "tasks"


class TestLoadAllTasks:
    def test_loads_all_42_tasks(self):
        tasks = load_all_tasks(TASKS_DIR)
        assert len(tasks) == 42

    def test_tasks_sorted_by_category_and_id(self):
        tasks = load_all_tasks(TASKS_DIR)
        ids = [t.id for t in tasks]
        # Should be sorted by category then id
        assert ids == sorted(ids, key=lambda x: (x[:x.index("-")], x))

    def test_all_tasks_have_required_fields(self):
        tasks = load_all_tasks(TASKS_DIR)
        for task in tasks:
            assert task.id, "Missing id"
            assert task.category, f"Missing category in {task.id}"
            assert task.title, f"Missing title in {task.id}"
            assert task.description, f"Missing description in {task.id}"
            assert task.difficulty in ("easy", "medium", "hard"), f"Invalid difficulty in {task.id}"
            assert task.estimated_minutes > 0, f"Invalid estimated_minutes in {task.id}"
            assert task.language, f"Missing language in {task.id}"
            assert task.project_ref, f"Missing project_ref in {task.id}"
            assert task.prompt, f"Missing prompt in {task.id}"

    def test_category_distribution(self):
        tasks = load_all_tasks(TASKS_DIR)
        categories = {}
        for t in tasks:
            categories[t.category] = categories.get(t.category, 0) + 1
        assert categories.get("software-engineering", 0) == 12
        assert categories.get("planning", 0) == 10
        assert categories.get("product-mind", 0) == 10
        assert categories.get("startup-mind", 0) == 10

    def test_all_tasks_have_grading(self):
        tasks = load_all_tasks(TASKS_DIR)
        for task in tasks:
            assert task.grading_type in ("rubric", "reference_answer"), f"Invalid grading type in {task.id}"
            if task.grading_type == "rubric":
                assert task.rubric is not None, f"Missing rubric in {task.id}"
                assert len(task.rubric.criteria) > 0, f"No criteria in rubric for {task.id}"
                # Check weights sum to approximately 1.0
                total_weight = sum(c.weight for c in task.rubric.criteria)
                assert abs(total_weight - 1.0) < 0.01, f"Weights don't sum to 1.0 in {task.id}: {total_weight}"
            elif task.grading_type == "reference_answer":
                assert task.reference_answer is not None, f"Missing reference_answer in {task.id}"
                assert task.reference_answer.answer, f"Empty answer in reference_answer for {task.id}"


class TestLoadTaskById:
    def test_load_existing_task(self):
        task = load_task_by_id("SE-001", TASKS_DIR)
        assert task.id == "SE-001"
        assert task.category == "software-engineering"

    def test_load_nonexistent_task(self):
        with pytest.raises(ValueError, match="Task not found"):
            load_task_by_id("NONEXISTENT-999", TASKS_DIR)


class TestGetTasksByCategory:
    def test_groups_tasks(self):
        tasks = load_all_tasks(TASKS_DIR)
        grouped = get_tasks_by_category(tasks)
        assert "software-engineering" in grouped
        assert len(grouped["software-engineering"]) == 12
        assert len(grouped["planning"]) == 10
        assert len(grouped["product-mind"]) == 10
        assert len(grouped["startup-mind"]) == 10


class TestValidateAllTasks:
    def test_all_42_tasks_pass(self):
        results = validate_all_tasks(TASKS_DIR)
        assert len(results) == 42
        failed = [r for r in results if not r.passed]
        if failed:
            msgs = [f"{r.task_id}: {r.errors}" for r in failed]
            pytest.fail(f"Validation failures: {msgs}")
        assert all(r.passed for r in results)

    def test_missing_required_field(self, tmp_path):
        # Create a task YAML missing 'title'
        task_yaml = {
            "id": "SE-BAD",
            "category": "software-engineering",
            "description": "test",
            "difficulty": "easy",
            "estimated_minutes": 10,
            "language": "Python",
            "project_ref": "someproject",
            "prompt": "Do something",
            "output_format": "text",
            "grading": {"rubric": {"criteria": [{"name": "A", "weight": 1.0, "description": "test", "max_score": 10}]}},
        }
        cat_dir = tmp_path / "software-engineering"
        cat_dir.mkdir()
        (cat_dir / "SE-BAD.yaml").write_text(yaml.dump(task_yaml, default_flow_style=False))
        results = validate_all_tasks(tmp_path)
        assert len(results) == 1
        assert not results[0].passed
        assert any("title" in e for e in results[0].errors)

    def test_invalid_category(self, tmp_path):
        task_yaml = {
            "id": "SE-BAD",
            "category": "invalid-category",
            "title": "Bad category",
            "description": "test task",
            "difficulty": "easy",
            "estimated_minutes": 10,
            "language": "Python",
            "project_ref": "someproject",
            "prompt": "Do something",
            "output_format": "text",
            "grading": {"rubric": {"criteria": [{"name": "A", "weight": 1.0, "description": "test", "max_score": 10}]}},
        }
        cat_dir = tmp_path / "invalid-category"
        cat_dir.mkdir()
        (cat_dir / "SE-BAD.yaml").write_text(yaml.dump(task_yaml, default_flow_style=False))
        results = validate_all_tasks(tmp_path)
        assert len(results) == 1
        assert not results[0].passed
        assert any("Invalid category" in e for e in results[0].errors)

    def test_invalid_difficulty(self, tmp_path):
        task_yaml = {
            "id": "SE-BAD",
            "category": "software-engineering",
            "title": "Bad difficulty",
            "description": "test task",
            "difficulty": "extreme",
            "estimated_minutes": 10,
            "language": "Python",
            "project_ref": "someproject",
            "prompt": "Do something",
            "output_format": "text",
            "grading": {"rubric": {"criteria": [{"name": "A", "weight": 1.0, "description": "test", "max_score": 10}]}},
        }
        cat_dir = tmp_path / "software-engineering"
        cat_dir.mkdir()
        (cat_dir / "SE-BAD.yaml").write_text(yaml.dump(task_yaml, default_flow_style=False))
        results = validate_all_tasks(tmp_path)
        assert len(results) == 1
        assert not results[0].passed
        assert any("Invalid difficulty" in e for e in results[0].errors)

    def test_rubric_weights_not_summing_to_one(self, tmp_path):
        task_yaml = {
            "id": "SE-BAD",
            "category": "software-engineering",
            "title": "Bad weights",
            "description": "test task",
            "difficulty": "easy",
            "estimated_minutes": 10,
            "language": "Python",
            "project_ref": "someproject",
            "prompt": "Do something",
            "output_format": "text",
            "grading": {"rubric": {"criteria": [
                {"name": "A", "weight": 0.5, "description": "test", "max_score": 10},
                {"name": "B", "weight": 0.3, "description": "test", "max_score": 10},
            ]}},
        }
        cat_dir = tmp_path / "software-engineering"
        cat_dir.mkdir()
        (cat_dir / "SE-BAD.yaml").write_text(yaml.dump(task_yaml, default_flow_style=False))
        results = validate_all_tasks(tmp_path)
        assert len(results) == 1
        assert not results[0].passed
        assert any("weights sum" in e for e in results[0].errors)

    def test_empty_task_file(self, tmp_path):
        cat_dir = tmp_path / "software-engineering"
        cat_dir.mkdir()
        (cat_dir / "EMPTY.yaml").write_text("")
        results = validate_all_tasks(tmp_path)
        assert len(results) == 1
        assert not results[0].passed
        assert any("Empty" in e for e in results[0].errors)

    def test_grading_missing_both_types(self, tmp_path):
        task_yaml = {
            "id": "SE-BAD",
            "category": "software-engineering",
            "title": "No grading type",
            "description": "test task",
            "difficulty": "easy",
            "estimated_minutes": 10,
            "language": "Python",
            "project_ref": "someproject",
            "prompt": "Do something",
            "output_format": "text",
            "grading": {"something_else": True},
        }
        cat_dir = tmp_path / "software-engineering"
        cat_dir.mkdir()
        (cat_dir / "SE-BAD.yaml").write_text(yaml.dump(task_yaml, default_flow_style=False))
        results = validate_all_tasks(tmp_path)
        assert len(results) == 1
        assert not results[0].passed
        assert any("rubric" in e and "reference_answer" in e for e in results[0].errors)
