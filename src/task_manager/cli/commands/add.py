"""task add — create a new task."""

from __future__ import annotations

from typing import Optional

import typer

from task_manager.cli.output import print_task_created
from task_manager.cli.validators import parse_due_date
from task_manager.contracts import Priority
from task_manager.models import Task


def add(
    ctx: typer.Context,
    title: str = typer.Argument(..., help="Task title"),
    description: str = typer.Option("", "--desc", "-d", help="Task description"),
    priority: Priority = typer.Option(Priority.MEDIUM, "--priority", "-p"),
    tags: Optional[str] = typer.Option(None, "--tags", "-t", help="Comma-separated tags"),
    project: Optional[str] = typer.Option(None, "--project", help="Project name"),
    context: Optional[str] = typer.Option(None, "--context", help="Context name"),
    due: Optional[str] = typer.Option(None, "--due", help="Due date (YYYY-MM-DD or 'tomorrow')"),
) -> None:
    """Create a new task."""
    from task_manager.storage import get_backend

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    due_date = parse_due_date(due) if due else None

    task = Task(
        title=title,
        description=description,
        priority=priority,
        tags=tags.split(",") if tags else [],
        project=project,
        context=context,
        due_date=due_date,
    )

    storage.create(task.to_storage())

    hooks = ctx.obj.get("hooks")
    if hooks:
        from task_manager.contracts import HookEvent

        hooks.emit(HookEvent.TASK_CREATED, task.to_storage())

    print_task_created(task)
