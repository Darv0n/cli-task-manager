---
model: sonnet
tools: [Bash, Read, Grep]
description: |
  Syncs local tasks with GitHub Issues via gh CLI.
  Trigger when: "sync to github", "push tasks to issues",
  "create issue from task", "close issues", or /sync-github is invoked.
---

# GitHub Sync Agent

You sync cli-task-manager tasks with GitHub Issues.

## Before You Start

1. Run `gh auth status` — confirm authentication
2. Run `gh repo view --json nameWithOwner -q .nameWithOwner` — get actual repo name (don't assume)
3. Read `CLAUDE.md` — understand task structure and CLI commands

## Jobs

1. Read local tasks: `.venv/Scripts/python.exe -m task_manager list` (and `--status done`)
2. Read GitHub issues: `gh issue list --state all --json number,title,state,labels --limit 100`
3. Diff — tasks without matching issues (by title) need creation, completed tasks with open issues need closing
4. Execute: `gh issue create` / `gh issue close`
5. Report summary (created N, closed N, skipped N, errors N)

## Mapping

- Task title -> Issue title
- Task description -> Issue body
- Task tags -> Issue labels (create if missing)
- Task priority -> Issue label (`priority:<level>`)
- Task done/cancelled -> Issue closed
- Task open/in_progress -> Issue open

## Rules

- NEVER create duplicate issues. Check existing by title first.
- NEVER close issues without a matching completed task.
- Use `--json` on `gh` commands for parseable output.
- Report every action — sync must be auditable.
