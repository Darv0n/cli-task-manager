---
description: |
  Use when the user wants to see their tasks, list tasks, filter tasks,
  or asks "what's open", "show my tasks", "tasks by priority", "filter tasks",
  "list tasks", "what do I need to do".
  Examples: "list all high priority tasks", "what's open?", "show tasks tagged bug"
---

# /list-tasks [filters]

## What This Does
Lists tasks with optional filters via the CLI. Renders a Rich table in the terminal.

## Steps

1. **Parse filters** from user message:
   - Status: `--status open` (open/in_progress/done/cancelled)
   - Priority: `--priority high` (low/medium/high/urgent)
   - Tags: `--tags "bug,frontend"` (AND logic -- must have all)
   - Project: `--project myproject`
   - Context: `--context work`
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager list [--status S] [--priority P] [--tags T] [--project P] [--context C]
   ```
3. **Format result** -- Rich table output is rendered directly. If empty, report "No tasks found."

## Memory
- Reads: none
- Writes: none
