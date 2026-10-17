---
description: |
  Use when the user wants to see task manager configuration, check settings,
  or says "show config", "task config", "which backend", "settings", "config path",
  "what backend", "list backends".
  Examples: "show the current config", "which storage backend am I using?", "where is my config?"
---

# /task-config [subcommand]

## What This Does
Displays current configuration state: active settings, config file path, or available backends.

## Steps

1. **Determine subcommand** from user intent:
   - General settings: `config show`
   - Config file location: `config path`
   - Available backends: `config backends`
2. **Execute CLI command**:
   ```bash
   .venv/Scripts/python.exe -m task_manager config show
   .venv/Scripts/python.exe -m task_manager config path
   .venv/Scripts/python.exe -m task_manager config backends
   ```

## Memory
- Reads: none
- Writes: none
