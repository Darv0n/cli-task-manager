# cli-task-manager

Production-grade CLI task manager with pluggable storage backends and a plugin system.

## Install

```bash
python -m venv .venv
.venv/Scripts/activate  # Windows
pip install -e ".[dev]"
```

## Usage

```bash
task add "Buy groceries" --priority high --tags "shopping,errands" --due tomorrow
task list --status open
task show <id-prefix>
task complete <id-prefix>
task search "groceries"
task config show
```

## Storage Backends

- **json** (default) — single JSON file at `~/.task-manager/data/tasks.json`
- **sqlite** — SQLite database at `~/.task-manager/data/tasks.db`

Override with `--storage sqlite` or `TASK_STORAGE_BACKEND=sqlite`.

## Config

`~/.task-manager/config.toml`:

```toml
[storage]
backend = "json"

[display]
date_format = "%Y-%m-%d"
rich_output = true

default_priority = "medium"
```

## Plugins

Drop `.py` files into `~/.task-manager/plugins/`. Each must expose a `plugin` variable implementing the `Plugin` protocol.
