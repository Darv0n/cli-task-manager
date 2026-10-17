#!/usr/bin/env bash
# PreToolUse hook: Block deletion of core source modules.
# Self-filtering: checks HOOK_TOOL_NAME internally.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))"  2>/dev/null)
[ -z "$TOOL" ] && TOOL="$HOOK_TOOL_NAME"

# Only care about Bash tool
[ "$TOOL" != "Bash" ] && exit 0

# Extract command
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$COMMAND" ] && COMMAND=$(echo "$HOOK_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('command',''))"  2>/dev/null)

# Check if command contains rm and targets src/task_manager/
if echo "$COMMAND" | grep -qE "\brm\b" && echo "$COMMAND" | grep -q "src/task_manager/"; then
  echo "[BLOCK] Core module deletion blocked. Use redistribution, not removal. If you need to move functionality, create the destination first, then migrate."
  exit 1
fi

exit 0
