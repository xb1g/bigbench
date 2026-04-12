"""Core benchmark runner - orchestrates task execution, grading, and results."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table

from .grader import grade_task
from .llm_client import call_llm, get_model_info
from .loader import load_all_tasks, load_task_by_id
from .models import (
    CATEGORY_WEIGHTS,
    RunResults,
    TaskResult,
)
from .results import (
    compute_category_scores,
    compute_overall_score,
    generate_run_id,
    save_results,
)

console = Console()


def run_single_task(
    task_id: str,
    model: str,
    dry_run: bool = False,
    temperature: float = 0.0,
    grading_model: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TaskResult:
    """Execute a single benchmark task and return scored result.

    Args:
        task_id: Task identifier (e.g., 'SE-001')
        model: LLM model to use
        dry_run: If True, use mock LLM responses
        temperature: Sampling temperature
        grading_model: Model for LLM-as-judge grading
        api_base: Custom API base URL
        api_key: Custom API key

    Returns:
        TaskResult with score and grading details.
    """
    # Load task
    try:
        task = load_task_by_id(task_id)
    except ValueError as e:
        return TaskResult(
            task_id=task_id,
            category="unknown",
            score=0.0,
            error=str(e),
            dry_run=dry_run,
        )

    # Call LLM
    try:
        raw_output = call_llm(
            model=model,
            prompt=task.prompt,
            temperature=temperature,
            dry_run=dry_run,
            api_base=api_base,
            api_key=api_key,
        )
    except Exception as e:
        return TaskResult(
            task_id=task.id,
            category=task.category,
            score=0.0,
            raw_output="",
            error=f"LLM call failed: {type(e).__name__}: {e}",
            dry_run=dry_run,
        )

    # Grade the output
    try:
        grading_details = grade_task(
            task=task,
            raw_output=raw_output,
            grading_model=grading_model,
            dry_run=dry_run,
        )
    except Exception as e:
        return TaskResult(
            task_id=task.id,
            category=task.category,
            score=0.0,
            raw_output=raw_output,
            error=f"Grading failed: {type(e).__name__}: {e}",
            dry_run=dry_run,
        )

    return TaskResult(
        task_id=task.id,
        category=task.category,
        score=grading_details.total_score,
        raw_output=raw_output,
        grading_details=grading_details,
        dry_run=dry_run,
    )


def run_all_tasks(
    model: str,
    dry_run: bool = False,
    temperature: float = 0.0,
    grading_model: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    tasks_dir: Optional[str] = None,
) -> RunResults:
    """Execute all benchmark tasks and produce combined results.

    Single task failures are recorded but don't crash the suite.

    Args:
        model: LLM model to use
        dry_run: If True, use mock LLM responses
        temperature: Sampling temperature
        grading_model: Model for LLM-as-judge grading
        api_base: Custom API base URL
        api_key: Custom API key
        tasks_dir: Override tasks directory

    Returns:
        RunResults with all scores and category breakdowns.
    """
    from pathlib import Path

    # Load all tasks
    tdir = Path(tasks_dir) if tasks_dir else None
    tasks = load_all_tasks(tdir)

    run_id = generate_run_id()
    model_info = get_model_info(model)

    console.print("\n[bold]LLM Benchmark Runner[/bold]")
    console.print(f"Run ID: [cyan]{run_id}[/cyan]")
    console.print(f"Model: [green]{model}[/green] ({model_info['provider']})")
    console.print(f"Tasks: [yellow]{len(tasks)}[/yellow]")
    if dry_run:
        console.print("[dim]Mode: DRY-RUN (mock responses)[/dim]")
    console.print()

    task_results: list[TaskResult] = []
    errors: list[str] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task_progress = progress.add_task("Running tasks...", total=len(tasks))

        for i, task in enumerate(tasks, 1):
            progress.update(task_progress, description=f"[{task.id}] {task.title[:40]}")

            result = run_single_task(
                task_id=task.id,
                model=model,
                dry_run=dry_run,
                temperature=temperature,
                grading_model=grading_model,
                api_base=api_base,
                api_key=api_key,
            )

            task_results.append(result)

            if result.error:
                errors.append(f"{task.id}: {result.error}")
                console.print(f"  [red]✗[/red] {task.id} - Error: {result.error[:60]}")
            else:
                sc = result.score
                color = "green" if sc >= 70 else "yellow" if sc >= 40 else "red"
                console.print(
                    f"  [green]✓[/green] {task.id} - "
                    f"Score: [{color}]{sc:.1f}[/{color}]"
                )

            progress.update(task_progress, advance=1)

    # Compute category and overall scores
    category_scores = compute_category_scores(task_results)
    overall_score = compute_overall_score(category_scores)

    results = RunResults(
        run_id=run_id,
        model_name=model,
        timestamp=datetime.now().isoformat(),
        overall_score=overall_score,
        category_scores=category_scores,
        per_task_results=task_results,
        dry_run=dry_run,
    )

    # Save results
    results_path = save_results(results)

    # Print summary
    _print_summary(results)

    if errors:
        console.print(f"\n[yellow]⚠ {len(errors)} task(s) had errors:[/yellow]")
        for err in errors:
            console.print(f"  [dim]- {err}[/dim]")

    console.print(f"\nResults saved to: [cyan]{results_path}[/cyan]")

    return results


def _print_summary(results: RunResults) -> None:
    """Print a formatted summary table of results."""
    console.print()

    # Category scores table
    table = Table(title="Benchmark Results Summary", show_header=True, header_style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Weight", justify="right")
    table.add_column("Weighted", justify="right")

    cs = results.category_scores
    categories = [
        ("Software Engineering", cs.software_engineering, "software_engineering"),
        ("Planning", cs.planning, "planning"),
        ("Product Mind", cs.product_mind, "product_mind"),
        ("Startup Mind", cs.startup_mind, "startup_mind"),
    ]

    for name, score, key in categories:
        weight = CATEGORY_WEIGHTS[key]
        color = "green" if score >= 70 else "yellow" if score >= 40 else "red"
        table.add_row(
            name,
            f"[{color}]{score:.1f}[/{color}]",
            f"{weight:.0%}",
            f"{score * weight:.1f}",
        )

    table.add_section()
    table.add_row(
        "[bold]Overall[/bold]",
        f"[bold]{results.overall_score:.1f}[/bold]",
        "",
        f"[bold]{results.overall_score:.1f}[/bold]",
    )

    console.print(table)

    if results.dry_run:
        console.print("[dim]Note: Results are from dry-run mode (mock LLM responses)[/dim]")
