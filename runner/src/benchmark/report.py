"""Report generation for benchmark results (markdown and JSON)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Optional

from .models import CATEGORY_WEIGHTS, RunResults
from .results import list_runs, load_results

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def _load_runs_for_report(
    run_ids: Optional[list[str]] = None,
    results_dir: Optional[Path] = None,
) -> list[RunResults]:
    """Load run results, either specific IDs or all available."""
    if run_ids:
        return [load_results(rid, results_dir) for rid in run_ids]

    # Load all runs
    all_ids = list_runs(results_dir)
    if not all_ids:
        return []
    runs: list[RunResults] = []
    for rid in all_ids:
        try:
            runs.append(load_results(rid, results_dir))
        except Exception:
            continue
    return runs


def _rank_models(runs: list[RunResults]) -> list[RunResults]:
    """Return runs sorted by overall_score descending."""
    return sorted(runs, key=lambda r: r.overall_score, reverse=True)


def _score_label(score: float) -> str:
    """Human-readable score label."""
    if score >= 80:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 60:
        return "Fair"
    if score >= 40:
        return "Needs Improvement"
    return "Poor"


def _score_emoji(score: float) -> str:
    """Emoji for score band."""
    if score >= 80:
        return "🟢"
    if score >= 60:
        return "🟡"
    if score >= 40:
        return "🟠"
    return "🔴"


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def generate_markdown_report(
    run_ids: Optional[list[str]] = None,
    results_dir: Optional[Path] = None,
) -> str:
    """Generate a full markdown report from benchmark results.

    If *run_ids* is provided, only those runs are included; otherwise all
    available runs are loaded for comparison.
    """
    runs = _load_runs_for_report(run_ids, results_dir)
    if not runs:
        return "# LLM Benchmark Report\n\nNo benchmark results found.\n"

    ranked = _rank_models(runs)
    lines: list[str] = []

    # --- Header ---
    lines.append("# LLM Benchmark Report")
    lines.append("")
    lines.append(f"**Date Generated:** {_today()}")
    lines.append(f"**Models Compared:** {len(runs)}")
    lines.append(f"**Runs Analyzed:** {len(runs)}")
    any_dry = any(r.dry_run for r in runs)
    if any_dry:
        lines.append("")
        lines.append("> ⚠ **Note:** Some results are from dry-run mode (mock LLM responses)")
    lines.append("")

    # --- 1. Executive Summary ---
    lines.extend(_executive_summary(ranked))

    # --- 2. Per-Category Analysis ---
    lines.extend(_per_category_analysis(runs))

    # --- 3. Per-Model Breakdown ---
    lines.extend(_per_model_breakdown(runs))

    # --- 4. Recommendations ---
    lines.extend(_recommendations(runs))

    lines.append("")
    return "\n".join(lines)


def _today() -> str:
    return date.today().isoformat()


def _executive_summary(ranked: list[RunResults]) -> list[str]:
    """Section 1: Executive Summary – table of all models, overall scores, rankings."""
    lines: list[str] = [
        "## Executive Summary",
        "",
        "| Rank | Model | Overall Score | SE | Planning | Product Mind | Startup Mind | Rating |",
        "|-----:|-------|-------------:|---:|--------:|-------------:|-------------:|--------|",
    ]

    for i, r in enumerate(ranked, 1):
        cs = r.category_scores
        rating = _score_label(r.overall_score)
        emoji = _score_emoji(r.overall_score)
        lines.append(
            f"| {i} | {r.model_name} | "
            f"{r.overall_score:.1f} | "
            f"{cs.software_engineering:.1f} | "
            f"{cs.planning:.1f} | "
            f"{cs.product_mind:.1f} | "
            f"{cs.startup_mind:.1f} | "
            f"{emoji} {rating} |"
        )

    lines.append("")
    return lines


def _per_category_analysis(runs: list[RunResults]) -> list[str]:
    """Section 2: Per-Category Analysis – avg, best, worst, distribution per category."""
    lines: list[str] = [
        "## Per-Category Analysis",
        "",
    ]

    categories = [
        ("Software Engineering", "software_engineering"),
        ("Planning", "planning"),
        ("Product Mind", "product_mind"),
        ("Startup Mind", "startup_mind"),
    ]

    for cat_name, cat_key in categories:
        weight = CATEGORY_WEIGHTS[cat_key]
        scores: list[tuple[str, float]] = []
        for r in runs:
            val = getattr(r.category_scores, cat_key)
            scores.append((r.model_name, val))

        if not scores:
            continue

        avg_score = sum(s for _, s in scores) / len(scores)
        best_model, best_score = max(scores, key=lambda x: x[1])
        worst_model, worst_score = min(scores, key=lambda x: x[1])
        score_range = best_score - worst_score

        lines.append(f"### {cat_name} (weight: {weight:.0%})")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|------|")
        lines.append(f"| Average Score | {avg_score:.1f} |")
        lines.append(f"| Best Model | {best_model} ({best_score:.1f}) |")
        lines.append(f"| Worst Model | {worst_model} ({worst_score:.1f}) |")
        lines.append(f"| Score Range | {score_range:.1f} |")
        lines.append("")

        # Score distribution
        lines.append("**Score Distribution:**")
        lines.append("")
        lines.append("| Model | Score | Visual |")
        lines.append("|-------|------:|--------|")
        for model, score in sorted(scores, key=lambda x: x[1], reverse=True):
            bar_len = int(score / 5)  # 1 char per 5 points
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"| {model} | {score:.1f} | `{bar}` |")
        lines.append("")

    return lines


def _per_model_breakdown(runs: list[RunResults]) -> list[str]:
    """Section 3: Per-Model Breakdown – overall, category scores, top/bottom tasks."""
    lines: list[str] = [
        "## Per-Model Breakdown",
        "",
    ]

    for r in runs:
        cs = r.category_scores
        lines.append(f"### {r.model_name}")
        lines.append("")
        lines.append(f"- **Run ID:** {r.run_id}")
        label = _score_label(r.overall_score)
        lines.append(f"- **Overall Score:** {r.overall_score:.1f} ({label})")
        if r.dry_run:
            lines.append("- **Mode:** Dry-run (mock responses)")
        lines.append("")
        lines.append("| Category | Score | Weight | Weighted |")
        lines.append("|----------|------:|-------:|---------:|")
        for cat_name, cat_key in [
            ("Software Engineering", "software_engineering"),
            ("Planning", "planning"),
            ("Product Mind", "product_mind"),
            ("Startup Mind", "startup_mind"),
        ]:
            score = getattr(cs, cat_key)
            weight = CATEGORY_WEIGHTS[cat_key]
            lines.append(f"| {cat_name} | {score:.1f} | {weight:.0%} | {score * weight:.1f} |")
        lines.append("")

        # Top 3 and Bottom 3 tasks
        successful = [t for t in r.per_task_results if not t.error]
        if successful:
            sorted_tasks = sorted(successful, key=lambda t: t.score, reverse=True)

            lines.append("**Top 3 Tasks:**")
            lines.append("")
            for t in sorted_tasks[:3]:
                lines.append(f"- **{t.task_id}** ({t.category}): {t.score:.1f}")
            lines.append("")

            lines.append("**Bottom 3 Tasks:**")
            lines.append("")
            for t in sorted_tasks[-3:]:
                lines.append(f"- **{t.task_id}** ({t.category}): {t.score:.1f}")
            lines.append("")

        # Errors
        errored = [t for t in r.per_task_results if t.error]
        if errored:
            lines.append(f"**Failed Tasks ({len(errored)}):**")
            lines.append("")
            for t in errored:
                lines.append(f"- **{t.task_id}**: {t.error[:80]}")
            lines.append("")

    return lines


def _recommendations(runs: list[RunResults]) -> list[str]:
    """Section 4: Recommendations – actionable insights based on score patterns."""
    lines: list[str] = [
        "## Recommendations",
        "",
    ]

    if len(runs) == 1:
        lines.extend(_single_run_recommendations(runs[0]))
    else:
        lines.extend(_multi_run_recommendations(runs))

    return lines


def _single_run_recommendations(r: RunResults) -> list[str]:
    """Generate recommendations for a single model run."""
    lines: list[str] = []
    cs = r.category_scores

    # Identify weakest category
    cat_scores = {
        "Software Engineering": cs.software_engineering,
        "Planning": cs.planning,
        "Product Mind": cs.product_mind,
        "Startup Mind": cs.startup_mind,
    }
    weakest_cat = min(cat_scores, key=cat_scores.get)
    strongest_cat = max(cat_scores, key=cat_scores.get)

    ws = cat_scores[weakest_cat]
    lines.append(f"1. **Focus area:** {weakest_cat} is the weakest category "
                 f"({ws:.1f}). "
                 "Prioritize improvements here for the biggest overall score gain.")
    ss = cat_scores[strongest_cat]
    lines.append(f"2. **Strength:** {strongest_cat} is the strongest category "
                 f"({ss:.1f}). Leverage this as a differentiator.")

    # Task-level insights
    successful = [t for t in r.per_task_results if not t.error]
    if successful:
        low_tasks = [t for t in successful if t.score < 40]
        if low_tasks:
            lines.append(f"3. **Struggling tasks:** {len(low_tasks)} task(s) scored below 40. "
                         f"Review task IDs: {', '.join(t.task_id for t in low_tasks[:5])}.")

        high_tasks = [t for t in successful if t.score >= 80]
        if high_tasks:
            ids = ", ".join(t.task_id for t in high_tasks[:5])
            lines.append(f"4. **High performers:** {len(high_tasks)} task(s) scored 80+. "
                         f"These demonstrate strong capability: {ids}.")

    # Overall assessment
    if r.overall_score >= 70:
        lines.append(f"5. **Overall:** {r.model_name} shows strong performance across categories. "
                     f"Consider it for production use.")
    elif r.overall_score >= 50:
        lines.append(f"5. **Overall:** {r.model_name} shows moderate performance. "
                     f"Best suited for tasks in {strongest_cat}.")
    else:
        lines.append(f"5. **Overall:** {r.model_name} needs significant improvement. "
                     f"Consider alternative models or fine-tuning for better results.")

    lines.append("")
    return lines


def _multi_run_recommendations(runs: list[RunResults]) -> list[str]:
    """Generate recommendations comparing multiple model runs."""
    lines: list[str] = []
    ranked = _rank_models(runs)
    best = ranked[0]
    worst = ranked[-1]

    # Best overall
    lines.append(f"1. **Best overall model:** {best.model_name} "
                 f"(score: {best.overall_score:.1f}). Recommended as the primary choice.")

    # Category-specific winners
    for cat_name, cat_key in [
        ("Software Engineering", "software_engineering"),
        ("Planning", "planning"),
        ("Product Mind", "product_mind"),
        ("Startup Mind", "startup_mind"),
    ]:
        best_for_cat = max(runs, key=lambda r: getattr(r.category_scores, cat_key))
        score = getattr(best_for_cat.category_scores, cat_key)
        if best_for_cat.model_name != best.model_name:
            lines.append(f"2. **Best for {cat_name}:** {best_for_cat.model_name} ({score:.1f}). "
                         f"Consider this model for {cat_name.lower()}-focused tasks.")

    # Gap analysis
    gap = best.overall_score - worst.overall_score
    if gap > 20:
        lines.append(f"3. **Significant gap:** {gap:.1f} points between best and worst. "
                     "The lower-performing model may not be suitable "
                     "for this benchmark's requirements.")
    elif gap > 10:
        lines.append(f"3. **Moderate gap:** {gap:.1f} points between best and worst. "
                     f"Consider cost/performance tradeoffs when selecting a model.")

    # Unanimous weaknesses
    weak_cats: list[str] = []
    for cat_name, cat_key in [
        ("Software Engineering", "software_engineering"),
        ("Planning", "planning"),
        ("Product Mind", "product_mind"),
        ("Startup Mind", "startup_mind"),
    ]:
        avg = sum(getattr(r.category_scores, cat_key) for r in runs) / len(runs)
        if avg < 50:
            weak_cats.append(cat_name)
    if weak_cats:
        lines.append(f"4. **Systemic weakness:** All models struggle with: "
                     f"{', '.join(weak_cats)}. This may indicate the tasks need prompt refinement "
                     f"or that current LLMs lack capability in these areas.")

    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# JSON report
# ---------------------------------------------------------------------------

def generate_json_report(
    run_ids: Optional[list[str]] = None,
    results_dir: Optional[Path] = None,
) -> str:
    """Export raw JSON data for the specified runs.

    Returns a JSON string containing a list of run result objects.
    """
    runs = _load_runs_for_report(run_ids, results_dir)
    data = [json.loads(r.model_dump_json()) for r in runs]
    return json.dumps(data, indent=2) + "\n"
