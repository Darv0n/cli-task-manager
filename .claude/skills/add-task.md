---
description: |
  Use when the user wants to create a new task, add a task, capture something,
  or says "new task", "task add", "add a task", "create task", "capture this".
  Examples: "add a task to fix the login bug", "new task: review PR", "capture deploy step"
---

# /add-task [title] [options]

## What This Does
Creates a new task via the CLI with optional metadata (priority, tags, project, context, due date).

## Steps

1. **Parse input** -- extract title and optional flags from user message
   - Priority: `--priority high` (low/medium/high/urgent, default: medium)
   - Tags: `--tags "bug,frontend"` (comma-separated, auto-lowercased)
   - Project: `--project myproject` (sigil `+` stripped automatically)
   - Context: `--context work` (sigil `@` stripped automatically)
   - Due date: `--due "2026-04-10"` or `--due "next friday"` (natural language supported)
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager add "TITLE" [--priority P] [--tags T] [--project P] [--context C] [--due D]
   ```
3. **Verify** -- confirm the Rich output shows the new task with a ULID
4. **Report** -- show the created task ID and details

## Memory
- Reads: none
- Writes: none (task data persists via storage backend)

## Quality Gates
- [ ] Title is provided and non-empty
- [ ] Priority value is valid if specified
- [ ] Due date parses without error
