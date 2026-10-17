#!/usr/bin/env bash
# PostToolUse hook: Run ruff check on edited files (advisory).
# Self-filtering: checks HOOK_TOOL_NAME internally.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))"  2>/dev/null)
[ -z "$TOOL" ] && TOOL="$HOOK_TOOL_NAME"

# Only care about Edit tool
[ "$TOOL" != "Edit" ] && exit 0

# Extract file path
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$FILE_PATH" ] && FILE_PATH=$(echo "$HOOK_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))"  2>/dev/null)

# Only care about src/ or tests/ files
echo "$FILE_PATH" | grep -qE "(src/|tests/)" || exit 0
echo "$FILE_PATH" | grep -q "\.py$" || exit 0

# Run ruff check on the specific file
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" 2>/dev/null || exit 0
RESULT=$(.venv/Scripts/ruff.exe check "$FILE_PATH" 2>&1)
if [ $? -ne 0 ]; then
  echo "[LINT] ruff violations found in $(basename "$FILE_PATH"):"
  echo "$RESULT" | head -10
fi

# Always exit 0 -- advisory, not blocking
exit 0
