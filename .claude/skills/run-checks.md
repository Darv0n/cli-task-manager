---
description: |
  Use when the user wants to run quality checks, verify code, lint and test,
  or says "run checks", "verify", "lint and test", "pre-commit", "check everything",
  "make sure it's clean", "quality gate".
  Examples: "run checks", "lint and test the project", "verify everything passes"
---

# /run-checks

## What This Does
Runs the full quality pipeline: ruff check, ruff format, pytest.

## Steps

1. **Lint**:
   ```bash
   .venv/Scripts/python.exe -m ruff check src/ tests/
   ```
2. **Format check**:
   ```bash
   .venv/Scripts/python.exe -m ruff format --check src/ tests/
   ```
3. **Test**:
   ```bash
   .venv/Scripts/python.exe -m pytest tests/ -q
   ```
4. **Report** -- summarize results:
   - Lint: N violations or clean
   - Format: N files need formatting or clean
   - Tests: N passed, N failed, time

## Memory
- Reads: none
- Writes: none

## Quality Gates
- [ ] Zero ruff violations
- [ ] All files formatted
- [ ] All 82+ tests pass
- [ ] Suite completes in < 2s
