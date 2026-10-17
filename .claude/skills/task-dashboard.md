---
description: |
  Use when the user wants a task overview, triage view, daily review,
  or says "dashboard", "task overview", "what should I work on", "triage",
  "daily review", "status report", "what's on my plate".
  Examples: "give me a dashboard", "what should I work on next?", "daily triage"
---

# /task-dashboard

## What This Does
Builds a comprehensive overview: open tasks by priority, in-progress work, overdue items,
and suggests what to work on next.

## Steps

1. **Gather data** -- run multiple CLI queries:
   ```bash
   .venv/Scripts/python.exe -m task_manager list --status open
   .venv/Scripts/python.exe -m task_manager list --status in_progress
   .venv/Scripts/python.exe -m task_manager config show
   ```
2. **Analyze** -- from the output, identify:
   - Total open tasks, grouped by priority (urgent > high > medium > low)
   - Currently in-progress tasks
   - Tasks with due dates approaching or past due
   - Tasks by project/context distribution
3. **Format dashboard** -- present as structured summary:
   ```
   ## In Progress (N)
   - [task summaries]

   ## Urgent / High Priority (N)
   - [task summaries]

   ## Overdue (N)
   - [task summaries with due dates]

   ## Suggested Next
   - [highest priority unstarted task]
   ```
4. **Suggest action** -- recommend which task to start or complete next

## Memory
- Reads: none
- Writes: none
