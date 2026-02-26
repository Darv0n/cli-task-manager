"""task complete — mark a task as done."""

from __future__ import annotations

import typer

from task_manager.cli.commands.show import _resolve_task_id
from task_manager.cli.output import print_task_completed
from task_manager.contracts import Status
from task_manager.models import Task
from task_manager.utils.time import utcnow_iso


def complete(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID or prefix"),
) -> None:
    """Mark a task as done."""
    from task_manager.errors import TaskManagerError
    from task_manager.storage import get_backend

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    try:
        resolved_id = _resolve_task_id(storage, task_id)
        updated_data = storage.update(
            resolved_id,
            {"status": Status.DONE.value, "updated_at": utcnow_iso()},
        )
        task = Task.from_storage(updated_data)

        hooks = ctx.obj.get("hooks")
        if hooks:
            from task_manager.contracts import HookEvent

            hooks.emit(HookEvent.TASK_COMPLETED, task.to_storage())

        print_task_completed(task)
    except TaskManagerError as exc:
        from task_manager.cli.output import console

        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(exc.exit_code) from exc
