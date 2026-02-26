"""task delete — remove a task."""

from __future__ import annotations

import typer

from task_manager.cli.commands.show import _resolve_task_id
from task_manager.cli.output import print_task_deleted


def delete(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID or prefix"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Delete a task permanently."""
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

    if not force:
        data = storage.get(resolved_id)
        title = data["title"] if data else resolved_id
        confirm = typer.confirm(f"Delete task '{title}'?")
        if not confirm:
            raise typer.Abort()

    deleted = storage.delete(resolved_id)
    if deleted:
        hooks = ctx.obj.get("hooks")
        if hooks:
            from task_manager.contracts import HookEvent

            hooks.emit(HookEvent.TASK_DELETED, {"id": resolved_id})
        print_task_deleted(resolved_id)
    else:
        from task_manager.cli.output import console

        console.print(f"[red]Error:[/red] Task not found: {task_id!r}")
        raise typer.Exit(10)
