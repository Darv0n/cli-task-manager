---
description: |
  Use when the user wants to tag a task, add a tag, remove a tag, label a task,
  or says "tag task", "add tag", "remove tag", "label task", "untag".
  Examples: "tag 01KJ with bug", "add tag 'frontend' to task 01KJ", "remove tag 'wip' from 01KJ"
---

# /tag-task [id] [--add/--remove tags]

## What This Does
Adds or removes tags from a task. Set operations: idempotent union (add) and difference (remove).

## Steps

1. **Parse input** -- extract task ID, operation (add/remove), and tag names
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager tag ID_PREFIX --add tag1,tag2
   .venv/Scripts/python.exe -m task_manager tag ID_PREFIX --remove tag1
   ```
3. **Confirm** -- report updated tag list

## Memory
- Reads: none
- Writes: none
