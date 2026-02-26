"""Root Typer application. Assembles all sub-commands."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from task_manager.config import Settings
from task_manager.errors import TaskManagerError

app = typer.Typer(
    name="task",
    help="Production CLI task manager.",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
)

err_console = Console(stderr=True)


@app.callback()
def main_callback(
    ctx: typer.Context,
    storage: Optional[str] = typer.Option(
        None,
        "--storage",
        "-s",
        help="Override storage backend (json|sqlite)",
        envvar="TASK_STORAGE_BACKEND",
    ),
    data_dir: Optional[Path] = typer.Option(
        None,
        "--data-dir",
        help="Override data directory",
        envvar="TASK_DATA_DIR",
    ),
    no_plugins: bool = typer.Option(False, "--no-plugins", help="Skip plugin loading"),
) -> None:
    """Global options applied to all commands."""
    settings = Settings.load()
    errors = settings.validate()
    if errors:
        for err in errors:
            err_console.print(f"[red]Config error:[/red] {err}")
        raise typer.Exit(30)

    # Override from CLI flags
    if storage or data_dir:
        from dataclasses import replace

        settings = replace(
            settings,
            **({"storage_backend": storage} if storage else {}),
            **({"data_dir": data_dir} if data_dir else {}),
        )

    # Ensure storage backends are registered
    import task_manager.storage.json_backend  # noqa: F401
    import task_manager.storage.sqlite_backend  # noqa: F401

    ctx.ensure_object(dict)
    ctx.obj["settings"] = settings
    ctx.obj["no_plugins"] = no_plugins

    # Load plugins
    if not no_plugins:
        from task_manager.plugins.hooks import DefaultHookRegistry
        from task_manager.plugins.loader import load_plugins

        hooks = DefaultHookRegistry()
        load_plugins(settings.plugins_dir, hooks)
        ctx.obj["hooks"] = hooks


# Register commands
from task_manager.cli.commands.add import add  # noqa: E402
from task_manager.cli.commands.complete import complete  # noqa: E402
from task_manager.cli.commands.config_cmd import config_app  # noqa: E402
from task_manager.cli.commands.delete import delete  # noqa: E402
from task_manager.cli.commands.list_ import list_tasks  # noqa: E402
from task_manager.cli.commands.search import search  # noqa: E402
from task_manager.cli.commands.show import show  # noqa: E402
from task_manager.cli.commands.tag import tag  # noqa: E402
from task_manager.cli.commands.update import update  # noqa: E402

app.command("add")(add)
app.command("list")(list_tasks)
app.command("show")(show)
app.command("update")(update)
app.command("delete")(delete)
app.command("complete")(complete)
app.command("tag")(tag)
app.command("search")(search)
app.add_typer(config_app, name="config")


def main() -> None:
    try:
        app()
    except TaskManagerError as exc:
        err_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(exc.exit_code) from exc
