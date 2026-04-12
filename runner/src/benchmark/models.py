"""Pydantic models for benchmark results and task definitions."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

# --- Task Definition Models ---


class GradingCriterion(BaseModel):
    """A single criterion in a rubric."""

    name: str
    weight: float = Field(ge=0.0, le=1.0)
    description: str
    max_score: int = Field(default=10, ge=1)


class Rubric(BaseModel):
    """Rubric-based grading configuration."""

    criteria: list[GradingCriterion]
    passing_threshold: int = Field(default=60, ge=0, le=100)


class ReferenceAnswer(BaseModel):
    """Reference answer for auto-grading."""

    method: str  # exact_match, structural_similarity, code_equivalence
    answer: str
    key_elements: list[str] = Field(default_factory=list)
    tolerance: Optional[float] = None


class TaskDefinition(BaseModel):
    """A single benchmark task definition loaded from YAML."""

    id: str
    category: str
    title: str
    description: str
    difficulty: str
    estimated_minutes: int
    language: str
    project_ref: str
    prompt: str
    input_format: str
    output_format: str
    grading_type: str = Field(default="rubric")  # "rubric" or "reference_answer"
    rubric: Optional[Rubric] = None
    reference_answer: Optional[ReferenceAnswer] = None


# --- Grading Result Models ---


class CriterionScore(BaseModel):
    """Score for a single rubric criterion."""

    name: str
    score: float = Field(ge=0)
    max_score: float = Field(ge=1)
    weight: float = Field(ge=0.0, le=1.0)
    rationale: str = ""


class GradingDetails(BaseModel):
    """Detailed grading results for a task."""

    grading_method: str  # "auto", "rubric", "llm_judge"
    total_score: float = Field(ge=0, le=100)
    criterion_scores: list[CriterionScore] = Field(default_factory=list)
    reference_match_type: Optional[str] = None  # exact, structural, partial, none
    rationale: str = ""


# --- Per-Task Result ---


class TaskResult(BaseModel):
    """Result for a single benchmark task."""

    task_id: str
    category: str
    score: float = Field(ge=0, le=100)
    raw_output: str = ""
    grading_details: Optional[GradingDetails] = None
    error: Optional[str] = None
    dry_run: bool = False


# --- Category Scores ---


class CategoryScores(BaseModel):
    """Scores per benchmark category."""

    software_engineering: float = Field(default=0.0, ge=0, le=100)
    planning: float = Field(default=0.0, ge=0, le=100)
    product_mind: float = Field(default=0.0, ge=0, le=100)
    startup_mind: float = Field(default=0.0, ge=0, le=100)


# --- Run Results ---


class RunResults(BaseModel):
    """Complete results for a benchmark run."""

    run_id: str
    model_name: str
    timestamp: str
    overall_score: float = Field(default=0.0, ge=0, le=100)
    category_scores: CategoryScores = Field(default_factory=CategoryScores)
    per_task_results: list[TaskResult] = Field(default_factory=list)
    dry_run: bool = False


# --- Category Mapping ---


CATEGORY_MAP: dict[str, str] = {
    "software-engineering": "software_engineering",
    "planning": "planning",
    "product-mind": "product_mind",
    "startup-mind": "startup_mind",
}

CATEGORY_WEIGHTS: dict[str, float] = {
    "software_engineering": 0.40,
    "planning": 0.25,
    "product_mind": 0.20,
    "startup_mind": 0.15,
}
