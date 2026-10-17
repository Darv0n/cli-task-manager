#!/usr/bin/env bash
# PostToolUse hook: Run protocol compliance tests after storage edits (advisory).
# Self-filtering: checks HOOK_TOOL_NAME internally.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))"  2>/dev/null)
[ -z "$TOOL" ] && TOOL="$HOOK_TOOL_NAME"

# Only care about Edit tool
[ "$TOOL" != "Edit" ] && exit 0

# Extract file path
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$FILE_PATH" ] && FILE_PATH=$(echo "$HOOK_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))"  2>/dev/null)

# Only care about storage/ files
echo "$FILE_PATH" | grep -q "storage/" || exit 0

# Run protocol compliance suite
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" 2>/dev/null || exit 0
RESULT=$(.venv/Scripts/python.exe -m pytest tests/test_storage_protocol.py -q --tb=short 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "[PROTOCOL] StorageBackend Protocol compliance test failed after edit to $(basename "$FILE_PATH"):"
  echo "$RESULT" | grep -E "FAILED|ERROR" | head -5
else
  echo "[PROTOCOL] All Protocol compliance tests pass."
fi

# Always exit 0 -- advisory, not blocking
exit 0
