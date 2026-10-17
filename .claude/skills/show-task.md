---
description: |
  Use when the user wants to see details of a specific task, inspect a task,
  or says "show task", "task details", "inspect task", "view task".
  Examples: "show task 01KJ", "what's the status of the deploy task", "inspect 01KJ"
---

# /show-task [id-prefix]

## What This Does
Shows full details of a single task by ID or prefix match.

## Steps

1. **Extract ID** -- get task ID or prefix from user message
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager show ID_PREFIX
   ```
3. **Handle errors** -- prefix matches 0 tasks = `TaskNotFound`, 2+ tasks = `AmbiguousTaskId`

## Memory
- Reads: none
- Writes: none
