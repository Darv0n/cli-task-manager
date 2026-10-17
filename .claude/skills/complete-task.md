---
description: |
  Use when the user wants to complete a task, mark a task as done, finish a task,
  or says "complete task", "mark done", "finish task", "close task", "done with task".
  Examples: "mark 01KJ as done", "complete the deploy task", "finish task 01KJ"
---

# /complete-task [id]

## What This Does
Marks a task as done. Sugar for `update --status done`.

## Steps

1. **Extract ID** -- get task ID or prefix from user message
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager complete ID_PREFIX
   ```
3. **Confirm** -- report task title and completion status

## Memory
- Reads: none
- Writes: none
