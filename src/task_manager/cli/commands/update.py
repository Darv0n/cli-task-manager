"""task update — modify an existing task."""

from __future__ import annotations

from typing import Optional

import typer

from task_manager.cli.commands.show import _resolve_task_id
from task_manager.cli.output import print_task_updated
from task_manager.contracts import Priority, Status
from task_manager.models import Task
from task_manager.utils.time import utcnow_iso


def update(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID or prefix"),
    title: Optional[str] = typer.Option(None, "--title", help="New title"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="New description"),
    status: Optional[Status] = typer.Option(None, "--status", "-s"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p"),
    project: Optional[str] = typer.Option(None, "--project", help="New project"),
    context: Optional[str] = typer.Option(None, "--context", help="New context"),
    due: Optional[str] = typer.Option(None, "--due", help="New due date"),
) -> None:
    """Update fields of an existing task."""
    from task_manager.errors import TaskManagerError
    from task_manager.storage import get_backend

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    try:
        resolved_id = _resolve_task_id(storage, task_id)
    except TaskManagerError as exc:
        from task_manager.cli.output import console

        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(exc.exit_code) from exc

    patch: dict = {"updated_at": utcnow_iso()}
    if title is not None:
        patch["title"] = title
    if description is not None:
        patch["description"] = description
    if status is not None:
        patch["status"] = status.value
    if priority is not None:
        patch["priority"] = priority.value
    if project is not None:
        patch["project"] = project.lstrip("+").strip() or None
    if context is not None:
        patch["context"] = context.lstrip("@").strip() or None
    if due is not None:
        from task_manager.cli.validators import parse_due_date

        patch["due_date"] = parse_due_date(due).isoformat()

    try:
        updated_data = storage.update(resolved_id, patch)
        task = Task.from_storage(updated_data)

        hooks = ctx.obj.get("hooks")
        if hooks:
            from task_manager.contracts import HookEvent

            hooks.emit(HookEvent.TASK_UPDATED, task.to_storage())

        print_task_updated(task)
    except TaskManagerError as exc:
        from task_manager.cli.output import console

        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(exc.exit_code) from exc
