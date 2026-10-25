#!/bin/bash
# Sets the left side of this session's status line to the ticket in progress.
# ~/.claude/statusline-command.sh reads ~/.claude/ticket-status/<session_id>:
# line 1 is the head it may shorten, line 2 the progress tail it always shows.
#   set-status.sh <ticket> "<name>" preparation   -> #<ticket> <name>: preparation
#   set-status.sh <ticket> "<name>" <i> <total>   -> #<ticket> <name>: PR <i>/<total>
set -euo pipefail

usage() { echo "usage: set-status.sh <ticket> \"<name>\" preparation | <ticket> \"<name>\" <i> <total>" >&2; exit 1; }

[ -n "${CLAUDE_CODE_SESSION_ID:-}" ] || { echo "CLAUDE_CODE_SESSION_ID is not set" >&2; exit 1; }
dir="$HOME/.claude/ticket-status"
file="$dir/$CLAUDE_CODE_SESSION_ID"
int='^[0-9]+$'

[[ "${1:-}" =~ $int ]] && [ -n "${2:-}" ] || usage
# One line, no backslashes: the status line prints the name through printf %b.
name=$(printf '%s' "$2" | tr '\n\\' ' /')
MAX_NAME=35
if [ ${#name} -gt $MAX_NAME ]; then
  name="${name:0:$((MAX_NAME - 1))}"
  name="${name%"${name##*[! ]}"}…"
fi
if [ "$#" -eq 3 ] && [ "$3" = preparation ]; then
  tail=": preparation"
elif [ "$#" -eq 4 ] && [[ "$3" =~ $int ]] && [[ "$4" =~ $int ]] && [ "$3" -ge 1 ] && [ "$3" -le "$4" ]; then
  tail=": PR $3/$4"
else
  usage
fi

mkdir -p "$dir"
# Nothing else deletes a session's file; no ticket session lasts a week.
find "$dir" -type f -mtime +7 -delete
printf '%s\n%s\n' "#$1 $name" "$tail" > "$file"
echo "status: #$1 $name$tail"
