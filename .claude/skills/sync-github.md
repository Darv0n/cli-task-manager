---
description: |
  Use when the user wants to sync tasks with GitHub Issues, push tasks to GitHub,
  create issues from tasks, or says "sync to github", "push tasks to issues",
  "create github issue from task", "close issue", "github sync".
  Examples: "sync my tasks to GitHub", "create a GitHub issue for task 01KJ", "close the issue for completed tasks"
---

# /sync-github

## What This Does
Spawns the github-sync-agent to synchronize local tasks with GitHub Issues using
the `gh` CLI (already installed).

## Steps

1. **Verify prerequisites**:
   ```bash
   gh auth status
   gh repo view --json nameWithOwner
   ```
2. **Spawn github-sync-agent** (sonnet) with:
   - Repository: `Darv0n/cli-task-manager`
   - Sync direction requested (push new, close completed, or full sync)
3. **Agent will**:
   - Read task list via CLI
   - Map tasks to GitHub issues via `gh issue list`
   - Create missing issues via `gh issue create`
   - Close issues for completed tasks via `gh issue close`
   - Report sync summary
4. **Review sync report** -- verify counts match expectations
5. **Update memory** -- append to `project_cli-task-manager-integrations.md`

## Agents Spawned
- **github-sync-agent** (sonnet) -- see `.claude/agents/github-sync-agent.md`

## Memory
- Reads: `project_cli-task-manager-integrations.md`, `reference_cli-task-manager-repo.md`
- Writes: `project_cli-task-manager-integrations.md` (sync results)
