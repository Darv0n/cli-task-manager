"""Output formatters. Rich tables for list view, plain text for single items."""

from __future__ import annotations

from rich import box
from rich.console import Console
from rich.table import Table

from task_manager.contracts import Priority, Status
from task_manager.models import Task

console = Console()

_PRIORITY_COLOR = {
    Priority.LOW: "dim",
    Priority.MEDIUM: "white",
    Priority.HIGH: "yellow",
    Priority.URGENT: "bold red",
}

_STATUS_COLOR = {
    Status.OPEN: "cyan",
    Status.IN_PROGRESS: "blue",
    Status.DONE: "green",
    Status.CANCELLED: "dim",
}


def print_task_list(tasks: list[Task], *, date_format: str = "%Y-%m-%d") -> None:
    if not tasks:
        console.print("[dim]No tasks found.[/dim]")
        return

    table = Table(box=box.SIMPLE_HEAD, show_footer=False)
    table.add_column("ID", style="dim", width=12)
    table.add_column("Title", min_width=20)
    table.add_column("Status", width=12)
    table.add_column("Priority", width=10)
    table.add_column("Tags", width=20)
    table.add_column("Due", width=12)
    table.add_column("Project", width=12)

    for task in tasks:
        status_color = _STATUS_COLOR.get(task.status, "white")
        priority_color = _PRIORITY_COLOR.get(task.priority, "white")
        due_str = task.due_date.strftime(date_format) if task.due_date else ""
        tags_str = ", ".join(task.tags) if task.tags else ""

        table.add_row(
            task.id[:10],
            task.title,
            f"[{status_color}]{task.status.value}[/{status_color}]",
            f"[{priority_color}]{task.priority.value}[/{priority_color}]",
            tags_str,
            due_str,
            task.project or "",
        )

    console.print(table)


def print_task_detail(task: Task, *, date_format: str = "%Y-%m-%d") -> None:
    """Single task view — key/value pairs."""
    priority_color = _PRIORITY_COLOR.get(task.priority, "white")
    status_color = _STATUS_COLOR.get(task.status, "white")

    console.print(f"[bold]{task.title}[/bold]")
    console.print(f"  [dim]ID:[/dim]          {task.id}")
    console.print(f"  [dim]Status:[/dim]      [{status_color}]{task.status.value}[/{status_color}]")
    console.print(
        f"  [dim]Priority:[/dim]    [{priority_color}]{task.priority.value}[/{priority_color}]"
    )
    if task.description:
        console.print(f"  [dim]Description:[/dim] {task.description}")
    if task.tags:
        console.print(f"  [dim]Tags:[/dim]        {', '.join(task.tags)}")
    if task.project:
        console.print(f"  [dim]Project:[/dim]     +{task.project}")
    if task.context:
        console.print(f"  [dim]Context:[/dim]     @{task.context}")
    if task.due_date:
        console.print(f"  [dim]Due:[/dim]         {task.due_date.strftime(date_format)}")
    console.print(f"  [dim]Created:[/dim]     {task.created_at}")
    console.print(f"  [dim]Updated:[/dim]     {task.updated_at}")


def print_task_created(task: Task) -> None:
    console.print(f"[green]Created[/green] task [{task.id[:10]}] {task.title!r}")


def print_task_updated(task: Task) -> None:
    console.print(f"[yellow]Updated[/yellow] task [{task.id[:10]}] {task.title!r}")


def print_task_deleted(task_id: str) -> None:
    console.print(f"[red]Deleted[/red] task [{task_id[:10]}]")


def print_task_completed(task: Task) -> None:
    console.print(f"[green]Completed[/green] task [{task.id[:10]}] {task.title!r}")
