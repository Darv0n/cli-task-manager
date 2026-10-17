---
description: |
  Use when the user wants to search for tasks, find a task by text,
  or says "search tasks", "find task", "look for task", "grep tasks", "search for".
  Examples: "search for deploy tasks", "find tasks mentioning API", "look for bug tasks"
---

# /search-tasks [query]

## What This Does
Full-text search across task titles, descriptions, and tags.

## Steps

1. **Extract query** -- get search terms from user message
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager search "QUERY"
   ```
3. **Format** -- Rich table output shows matching tasks. If empty, report "No tasks found."

## Memory
- Reads: none
- Writes: none
