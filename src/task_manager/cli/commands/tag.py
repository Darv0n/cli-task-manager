"""task tag — add or remove tags from a task."""

from __future__ import annotations

from typing import Optional

import typer

from task_manager.cli.commands.show import _resolve_task_id
from task_manager.cli.output import print_task_updated
from task_manager.models import Task
from task_manager.utils.time import utcnow_iso


def tag(
    ctx: typer.Context,
    task_id: str = typer.Argument(..., help="Task ID or prefix"),
    add: Optional[str] = typer.Option(None, "--add", "-a", help="Tags to add (comma-separated)"),
    remove: Optional[str] = typer.Option(
        None, "--remove", "-r", help="Tags to remove (comma-separated)"
    ),
) -> None:
    """Add or remove tags from a task."""
    from task_manager.errors import TaskManagerError
    from task_manager.storage import get_backend

    if not add and not remove:
        from task_manager.cli.output import console

        console.print("[yellow]Specify --add or --remove (or both).[/yellow]")
        raise typer.Exit(1)

    settings = ctx.obj["settings"]
    storage = get_backend(settings.storage_backend, data_dir=settings.data_dir)

    try:
        resolved_id = _resolve_task_id(storage, task_id)
        data = storage.get(resolved_id)
        current_tags = set(data.get("tags", []))

        if add:
            new_tags = {t.strip().lower() for t in add.split(",") if t.strip()}
            current_tags |= new_tags

        if remove:
            rm_tags = {t.strip().lower() for t in remove.split(",") if t.strip()}
            current_tags -= rm_tags

        updated_data = storage.update(
            resolved_id,
            {"tags": sorted(current_tags), "updated_at": utcnow_iso()},
        )
        task = Task.from_storage(updated_data)
        print_task_updated(task)
    except TaskManagerError as exc:
        from task_manager.cli.output import console

        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(exc.exit_code) from exc
