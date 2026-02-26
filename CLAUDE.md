# cli-task-manager

Production-grade CLI task manager. Pluggable storage, plugin system, TOML config.

## Quick Reference

```bash
# Dev setup
.venv/Scripts/python.exe -m pip install -e ".[dev]"

# Run
.venv/Scripts/python.exe -m task_manager [command]

# Lint + test
.venv/Scripts/ruff.exe check src/ tests/
.venv/Scripts/ruff.exe format src/ tests/
.venv/Scripts/python.exe -m pytest tests/ -q
```

## Architecture

### Dependency Flow (strict — no cycles)

```
contracts.py          <- single source of truth: enums, protocols, type aliases
    |
errors.py             <- error hierarchy with structured exit codes
utils/                <- ids (ULID), time (ISO 8601), filters (predicates)
    |
models.py             <- Pydantic v2 Task model (imports contracts + utils)
config.py             <- frozen Settings dataclass (imports contracts)
    |
storage/              <- registry + JSON backend + SQLite backend
plugins/              <- hook registry + directory-based loader
    |
cli/                  <- Typer app, commands, output formatters, validators
```

### Load-Bearing Decisions

| Decision | Choice | Why it matters |
|----------|--------|----------------|
| Types | `contracts.py` is the only file that defines types | Single source of truth — everything else imports from here |
| Model | Pydantic v2 | Validation at parse time, not storage time. Free serialization. |
| Storage | `Protocol` (structural subtyping) | Plugins implement storage without importing our code |
| IDs | ULID (pure Python, `utils/ids.py`) | Time-sortable, prefix-matchable for CLI UX, zero deps |
| Config | `tomllib` (stdlib) + frozen dataclass | No deps. Env vars > TOML > defaults. Immutable after load. |
| Plugins | Directory-based (`~/.task-manager/plugins/*.py`) | Zero friction. Drop a file, it loads. |
| Errors | Named for structural cause, not symptom | `TaskNotFound` not `TaskLookupError`. Exit codes per category. |

### Storage Backends

Both backends implement `StorageBackend` Protocol from `contracts.py` and self-register via `register_backend()` at import time.

- **JSON** (`storage/json_backend.py`): Single file at `data_dir/tasks.json`. Atomic writes via `.tmp` + `replace()`.
- **SQLite** (`storage/sqlite_backend.py`): WAL mode, indexed on status/priority/project. Tags stored as JSON text.

### CLI Commands

`add`, `list`, `show`, `update`, `delete`, `complete`, `tag`, `search`, `config`

All commands resolve task IDs by prefix match (`task show 01KJ` works). Ambiguous prefixes raise `AmbiguousTaskId`.

### Plugin System

- `plugins/hooks.py`: `DefaultHookRegistry` — synchronous event bus. Handlers get a deepcopy of payload. Exceptions caught and logged to stderr.
- `plugins/loader.py`: Scans `plugins_dir/*.py`, looks for `plugin` variable implementing `Plugin` protocol.
- Hook events: `task.created`, `task.updated`, `task.deleted`, `task.completed`, `before.list`

## Conventions

- Python 3.11+ (uses `TypeAlias`, not `type` statement)
- ruff: line-length 100, select E/F/I/N/W, ignore N818
- Tests use `tmp_path` fixtures — never touch real `~/.task-manager/`
- CLI tests use `CliRunner` with `--data-dir` and `--no-plugins` for isolation
- Protocol compliance suite (`test_storage_protocol.py`) parametrizes both backends

## File Map

```
src/task_manager/
  __init__.py              # __version__
  __main__.py              # python -m entry
  contracts.py             # enums, protocols, type aliases
  models.py                # Task (Pydantic v2)
  config.py                # Settings + TOML loader
  errors.py                # error hierarchy
  cli/
    app.py                 # root Typer app + global options + command registration
    commands/{add,list_,show,update,delete,complete,tag,search,config_cmd}.py
    output.py              # Rich formatters (table + detail view)
    validators.py          # due date parsing (natural language + ISO)
  storage/
    __init__.py            # backend registry
    json_backend.py
    sqlite_backend.py
  plugins/
    hooks.py               # DefaultHookRegistry
    loader.py              # directory scanner + importlib
  utils/
    ids.py                 # ULID generation
    time.py                # utcnow_iso()
    filters.py             # apply_filters() shared by backends
tests/
  conftest.py              # fixtures: tmp dirs, sample tasks, backends
  test_models.py           # 15 tests: creation, tags, sigils, serialization
  test_ids.py              # ULID length, uniqueness, sortability, charset
  test_filters.py          # 8 tests: all filter combinations
  test_config.py           # defaults, env override, validation
  test_storage_json.py     # JSON backend CRUD + filters
  test_storage_sqlite.py   # SQLite backend CRUD + filters
  test_storage_protocol.py # both backends pass identical compliance suite
  test_cli_add.py          # CLI add command
  test_cli_list.py         # CLI list command
  test_plugins.py          # hook registry, isolation, loader
```
