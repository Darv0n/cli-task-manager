"""task config — view and modify configuration."""

from __future__ import annotations

import typer

from task_manager.cli.output import console

config_app = typer.Typer(help="View and modify configuration.")


@config_app.command("show")
def config_show(ctx: typer.Context) -> None:
    """Show current configuration."""
    from dataclasses import asdict

    settings = ctx.obj["settings"]
    for key, value in asdict(settings).items():
        console.print(f"  [dim]{key}:[/dim] {value}")


@config_app.command("path")
def config_path(ctx: typer.Context) -> None:
    """Show config file path."""
    from task_manager.config import CONFIG_DIR, CONFIG_FILE

    console.print(f"  [dim]Config dir:[/dim]  {CONFIG_DIR}")
    console.print(f"  [dim]Config file:[/dim] {CONFIG_FILE}")
    console.print(f"  [dim]Data dir:[/dim]    {ctx.obj['settings'].data_dir}")
    console.print(f"  [dim]Plugins dir:[/dim] {ctx.obj['settings'].plugins_dir}")


@config_app.command("backends")
def config_backends(ctx: typer.Context) -> None:
    """List available storage backends."""
    from task_manager.storage import available_backends

    backends = available_backends()
    current = ctx.obj["settings"].storage_backend
    for name in backends:
        marker = " [green](active)[/green]" if name == current else ""
        console.print(f"  {name}{marker}")
