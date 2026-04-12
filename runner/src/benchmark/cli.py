"""CLI interface for the LLM Benchmark Runner using Click."""

from __future__ import annotations

import os
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .loader import load_all_tasks
from .results import list_runs, load_results
from .runner import run_all_tasks, run_single_task

console = Console()


def _get_env_config() -> dict:
    """Get configuration from environment variables."""
    return {
        "api_base": os.environ.get("FIREWORKS_API_BASE"),
        "api_key": os.environ.get("FIREWORKS_API_KEY"),
        "default_model": os.environ.get("DEFAULT_MODEL", "gpt-4o"),
        "grading_model": os.environ.get("GRADING_MODEL", os.environ.get("DEFAULT_MODEL", "gpt-4o")),
        "temperature": float(os.environ.get("DEFAULT_TEMPERATURE", "0")),
    }


@click.group()
@click.version_option(version="0.1.0", prog_name="llm-bench")
def main() -> None:
    """LLM Benchmark Runner - Evaluate AI models on SE, planning, product & startup mind."""
    pass


@main.command()
@click.option("--task", "-t", "task_id", help="Run a single task by ID (e.g., SE-001)")
@click.option("--all", "run_all", is_flag=True, help="Run all benchmark tasks")
@click.option(
    "--model", "-m",
    help="LLM model identifier (e.g., gpt-4o, claude-sonnet-4, gemini/gemini-2.5-pro)",
)
@click.option("--dry-run", is_flag=True, help="Execute with mock LLM responses (no API calls)")
@click.option("--temperature", type=float, default=None, help="Sampling temperature (default: 0)")
@click.option("--grading-model", help="Model to use for LLM-as-judge grading")
@click.option("--api-base", help="Custom API base URL")
@click.option("--api-key", help="Custom API key")
def run(
    task_id: Optional[str],
    run_all: bool,
    model: Optional[str],
    dry_run: bool,
    temperature: Optional[float],
    grading_model: Optional[str],
    api_base: Optional[str],
    api_key: Optional[str],
) -> None:
    """Execute benchmark tasks against an LLM model."""
    env = _get_env_config()

    # Resolve model
    model = model or env["default_model"]
    temp = temperature if temperature is not None else env["temperature"]
    g_model = grading_model or env["grading_model"]
    a_base = api_base or env["api_base"]
    a_key = api_key or env["api_key"]

    if not task_id and not run_all:
        console.print("[red]Error: Specify --task <id> or --all[/red]")
        console.print("Use [cyan]llm-bench run --help[/cyan] for usage information.")
        raise SystemExit(1)

    if task_id and run_all:
        console.print("[red]Error: Specify either --task or --all, not both[/red]")
        raise SystemExit(1)

    if task_id:
        # Single task execution
        result = run_single_task(
            task_id=task_id,
            model=model,
            dry_run=dry_run,
            temperature=temp,
            grading_model=g_model,
            api_base=a_base,
            api_key=a_key,
        )

        if result.error:
            console.print(f"\n[red]✗ Task {task_id} failed:[/red] {result.error}")
            raise SystemExit(1)

        # Display result
        _print_task_result(result)

        # Save single task result as a mini-run
        from datetime import datetime

        from .models import RunResults
        from .results import (
            compute_category_scores,
            compute_overall_score,
            generate_run_id,
            save_results,
        )

        run_id = generate_run_id()
        category_scores = compute_category_scores([result])
        overall_score = compute_overall_score(category_scores)

        run_results = RunResults(
            run_id=run_id,
            model_name=model,
            timestamp=datetime.now().isoformat(),
            overall_score=overall_score,
            category_scores=category_scores,
            per_task_results=[result],
            dry_run=dry_run,
        )

        results_path = save_results(run_results)
        console.print(f"\nResults saved to: [cyan]{results_path}[/cyan]")

    elif run_all:
        # Full suite execution - results are saved and printed by run_all_tasks
        run_all_tasks(
            model=model,
            dry_run=dry_run,
            temperature=temp,
            grading_model=g_model,
            api_base=a_base,
            api_key=a_key,
        )


