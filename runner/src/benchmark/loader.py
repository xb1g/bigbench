"""Load and validate benchmark task YAML definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
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


# --- Validation ---

VALID_CATEGORIES = {"software-engineering", "planning", "product-mind", "startup-mind"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
REQUIRED_FIELDS = [
    "id", "category", "title", "description", "difficulty",
    "estimated_minutes", "language", "project_ref", "prompt",
    "output_format", "grading",
]


@dataclass
class TaskValidationResult:
    """Result of validating a single task YAML file."""

    path: Path
    task_id: str
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


def validate_all_tasks(tasks_dir: Optional[Path] = None) -> list[TaskValidationResult]:
    """Validate all task YAML files against the schema.

    Checks:
    - Required fields present
    - Valid category value
    - Valid difficulty value
    - Valid grading type (reference_answer or rubric with criteria)
    - Rubric weights sum to 1.0
    - Project_ref exists as directory in ~/dev

    Returns a list of TaskValidationResult, one per task file.
    """
    tasks_dir = tasks_dir or DEFAULT_TASKS_DIR
    if not tasks_dir.exists():
        raise FileNotFoundError(f"Tasks directory not found: {tasks_dir}")

    results: list[TaskValidationResult] = []

    for yaml_file in sorted(tasks_dir.rglob("*.yaml")):
        # Skip schema.yaml
        if yaml_file.name == "schema.yaml":
            continue

        errors: list[str] = []

        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)

            if not data:
                results.append(TaskValidationResult(
                    path=yaml_file, task_id=yaml_file.stem,
                    errors=["Empty task file"],
                ))
                continue

            # Check required fields
            for field_name in REQUIRED_FIELDS:
                if field_name not in data or data[field_name] is None:
                    errors.append(f"Missing required field: {field_name}")
                elif isinstance(data[field_name], str) and not data[field_name].strip():
                    errors.append(f"Required field is empty: {field_name}")

            # Validate category
            category = data.get("category")
            if category and category not in VALID_CATEGORIES:
                errors.append(
                    f"Invalid category: {category!r} "
                    f"(valid: {', '.join(sorted(VALID_CATEGORIES))})"
                )

            # Validate difficulty
            difficulty = data.get("difficulty")
            if difficulty and difficulty not in VALID_DIFFICULTIES:
                errors.append(
                    f"Invalid difficulty: {difficulty!r} "
                    f"(valid: {', '.join(sorted(VALID_DIFFICULTIES))})"
                )

            # Validate grading
            grading = data.get("grading")
            if grading is not None:
                if "rubric" in grading:
                    rubric_data = grading["rubric"]
                    criteria = rubric_data.get("criteria", [])
                    if not criteria:
                        errors.append("Rubric has no criteria")
                    else:
                        # Validate each criterion has required fields
                        for i, c in enumerate(criteria):
                            if "name" not in c:
                                errors.append(f"Criterion {i} missing 'name'")
                            if "weight" not in c:
                                errors.append(f"Criterion {i} missing 'weight'")
                            if "description" not in c:
                                errors.append(f"Criterion {i} missing 'description'")

                        # Check weights sum to 1.0
                        weights = []
                        for c in criteria:
                            w = c.get("weight", 0)
                            try:
                                weights.append(float(w))
                            except (TypeError, ValueError):
                                errors.append(
                                    f"Criterion '{c.get('name', i)}' has non-numeric weight: {w!r}"
                                )
                                weights.append(0.0)
                        if weights:
                            total_weight = sum(weights)
                            if abs(total_weight - 1.0) > 0.01:
                                errors.append(
                                    f"Rubric weights sum to {total_weight:.2f}, expected 1.0"
                                )
                elif "reference_answer" in grading:
                    ref = grading["reference_answer"]
                    if not ref.get("method"):
                        errors.append("Reference answer missing 'method'")
                    if not ref.get("answer"):
                        errors.append("Reference answer missing 'answer'")
                else:
                    errors.append(
                        "Grading must have 'rubric' or 'reference_answer', "
                        f"got: {list(grading.keys())}"
                    )
            elif "grading" in REQUIRED_FIELDS:
                # Already caught by required-fields check above
                pass

            # Validate project_ref exists as directory in ~/dev
            project_ref = data.get("project_ref")
            if project_ref and isinstance(project_ref, str) and project_ref.strip():
                project_path = Path.home() / "dev" / project_ref
                if not project_path.exists():
                    errors.append(
                        f"project_ref directory does not exist: ~/dev/{project_ref}"
                    )

            task_id = data.get("id", yaml_file.stem)
            results.append(TaskValidationResult(
                path=yaml_file, task_id=task_id, errors=errors,
            ))

        except yaml.YAMLError as e:
            results.append(TaskValidationResult(
                path=yaml_file, task_id=yaml_file.stem,
                errors=[f"YAML parse error: {e}"],
            ))
        except Exception as e:
            results.append(TaskValidationResult(
                path=yaml_file, task_id=yaml_file.stem,
                errors=[f"Validation error: {e}"],
            ))

    return results
