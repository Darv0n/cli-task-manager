"""task list — list tasks with filters."""

from __future__ import annotations

from typing import Optional

import typer

from task_manager.cli.output import print_task_list
from task_manager.models import Task


def list_tasks(
    ctx: typer.Context,
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status (comma-separated)"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", "-p", help="Filter by priority (comma-separated)"
    ),
    tags: Optional[str] = typer.Option(
        None, "--tags", "-t", help="Filter by tags (comma-separated, all must match)"
    ),
    project: Optional[str] = typer.Option(None, "--project", help="Filter by project"),
    context: Optional[str] = typer.Option(None, "--context", help="Filter by context"),
) -> None:
    """List tasks with optional filters."""
    from task_manager.storage import get_backend

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    results = storage.list(
        status=status.split(",") if status else None,
        priority=priority.split(",") if priority else None,
        tags=tags.split(",") if tags else None,
        project=project,
        context=context,
    )

    tasks = [Task.from_storage(r) for r in results]
    print_task_list(tasks, date_format=settings.date_format)
