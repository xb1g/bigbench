"""Results storage with atomic file writes."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import (
    CATEGORY_MAP,
    CATEGORY_WEIGHTS,
    CategoryScores,
    RunResults,
    TaskResult,
)

# Default results directory relative to project root
DEFAULT_RESULTS_DIR = Path(__file__).resolve().parents[3] / "results"


def generate_run_id() -> str:
    """Generate a unique run ID based on timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def compute_category_scores(task_results: list[TaskResult]) -> CategoryScores:
    """Compute per-category scores as the average of tasks in each category.

    Categories with no tasks get a score of 0.0.
    """
    category_totals: dict[str, list[float]] = {
        "software_engineering": [],
        "planning": [],
        "product_mind": [],
        "startup_mind": [],
    }

    for result in task_results:
        # Map YAML category names to result category keys
        category_key = CATEGORY_MAP.get(result.category, result.category)
        if category_key in category_totals:
            category_totals[category_key].append(result.score)

    def _avg(key: str) -> float:
        vals = category_totals[key]
        return round(sum(vals) / len(vals), 1) if vals else 0.0

    scores = CategoryScores(
        software_engineering=_avg("software_engineering"),
        planning=_avg("planning"),
        product_mind=_avg("product_mind"),
        startup_mind=_avg("startup_mind"),
    )

    return scores


def compute_overall_score(category_scores: CategoryScores) -> float:
    """Compute overall weighted score.

    Formula: se*0.40 + planning*0.25 + product*0.20 + startup*0.15
    """
    overall = (
        category_scores.software_engineering * CATEGORY_WEIGHTS["software_engineering"]
        + category_scores.planning * CATEGORY_WEIGHTS["planning"]
        + category_scores.product_mind * CATEGORY_WEIGHTS["product_mind"]
        + category_scores.startup_mind * CATEGORY_WEIGHTS["startup_mind"]
    )
    return round(overall, 1)


def save_results(
    results: RunResults,
    results_dir: Optional[Path] = None,
) -> Path:
    """Save results to JSON with atomic file write.

    Writes to a .tmp file first, then renames to final path.
    This prevents partial/corrupt writes on crash.

    Returns the path to the saved results file.
    """
    results_dir = results_dir or DEFAULT_RESULTS_DIR
    run_dir = results_dir / results.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    final_path = run_dir / "results.json"
    tmp_path = run_dir / "results.json.tmp"

    # Write to temp file
    with open(tmp_path, "w") as f:
        f.write(results.model_dump_json(indent=2))
        f.write("\n")

    # Atomic rename
    os.replace(tmp_path, final_path)

    return final_path


def load_results(run_id: str, results_dir: Optional[Path] = None) -> RunResults:
    """Load results for a given run ID."""
    results_dir = results_dir or DEFAULT_RESULTS_DIR
    results_path = results_dir / run_id / "results.json"

    if not results_path.exists():
        raise FileNotFoundError(f"Results not found for run: {run_id}")

    with open(results_path) as f:
        data = json.load(f)

    return RunResults.model_validate(data)


def list_runs(results_dir: Optional[Path] = None) -> list[str]:
    """List all available run IDs, sorted newest first."""
    results_dir = results_dir or DEFAULT_RESULTS_DIR
    if not results_dir.exists():
        return []

    runs = []
    for entry in sorted(results_dir.iterdir(), reverse=True):
        if entry.is_dir() and (entry / "results.json").exists():
            runs.append(entry.name)

    return runs
