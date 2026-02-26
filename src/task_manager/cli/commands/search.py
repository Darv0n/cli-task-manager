"""task search — full-text search across tasks."""

from __future__ import annotations

import typer

from task_manager.cli.output import print_task_list
from task_manager.models import Task


def search(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search query (matches title, description, tags)"),
) -> None:
    """Search tasks by title, description, or tags."""
    from task_manager.storage import get_backend

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    results = storage.search(query)
    tasks = [Task.from_storage(r) for r in results]
    print_task_list(tasks, date_format=settings.date_format)
