#!/usr/bin/env bash
# PostToolUse hook: Run pytest after source edits (advisory).
# Self-filtering: checks HOOK_TOOL_NAME internally.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))"  2>/dev/null)
[ -z "$TOOL" ] && TOOL="$HOOK_TOOL_NAME"

# Only care about Edit tool
[ "$TOOL" != "Edit" ] && exit 0

# Extract file path
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$FILE_PATH" ] && FILE_PATH=$(echo "$HOOK_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))"  2>/dev/null)

# Only care about src/task_manager/ files (not test files -- avoid loop)
echo "$FILE_PATH" | grep -q "src/task_manager/" || exit 0

# Run quick test suite
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" 2>/dev/null || exit 0
RESULT=$(.venv/Scripts/python.exe -m pytest tests/ -q --tb=short 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  FAILED=$(echo "$RESULT" | grep -cE "FAILED")
  echo "[TEST] $FAILED test(s) failing after edit to $(basename "$FILE_PATH"):"
  echo "$RESULT" | grep -E "FAILED|ERROR" | head -5
fi

# Always exit 0 -- advisory, not blocking
exit 0
