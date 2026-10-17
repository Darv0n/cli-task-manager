#!/usr/bin/env bash
# PreToolUse hook: Warn when editing contracts.py without reading it first.
# Self-filtering: checks HOOK_TOOL_NAME internally.

INPUT=$(cat)

# Extract tool name from stdin JSON or fall back to env var
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))"  2>/dev/null)
[ -z "$TOOL" ] && TOOL="$HOOK_TOOL_NAME"

# Only care about Edit tool
[ "$TOOL" != "Edit" ] && exit 0

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$FILE_PATH" ] && FILE_PATH=$(echo "$HOOK_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))"  2>/dev/null)

# Only care about contracts.py
echo "$FILE_PATH" | grep -q "contracts\.py" || exit 0

# Warn (exit 0 = advisory, not blocking)
echo "[GUARD] contracts.py is the single source of truth for all types, protocols, and enums. Read it before editing to understand the downstream impact on models, storage, plugins, and CLI."
exit 0
