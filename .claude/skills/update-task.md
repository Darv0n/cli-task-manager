---
description: |
  Use when the user wants to update a task, change status, edit a task,
  modify task fields, set priority, or says "update task", "change status",
  "edit task", "modify task", "set priority", "change due date".
  Examples: "set task 01KJ to in_progress", "change priority of 01KJ to urgent"
---

# /update-task [id] [fields]

## What This Does
Updates one or more fields on an existing task. Partial update -- only specified fields change.

## Steps

1. **Parse input** -- extract task ID/prefix and fields to change
   - `--title "new title"`, `--status in_progress`, `--priority urgent`
   - `--due "next week"`, `--project newproj`, `--context home`
   - `--description "more details"`
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager update ID [--title T] [--status S] [--priority P] ...
   ```
3. **Verify** -- confirm `updated_at` timestamp refreshed in output

## Memory
- Reads: none
- Writes: none
