---
description: |
  Use when the user wants to create a plugin, add a plugin, write a hook plugin,
  or says "create plugin", "add plugin", "write a hook plugin", "new integration",
  "plugin for X", "hook into task events".
  Examples: "create a GitHub issues plugin", "write a plugin that logs to Slack", "add a Todoist sync plugin"
---

# /add-plugin [plugin-name]

## What This Does
Spawns the plugin-architect agent to create a new plugin that hooks into task
lifecycle events.

## Steps

1. **Confirm scope** -- ask user what the plugin should do and which events to hook
   - Available events: `task.created`, `task.updated`, `task.deleted`, `task.completed`
2. **Load context** -- read these files for the agent:
   - `src/task_manager/contracts.py` -- Plugin protocol definition
   - `src/task_manager/plugins/hooks.py` -- hook event types, registry
   - `src/task_manager/plugins/loader.py` -- how plugins are discovered
3. **Spawn plugin-architect agent** (sonnet) with:
   - Plugin purpose and target events
   - Protocol definition
   - Hook registry API
4. **Verify outputs**:
   - [ ] Plugin file at `~/.task-manager/plugins/<name>.py`
   - [ ] Exposes `plugin` variable at module top level
   - [ ] `register(hooks)` wires handlers correctly
   - [ ] Plugin loads without crash
5. **Update memory** -- append to `feedback_cli-task-manager-plugins.md`

## Agents Spawned
- **plugin-architect** (sonnet) -- see `.claude/agents/plugin-architect.md`

## Memory
- Reads: `feedback_cli-task-manager-plugins.md` (prior plugin patterns)
- Writes: `feedback_cli-task-manager-plugins.md` (new plugin notes)
