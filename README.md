<h1 align="center">task</h1>

<p align="center">
  <strong>A production-grade CLI task manager that doesn't suck.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/storage-JSON_%7C_SQLite-4a90d9?style=flat-square" alt="Storage">
  <img src="https://img.shields.io/badge/tests-82_passing-2ea44f?style=flat-square" alt="Tests">
  <img src="https://img.shields.io/badge/lint-ruff-d4aa00?style=flat-square&logo=ruff&logoColor=white" alt="Ruff">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
</p>

<p align="center">
  Pluggable storage backends &bull; Plugin system &bull; TOML config &bull; Rich output &bull; Zero boilerplate
</p>

---

## Why This Exists

Every task manager CLI is either a toy tutorial project or an overengineered mess. This one is neither. It's a clean, extensible system with real architecture — the kind of thing you'd actually want to maintain.

- **Pluggable storage** — JSON by default, SQLite when you need it, your own backend when you want it
- **Plugin system** — drop a `.py` file in a directory and it loads. Hook into any lifecycle event
- **Prefix-matched IDs** — `task show 01K` just works. No copying full UUIDs
- **TOML config** — env vars > config file > defaults. Frozen after load. No surprise mutations
- **82 tests in 0.4s** — because untested code is a rough draft

## Quick Start

```bash
pip install -e ".[dev]"
```

```bash
task add "Refactor auth module" --priority high --tags "backend,security" --due tomorrow
task add "Update README" --project docs --context laptop
task add "Buy coffee" --priority urgent --due today

task list
task list --status open --priority high
task search "auth"
task show 01KJ          # prefix match
task complete 01KJ
task tag 01KJ --add "done,shipped" --remove "security"

task config show
task config backends
```

## Architecture

```
contracts.py ─── single source of truth (enums, protocols, type aliases)
     │
     ├── errors.py ─── structured hierarchy, exit codes per category
     ├── utils/ ────── ULID gen, ISO time, filter predicates
     │
     ├── models.py ─── Pydantic v2 Task (validates at parse, not storage)
     ├── config.py ─── frozen dataclass, TOML + env overlay
     │
     ├── storage/ ──── Protocol-based registry
     │    ├── json_backend.py ─── atomic writes (.tmp → replace)
     │    └── sqlite_backend.py ── WAL mode, indexed
     │
     ├── plugins/ ──── directory-based loader + isolated hook dispatch
     │
     └── cli/ ──────── Typer app, 9 commands, Rich output
```

**Key decisions:**

| What | Choice | Why |
|------|--------|-----|
| Types | `contracts.py` only | One file defines all types. Everything else imports. |
| Model | Pydantic v2 | Validate at the boundary, not in storage. Free serde. |
| Storage | `Protocol` | Structural subtyping — plugins don't import our code. |
| IDs | ULID (pure Python) | Time-sortable + prefix-matchable. Zero dependencies. |
| Config | `tomllib` stdlib | No deps. Human-writable. Immutable after construction. |
| Errors | Structural naming | `TaskNotFound`, not `TaskLookupError`. The name is the diagnosis. |

## Storage Backends

| Backend | File | Use case |
|---------|------|----------|
| `json` (default) | `~/.task-manager/data/tasks.json` | Simple, human-readable, git-friendly |
| `sqlite` | `~/.task-manager/data/tasks.db` | Indexed queries, better at scale |

```bash
task --storage sqlite add "Use the database"
# or
export TASK_STORAGE_BACKEND=sqlite
```

Writing your own backend is one class that implements `StorageBackend` protocol:

```python
from task_manager.storage import register_backend

class MyBackend:
    name = "my-backend"
    def get(self, task_id): ...
    def list(self, *, status=None, priority=None, tags=None, project=None, context=None): ...
    def create(self, data): ...
    def update(self, task_id, patch): ...
    def delete(self, task_id): ...
    def search(self, query): ...

register_backend("my-backend", MyBackend)
```

## Plugin System

Drop a `.py` file in `~/.task-manager/plugins/`. Done.

```python
# ~/.task-manager/plugins/slack_notify.py

class SlackNotifier:
    name = "slack-notify"
    version = "0.1.0"

    def register(self, hooks):
        hooks.on("task.completed", self._on_complete)

    def _on_complete(self, event, payload):
        # payload is a deep copy — mutate freely
        print(f"Task completed: {payload['title']}")

plugin = SlackNotifier()
```

**Available hooks:** `task.created`, `task.updated`, `task.deleted`, `task.completed`, `before.list`

Plugin crashes are caught and logged to stderr. They never break your workflow.

## Configuration

`~/.task-manager/config.toml`

```toml
[storage]
backend = "json"          # "json" | "sqlite" | custom backend name
data_dir = "~/.task-manager/data"

[display]
date_format = "%Y-%m-%d"
rich_output = true

default_priority = "medium"
plugins_dir = "~/.task-manager/plugins"
```

**Resolution order:** Environment variables > TOML file > Built-in defaults

| Env var | Overrides |
|---------|-----------|
| `TASK_STORAGE_BACKEND` | `storage.backend` |
| `TASK_DATA_DIR` | `storage.data_dir` |
| `TASK_DEFAULT_PRIORITY` | `default_priority` |
| `TASK_DATE_FORMAT` | `display.date_format` |
| `TASK_RICH_OUTPUT` | `display.rich_output` |
| `TASK_PLUGINS_DIR` | `plugins_dir` |

## Development

```bash
git clone https://github.com/Darv0n/cli-task-manager.git
cd cli-task-manager
python -m venv .venv && .venv/Scripts/activate
pip install -e ".[dev]"

# Test
pytest                     # 82 tests, ~0.4s

# Lint
ruff check src/ tests/
ruff format src/ tests/
```

**Test architecture:** Both storage backends run through an identical protocol compliance suite (`test_storage_protocol.py`). If you add a backend, it automatically gets tested against the same contract.

## License

[MIT](LICENSE)
