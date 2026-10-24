#!/bin/bash
# Sets the left side of this session's status line to the ticket in progress.
# ~/.claude/statusline-command.sh reads ~/.claude/ticket-status/<session_id>.
#   set-status.sh <ticket> preparation   -> Ticket #<ticket>: preparation
#   set-status.sh <ticket> <i> <total>   -> Ticket #<ticket>: PR <i>/<total>
#   set-status.sh clear                  -> back to folder@branch
set -euo pipefail

usage() { echo "usage: set-status.sh <ticket> preparation | <ticket> <i> <total> | clear" >&2; exit 1; }

[ -n "${CLAUDE_CODE_SESSION_ID:-}" ] || { echo "CLAUDE_CODE_SESSION_ID is not set" >&2; exit 1; }
dir="$HOME/.claude/ticket-status"
file="$dir/$CLAUDE_CODE_SESSION_ID"
int='^[0-9]+$'

if [ "$#" -eq 1 ] && [ "$1" = clear ]; then
  rm -f "$file"
  echo "status cleared"
  exit 0
fi

[[ "${1:-}" =~ $int ]] || usage
if [ "$#" -eq 2 ] && [ "$2" = preparation ]; then
  text="Ticket #$1: preparation"
elif [ "$#" -eq 3 ] && [[ "$2" =~ $int ]] && [[ "$3" =~ $int ]] && [ "$2" -ge 1 ] && [ "$2" -le "$3" ]; then
  text="Ticket #$1: PR $2/$3"
else
  usage
fi

mkdir -p "$dir"
printf '%s' "$text" > "$file"
echo "status: $text"
