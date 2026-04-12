"""Load and validate benchmark task YAML definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from .models import GradingCriterion, ReferenceAnswer, Rubric, TaskDefinition

# Default tasks directory relative to project root
DEFAULT_TASKS_DIR = Path(__file__).resolve().parents[3] / "tasks"


def _parse_grading(grading_data: dict) -> tuple[str, Optional[Rubric], Optional[ReferenceAnswer]]:
    """Parse the grading section of a task YAML.

    Returns (grading_type, rubric, reference_answer).
    """
    if "rubric" in grading_data:
        rubric_data = grading_data["rubric"]
        criteria = [
            GradingCriterion(
                name=c["name"],
                weight=c["weight"],
                description=c["description"],
                max_score=c.get("max_score", 10),
            )
            for c in rubric_data.get("criteria", [])
        ]
        rubric = Rubric(
            criteria=criteria,
            passing_threshold=rubric_data.get("passing_threshold", 60),
        )
        return "rubric", rubric, None

    if "reference_answer" in grading_data:
        ref_data = grading_data["reference_answer"]
        ref_answer = ReferenceAnswer(
            method=ref_data["method"],
            answer=ref_data["answer"],
            key_elements=ref_data.get("key_elements", []),
            tolerance=ref_data.get("tolerance"),
        )
        return "reference_answer", None, ref_answer

    raise ValueError(
        f"Task grading must have 'rubric' or 'reference_answer', "
        f"got: {list(grading_data.keys())}"
    )


def load_task(task_path: Path) -> TaskDefinition:
    """Load a single task definition from a YAML file."""
    with open(task_path) as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Empty task file: {task_path}")

    grading_type, rubric, reference_answer = _parse_grading(data.get("grading", {}))

    return TaskDefinition(
        id=data["id"],
        category=data["category"],
        title=data["title"],
        description=data["description"],
        difficulty=data["difficulty"],
        estimated_minutes=data["estimated_minutes"],
        language=data["language"],
        project_ref=data["project_ref"],
        prompt=data["prompt"],
        input_format=data.get("input_format", ""),
        output_format=data.get("output_format", ""),
        grading_type=grading_type,
        rubric=rubric,
        reference_answer=reference_answer,
    )


def load_all_tasks(tasks_dir: Optional[Path] = None) -> list[TaskDefinition]:
    """Load all task definitions from the tasks directory.

    Returns a sorted list by (category, id).
    """
    tasks_dir = tasks_dir or DEFAULT_TASKS_DIR
    if not tasks_dir.exists():
        raise FileNotFoundError(f"Tasks directory not found: {tasks_dir}")

    tasks: list[TaskDefinition] = []
    for yaml_file in sorted(tasks_dir.rglob("*.yaml")):
        # Skip schema.yaml
        if yaml_file.name == "schema.yaml":
            continue
        try:
            task = load_task(yaml_file)
            tasks.append(task)
        except Exception as e:
            raise ValueError(f"Failed to load task from {yaml_file}: {e}") from e

    # Sort by category then id
    tasks.sort(key=lambda t: (t.category, t.id))
    return tasks


def load_task_by_id(task_id: str, tasks_dir: Optional[Path] = None) -> TaskDefinition:
    """Load a specific task by its ID (e.g., SE-001)."""
    tasks = load_all_tasks(tasks_dir)
    for task in tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"Task not found: {task_id}")


def get_tasks_by_category(tasks: list[TaskDefinition]) -> dict[str, list[TaskDefinition]]:
    """Group tasks by category."""
    categories: dict[str, list[TaskDefinition]] = {}
    for task in tasks:
        categories.setdefault(task.category, []).append(task)
    return categories
