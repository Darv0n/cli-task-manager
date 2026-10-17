---
description: |
  Use when the user wants to delete a task, remove a task, drop a task,
  or says "delete task", "remove task", "drop task", "kill task", "trash task".
  Examples: "delete task 01KJ", "remove the old deploy task", "drop 01KJ"
---

# /delete-task [id]

## What This Does
Permanently removes a task from storage.

## Steps

1. **Extract ID** -- get task ID or prefix from user message
2. **Confirm intent** -- use AskUserQuestion: "Delete task 'TITLE' (ID)? This is permanent."
3. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager delete ID_PREFIX --force
   ```
   Always pass `--force` -- no interactive prompt in agent context.
4. **Confirm** -- report deletion

## Memory
- Reads: none
- Writes: none

## Safety
- Always confirm with user before executing
- `--force` is required in agent context (no stdin for interactive prompt)
