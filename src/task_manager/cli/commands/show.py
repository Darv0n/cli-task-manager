"""task show — display a single task by ID or prefix."""

from __future__ import annotations

import typer

from task_manager.cli.output import print_task_detail
from task_manager.models import Task


def _resolve_task_id(storage: object, prefix: str) -> str:
    """Resolve a task ID prefix to a full ID. Raises on not found or ambiguous."""
    from task_manager.errors import AmbiguousTaskId, TaskNotFound

    # Try exact match first
    result = storage.get(prefix)
    if result is not None:
        return prefix

    # Prefix search
    all_tasks = storage.list()
    matches = [t["id"] for t in all_tasks if t["id"].startswith(prefix.upper())]

    if len(matches) == 0:
        raise TaskNotFound(prefix)
    if len(matches) == 1:
        return matches[0]
    raise AmbiguousTaskId(prefix, matches)


def show(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID or prefix"),
) -> None:
    """Show details of a single task."""
    from task_manager.errors import TaskManagerError
    from task_manager.storage import get_backend

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    try:
        resolved_id = _resolve_task_id(storage, task_id)
        data = storage.get(resolved_id)
        task = Task.from_storage(data)
        print_task_detail(task, date_format=settings.date_format)
    except TaskManagerError as exc:
        from task_manager.cli.output import console

        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(exc.exit_code) from exc
