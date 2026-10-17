# cli-task-manager

Production CLI task manager. Pluggable storage, plugin system, TOML config.

## Quick Reference

```bash
.venv/Scripts/python.exe -m task_manager [command]        # run
.venv/Scripts/ruff.exe check src/ tests/                  # lint
.venv/Scripts/ruff.exe format src/ tests/                 # format
.venv/Scripts/python.exe -m pytest tests/ -q              # test (82, 0.4s)
```

## Architecture

### Dependency DAG (strict -- NEVER import upward)

```
contracts.py  <- enums, protocols, type aliases (SINGLE SOURCE OF TRUTH)
    |
errors.py     <- error hierarchy, structured exit codes
utils/        <- ids (ULID), time (ISO 8601), filters
    |
models.py     <- Pydantic v2 Task model
config.py     <- frozen Settings dataclass
    |
storage/      <- registry + JSON + SQLite backends
plugins/      <- hook registry + directory loader
    |
cli/          <- Typer app, commands, formatters
```

### Task Lifecycle

```
OPEN --update--> IN_PROGRESS --complete--> DONE
  |                   |
  +----cancel---------+----cancel----> CANCELLED
  |
  +----complete--> DONE
```

No transition enforcement (V1). Any status reachable via `update --status`.
`complete` = sugar for `update --status=done`. `delete` removes from any state.

### Load-Bearing Decisions

| Decision | Choice | Constraint |
|----------|--------|------------|
| Types | `contracts.py` only | Everything imports from here |
| Storage | `Protocol` (structural subtyping) | 7 methods, self-registering |
| IDs | ULID (pure Python) | Time-sorted, prefix-matchable |
| Config | `tomllib` + frozen dataclass | env > TOML > defaults, immutable |
| Plugins | `~/.task-manager/plugins/*.py` | Expose `plugin` var, `register(hooks)` |
| Errors | Named for structural cause | `TaskNotFound` not `TaskLookupError` |

## CLI Commands

`add`, `list`, `show`, `update`, `delete`, `complete`, `tag`, `search`, `config`

Prefix resolution: `task show 01KJ` works. Ambiguous = `AmbiguousTaskId`.
Delete in agent context: always pass `--force` (no interactive prompt).

## Storage Backends

- **JSON**: `data_dir/tasks.json`. Atomic writes (`.tmp` + `replace()`).
- **SQLite**: WAL mode, indexed status/priority/project. Tags as JSON text.

New backends: implement all 7 `StorageBackend` Protocol methods + `register_backend()`.

## Plugin System

- `hooks.py`: Sync event bus. Handlers get deepcopy. Exceptions caught/logged.
- `loader.py`: Scans `plugins_dir/*.py` for `plugin` var implementing `Plugin` protocol.
- Events: `task.created`, `task.updated`, `task.deleted`, `task.completed`, `before.list`

## Conventions

- Python 3.11+, ruff (E/F/I/N/W, line-length 100, ignore N818)
- Tests: `tmp_path` fixtures, `--data-dir` + `--no-plugins` for CLI isolation
- Protocol compliance: `test_storage_protocol.py` parametrizes both backends

## Skills & Agents

Skills: `/add-task`, `/list-tasks`, `/show-task`, `/update-task`, `/complete-task`,
`/tag-task`, `/search-tasks`, `/delete-task`, `/task-config`, `/sync-github`,
`/add-backend`, `/add-plugin`, `/task-dashboard`, `/run-checks`

Agents: `backend-architect` (opus), `plugin-architect` (sonnet),
`github-sync-agent` (sonnet), `test-author` (sonnet),
`code-reviewer` (sonnet), `integration-scout` (haiku)

## Hooks

PreToolUse: contracts.py edit guard, import DAG guard, core module delete guard
PostToolUse: lint gate, test gate, Protocol compliance gate
PostToolUseFailure: test failure parser
UserPromptSubmit: task intent router
Stop: session learning capture
