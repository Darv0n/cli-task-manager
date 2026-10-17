---
description: |
  Use when the user wants to create a new storage backend, add a backend,
  or says "add storage backend", "create backend", "new backend for X",
  "implement a backend", "storage for postgres", "redis backend".
  Examples: "create a Redis storage backend", "add a PostgreSQL backend", "new backend for S3"
---

# /add-backend [backend-name]

## What This Does
Spawns the backend-architect agent to create a new storage backend that implements
the full `StorageBackend` Protocol from `contracts.py`.

## Steps

1. **Confirm scope** -- ask user what storage system the backend targets
2. **Load context** -- read these files for the agent:
   - `src/task_manager/contracts.py` -- Protocol definition (7 methods)
   - `src/task_manager/storage/json_backend.py` -- reference implementation
   - `src/task_manager/storage/__init__.py` -- registration pattern
   - `tests/test_storage_protocol.py` -- compliance test suite
3. **Spawn backend-architect agent** (opus) with:
   - Target storage system name
   - Protocol definition
   - Registration pattern
   - Test patterns
4. **Verify outputs**:
   - [ ] New backend file in `src/task_manager/storage/`
   - [ ] All 7 Protocol methods implemented
   - [ ] Self-registration via `register_backend()`
   - [ ] Tests pass: `pytest tests/test_storage_protocol.py -q`
5. **Update memory** -- append to `feedback_cli-task-manager-backends.md`

## Agents Spawned
- **backend-architect** (opus) -- see `.claude/agents/backend-architect.md`

## Memory
- Reads: `feedback_cli-task-manager-backends.md` (prior backend patterns)
- Writes: `feedback_cli-task-manager-backends.md` (new backend notes)