def _print_task_result(result) -> None:
    """Print a formatted single task result."""
    color = "green" if result.score >= 70 else "yellow" if result.score >= 40 else "red"

    panel_content = f"Score: [{color}]{result.score:.1f}/100[/{color}]\n"
    panel_content += f"Category: {result.category}\n"
    method = result.grading_details.grading_method if result.grading_details else "N/A"
    panel_content += f"Method: {method}\n"

    if result.grading_details and result.grading_details.criterion_scores:
        panel_content += "\n[bold]Criterion Breakdown:[/bold]\n"
        for cs in result.grading_details.criterion_scores:
            ratio = cs.score / cs.max_score
            cs_color = "green" if ratio >= 0.7 else "yellow" if ratio >= 0.4 else "red"
            line = (
                f"  • {cs.name}: [{cs_color}]{cs.score:.1f}/{cs.max_score}"
                f"[/{cs_color}] (weight: {cs.weight:.0%})\n"
            )
            panel_content += line
            if cs.rationale:
                panel_content += f"    [dim]{cs.rationale[:100]}[/dim]\n"

    if result.dry_run:
        panel_content += "\n[dim]⚠ Dry-run mode (mock responses)[/dim]"

    console.print(Panel(panel_content, title=f"Task: {result.task_id}", border_style=color))


@main.command()
@click.argument("run_id", required=False)
@click.option("--list", "list_runs_flag", is_flag=True, help="List all available runs")
def results(run_id: Optional[str], list_runs_flag: bool) -> None:
    """Show benchmark results for a run, or list all runs."""
    if list_runs_flag or not run_id:
        # List all runs
        runs = list_runs()
        if not runs:
            console.print("[yellow]No benchmark results found.[/yellow]")
            console.print(
                "Run [cyan]llm-bench run --all --model <model>[/cyan] to generate results."
            )
            return

        table = Table(title="Benchmark Runs", show_header=True, header_style="bold")
        table.add_column("Run ID", style="cyan")
        table.add_column("Model", style="green")
        table.add_column("Timestamp")
        table.add_column("Overall", justify="right")
        table.add_column("SE", justify="right")
        table.add_column("Plan", justify="right")
        table.add_column("Prod", justify="right")
        table.add_column("Start", justify="right")
        table.add_column("Dry Run", justify="center")

        for rid in runs:
            try:
                r = load_results(rid)
                score = r.overall_score
                color = "green" if score >= 70 else "yellow" if score >= 40 else "red"
                table.add_row(
                    rid,
                    r.model_name,
                    r.timestamp[:19],
                    f"[{color}]{r.overall_score:.1f}[/{color}]",
                    f"{r.category_scores.software_engineering:.1f}",
                    f"{r.category_scores.planning:.1f}",
                    f"{r.category_scores.product_mind:.1f}",
                    f"{r.category_scores.startup_mind:.1f}",
                    "✓" if r.dry_run else "",
                )
            except Exception:
                table.add_row(rid, "[dim]error loading[/dim]", "", "", "", "", "", "", "")

        console.print(table)
        return

    # Show specific run
    try:
        r = load_results(run_id)
    except FileNotFoundError:
        console.print(f"[red]Run not found: {run_id}[/red]")
        raise SystemExit(1)

    # Detailed view
    console.print(f"\n[bold]Run:[/bold] {r.run_id}")
    console.print(f"[bold]Model:[/bold] {r.model_name}")
    console.print(f"[bold]Timestamp:[/bold] {r.timestamp}")
    console.print(f"[bold]Overall Score:[/bold] {r.overall_score:.1f}/100")
    if r.dry_run:
        console.print("[dim]⚠ Dry-run mode results[/dim]")

    # Category scores
    console.print("\n[bold]Category Scores:[/bold]")
    cs = r.category_scores
    for name, score in [
        ("Software Engineering", cs.software_engineering),
        ("Planning", cs.planning),
        ("Product Mind", cs.product_mind),
        ("Startup Mind", cs.startup_mind),
    ]:
        color = "green" if score >= 70 else "yellow" if score >= 40 else "red"
        console.print(f"  {name}: [{color}]{score:.1f}[/{color}]")

    # Per-task results
    console.print(f"\n[bold]Per-Task Results ({len(r.per_task_results)} tasks):[/bold]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Task ID", style="cyan")
    table.add_column("Category")
    table.add_column("Score", justify="right")
    table.add_column("Error", style="red")

    for tr in r.per_task_results:
        color = "green" if tr.score >= 70 else "yellow" if tr.score >= 40 else "red"
        table.add_row(
            tr.task_id,
            tr.category,
            f"[{color}]{tr.score:.1f}[/{color}]",
            tr.error or "",
        )

    console.print(table)


