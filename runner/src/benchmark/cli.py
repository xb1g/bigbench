"""CLI interface for the LLM Benchmark Runner using Click."""

from __future__ import annotations

import os
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .loader import load_all_tasks, validate_all_tasks
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
@click.option("--limit", type=int, default=None, help="Limit number of tasks to run (with --all)")
def run(
    task_id: Optional[str],
    run_all: bool,
    model: Optional[str],
    dry_run: bool,
    temperature: Optional[float],
    grading_model: Optional[str],
    api_base: Optional[str],
    api_key: Optional[str],
    limit: Optional[int],
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
            limit=limit,
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


@main.group(invoke_without_command=True)
@click.pass_context
def model(ctx: click.Context) -> None:
    """Manage model presets and configuration."""
    if ctx.invoked_subcommand is None:
        # Default to 'list' when no subcommand given
        _list_models()


@model.command("list")
def model_list() -> None:
    """List available model presets with usage instructions."""
    _list_models()


def _list_models() -> None:
    """List available model presets with usage instructions."""
    from .llm_client import MODEL_PRESETS

    table = Table(title="Model Presets", show_header=True, header_style="bold")
    table.add_column("Preset ID", style="cyan")
    table.add_column("Provider", style="green")
    table.add_column("Default API Base", style="yellow")
    table.add_column("Instructions", style="dim")

    for preset_id, preset in MODEL_PRESETS.items():
        table.add_row(
            preset_id,
            preset["provider"],
            preset.get("default_api_base", ""),
            preset.get("instructions", ""),
        )

    console.print(table)
    console.print(
        "\n[dim]Override defaults with --api-base and --api-key flags.[/dim]"
    )
    console.print(
        "[dim]Example: llm-bench run --all --model ollama/llama3 --limit 5[/dim]"
    )
    console.print(
        "[dim]Custom: llm-bench run --task SE-001 --model local/my-model "
        "--api-base http://localhost:1234/v1[/dim]"
    )


@main.group(invoke_without_command=True)
@click.pass_context
def task(ctx: click.Context) -> None:
    """Manage benchmark tasks (list, create, validate)."""
    if ctx.invoked_subcommand is None:
        # Default to 'list' when no subcommand given
        _list_tasks()


@task.command("list")
def task_list() -> None:
    """List all available benchmark tasks."""
    _list_tasks()


@task.command("create")
@click.option(
    "--category", "-c",
    required=True,
    help="Category: software-engineering, planning, product-mind, startup-mind",
)
@click.option("--id", "task_id", required=True, help="Task ID to create (e.g., SE-NEW)")
def task_create(category: str, task_id: str) -> None:
    """Scaffold a new task YAML file with template values."""
    _create_task(category, task_id)


@task.command("validate")
def task_validate() -> None:
    """Validate ALL task YAML files against the schema."""
    try:
        results = validate_all_tasks()
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed

    # Print per-task results
    table = Table(
        title="Task Validation Results",
        show_header=True,
        header_style="bold",
    )
    table.add_column("Task ID", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Errors", style="red")

    for r in results:
        if r.passed:
            table.add_row(r.task_id, "[green]✓ PASS[/green]", "")
        else:
            error_text = "\n".join(r.errors)
            table.add_row(r.task_id, "[red]✗ FAIL[/red]", error_text)

    console.print(table)

    # Summary
    if failed == 0:
        console.print(f"\n[green]✓ All {total} tasks passed validation.[/green]")
    else:
        console.print(
            f"\n[red]✗ {failed}/{total} tasks failed validation.[/red]"
        )
        raise SystemExit(1)


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


@main.group(invoke_without_command=True)
@click.pass_context
def report(ctx: click.Context) -> None:
    """Export and manage benchmark reports."""
    if ctx.invoked_subcommand is None:
        # Show help when no subcommand given
        console.print(ctx.get_help())


@report.command("export")
@click.option("--run-id", multiple=True,
              help="Run ID(s) to export (can be repeated). Omit for all runs.")
@click.option(
    "--format", "fmt",
    type=click.Choice(["markdown", "json"]),
    default="markdown",
    help="Export format",
)
@click.option("--output", "-o", help="Output file path (default: report.md or report.json)")
def report_export(run_id: tuple[str, ...], fmt: str, output: Optional[str]) -> None:
    """Export benchmark results as a formatted report.

    Generates a report with Executive Summary, Per-Category Analysis,
    Per-Model Breakdown, and Recommendations.

    Use --run-id multiple times to compare specific runs, or omit to compare all.
    """
    from .report import generate_json_report, generate_markdown_report

    run_ids = list(run_id) if run_id else None

    # Validate that specified run IDs exist
    if run_ids:
        for rid in run_ids:
            try:
                load_results(rid)
            except FileNotFoundError:
                console.print(f"[red]Run not found: {rid}[/red]")
                raise SystemExit(1)

    if fmt == "json":
        out_path = output or "report.json"
        from pathlib import Path
        json_content = generate_json_report(run_ids=run_ids)
        Path(out_path).write_text(json_content)
        console.print(f"[green]✓ JSON report exported:[/green] {out_path}")
        return

    # Markdown report
    out_path = output or "report.md"
    from pathlib import Path
    md = generate_markdown_report(run_ids=run_ids)
    Path(out_path).write_text(md)
    console.print(f"[green]✓ Markdown report exported:[/green] {out_path}")


if __name__ == "__main__":
    main()
