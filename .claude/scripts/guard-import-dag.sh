#!/usr/bin/env bash
# PreToolUse hook: Block edits that introduce import DAG violations.
# Self-filtering: checks HOOK_TOOL_NAME internally.
#
# DAG (left may import from right, not vice versa):
#   cli -> plugins -> storage -> config -> models -> utils -> errors -> contracts
#
# Each module has a numeric rank. An import from a lower rank to a higher rank
# is a DAG violation.

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))"  2>/dev/null)
[ -z "$TOOL" ] && TOOL="$HOOK_TOOL_NAME"

# Only care about Edit tool
[ "$TOOL" != "Edit" ] && exit 0

# Extract file path
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$FILE_PATH" ] && FILE_PATH=$(echo "$HOOK_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))"  2>/dev/null)

# Only care about src/task_manager/ files
echo "$FILE_PATH" | grep -q "src/task_manager/" || exit 0
# Skip __init__.py and __main__.py
echo "$FILE_PATH" | grep -qE "__init__|__main__" && exit 0

# Extract new_string (the code being added)
NEW_STRING=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('new_string','') if isinstance(d.get('tool_input'),dict) else '')"  2>/dev/null)
[ -z "$NEW_STRING" ] && exit 0

# Determine the rank of the file being edited
get_rank() {
  case "$1" in
    *contracts*) echo 0 ;;
    *errors*)    echo 1 ;;
    *utils*)     echo 2 ;;
    *models*)    echo 3 ;;
    *config*)    echo 4 ;;
    *storage*)   echo 5 ;;
    *plugins*)   echo 6 ;;
    *cli*)       echo 7 ;;
    *)           echo 99 ;;
  esac
}

FILE_RANK=$(get_rank "$FILE_PATH")
[ "$FILE_RANK" = "99" ] && exit 0

# Check for imports in new_string that would violate the DAG
VIOLATIONS=""
for target in contracts errors utils models config storage plugins cli; do
  if echo "$NEW_STRING" | grep -qE "(from task_manager\.$target|from \.$target|import task_manager\.$target)"; then
    TARGET_RANK=$(get_rank "$target")
    if [ "$TARGET_RANK" -gt "$FILE_RANK" ]; then
      VIOLATIONS="$VIOLATIONS  - Importing '$target' (rank $TARGET_RANK) from a file at rank $FILE_RANK\n"
    fi
  fi
done

if [ -n "$VIOLATIONS" ]; then
  echo "[BLOCK] Import DAG violation detected. This edit would create a dependency cycle."
  echo "DAG: contracts(0) -> errors(1) -> utils(2) -> models(3) -> config(4) -> storage(5) -> plugins(6) -> cli(7)"
  echo "Violations:"
  echo -e "$VIOLATIONS"
  echo "Lower-ranked modules CANNOT import from higher-ranked modules."
  exit 1
fi

exit 0