@main.command()
@click.option(
    "--category", "-c",
    help="Category: software-engineering, planning, product-mind, startup-mind",
)
@click.option("--id", "task_id", help="Task ID to create (e.g., SE-NEW)")
def task(category: Optional[str], task_id: Optional[str]) -> None:
    """Manage benchmark tasks. Use --category and --id to scaffold a new task."""
    if category and task_id:
        _create_task(category, task_id)
    elif category or task_id:
        console.print("[red]Both --category and --id are required to create a task.[/red]")
        raise SystemExit(1)
    else:
        # List all tasks
        _list_tasks()


def _list_tasks() -> None:
    """List all available benchmark tasks."""
    try:
        tasks = load_all_tasks()
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


    table = Table(title="Benchmark Tasks", show_header=True, header_style="bold")
    table.add_column("ID", style="cyan")
    table.add_column("Category")
    table.add_column("Title")
    table.add_column("Difficulty")
    table.add_column("Language")
    table.add_column("Grading")

    for t in tasks:
        diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(t.difficulty, "")
        table.add_row(
            t.id,
            t.category,
            t.title[:50],
            f"[{diff_color}]{t.difficulty}[/{diff_color}]",
            t.language,
            t.grading_type,
        )

    console.print(table)
    console.print(f"\nTotal: {len(tasks)} tasks")


def _create_task(category: str, task_id: str) -> None:
    """Create a new task YAML from template."""
    from pathlib import Path

    # Validate category
    valid_categories = ["software-engineering", "planning", "product-mind", "startup-mind"]
    if category not in valid_categories:
        console.print(f"[red]Invalid category: {category}[/red]")
        console.print(f"Valid: {', '.join(valid_categories)}")
        raise SystemExit(1)

    tasks_dir = Path(__file__).resolve().parents[3] / "tasks"
    category_dir = tasks_dir / category
    category_dir.mkdir(parents=True, exist_ok=True)

    filepath = category_dir / f"{task_id}.yaml"
    if filepath.exists():
        console.print(f"[red]Task file already exists: {filepath}[/red]")
        raise SystemExit(1)

    template = f"""id: {task_id}
category: {category}
title: "TODO: Add task title (5-15 words)"
description: "TODO: One-paragraph summary of what the task evaluates"
difficulty: medium  # easy, medium, hard
estimated_minutes: 20  # 5-120
language: Python  # Python, TypeScript, JavaScript, Go, Rust, SQL, Shell, Swift, Other
project_ref: "TODO: Directory name under ~/dev/"

prompt: |
  TODO: Write a detailed scenario (200+ words) that the LLM must respond to.
  The prompt should be specific enough to produce gradable, comparable outputs.
  Reference actual code patterns, architectural decisions, or product challenges
  from the project specified in project_ref.

input_format: "TODO: Description of what input the LLM receives"
output_format: "TODO: Description of what the LLM must produce"

grading:
  rubric:
    criteria:
      - name: "Criterion 1"
        weight: 0.3
        description: "TODO: What this criterion measures"
        max_score: 10
      - name: "Criterion 2"
        weight: 0.3
        description: "TODO: What this criterion measures"
        max_score: 10
      - name: "Criterion 3"
        weight: 0.2
        description: "TODO: What this criterion measures"
        max_score: 10
      - name: "Criterion 4"
        weight: 0.2
        description: "TODO: What this criterion measures"
        max_score: 10
    passing_threshold: 60
"""

    filepath.write_text(template)
    console.print(f"[green]✓ Created task template:[/green] {filepath}")
    console.print("[dim]Edit the file to add your task content.[/dim]")


@main.command()
@click.option("--run-id", required=True, help="Run ID to export")
@click.option(
    "--format", "fmt",
    type=click.Choice(["markdown", "json"]),
    default="markdown",
    help="Export format",
)
@click.option("--output", "-o", help="Output file path (default: report_<run_id>.md)")
def report(run_id: str, fmt: str, output: Optional[str]) -> None:
    """Export benchmark results as a formatted report."""
    try:
        r = load_results(run_id)
    except FileNotFoundError:
        console.print(f"[red]Run not found: {run_id}[/red]")
        raise SystemExit(1)

    if fmt == "json":
        # Export as JSON (just copy results)
        out_path = output or f"report_{run_id}.json"
        from pathlib import Path
        Path(out_path).write_text(r.model_dump_json(indent=2) + "\n")
        console.print(f"[green]✓ JSON report exported:[/green] {out_path}")
        return

    # Markdown report
    out_path = output or f"report_{run_id}.md"
    md = _generate_markdown_report(r)
    from pathlib import Path
    Path(out_path).write_text(md)
    console.print(f"[green]✓ Markdown report exported:[/green] {out_path}")


def _generate_markdown_report(r) -> str:
    """Generate a formatted markdown report from run results."""
    from .models import CATEGORY_WEIGHTS

    lines = [
        "# LLM Benchmark Report",
        "",
        f"**Run ID:** {r.run_id}",
        f"**Model:** {r.model_name}",
        f"**Date:** {r.timestamp[:10]}",
        f"**Overall Score:** {r.overall_score:.1f}/100",
        "",
    ]

    if r.dry_run:
        lines.append("> ⚠ **Note:** Results are from dry-run mode (mock LLM responses)")
        lines.append("")

    # Executive Summary
    lines.extend([
        "## Executive Summary",
        "",
        "| Category | Score | Weight | Weighted |",
        "|----------|-------|--------|----------|",
    ])

    cs = r.category_scores
    for name, score, key in [
        ("Software Engineering", cs.software_engineering, "software_engineering"),
        ("Planning", cs.planning, "planning"),
        ("Product Mind", cs.product_mind, "product_mind"),
        ("Startup Mind", cs.startup_mind, "startup_mind"),
    ]:
        weight = CATEGORY_WEIGHTS[key]
        lines.append(f"| {name} | {score:.1f} | {weight:.0%} | {score * weight:.1f} |")

    lines.append(f"| **Overall** | **{r.overall_score:.1f}** | | **{r.overall_score:.1f}** |")
    lines.append("")

    # Per-task results
    lines.extend([
        "## Per-Task Results",
        "",
        "| Task ID | Category | Difficulty | Score |",
        "|---------|----------|------------|-------|",
    ])

    for tr in r.per_task_results:
        status = "✓" if not tr.error else "✗"
        lines.append(f"| {tr.task_id} | {tr.category} | | {tr.score:.1f} {status} |")

    lines.append("")

    # Top and bottom performers
    successful = [tr for tr in r.per_task_results if not tr.error]
    if successful:
        sorted_tasks = sorted(successful, key=lambda t: t.score, reverse=True)
        lines.extend(["### Top 3 Tasks", ""])
        for tr in sorted_tasks[:3]:
            lines.append(f"- **{tr.task_id}** ({tr.category}): {tr.score:.1f}")

        lines.extend(["", "### Bottom 3 Tasks", ""])
        for tr in sorted_tasks[-3:]:
            lines.append(f"- **{tr.task_id}** ({tr.category}): {tr.score:.1f}")

    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
