#!/usr/bin/env bash
# Remove a pushed PR branch's worktree and local branch, once nothing on them is missing from
# origin, and clear the session's status line. Run from outside that worktree.
# With <ticket>, given on the ticket's last PR, also remove the ticket's WIP label.
# Usage: cleanup.sh <branch> [<ticket>]
set -euo pipefail

branch=${1:?usage: cleanup.sh <branch> [<ticket>]}
ticket=${2:-}

wt=$(git worktree list --porcelain | awk -v b="branch refs/heads/$branch" '
  /^worktree / { path = substr($0, 10) }
  $0 == b      { print path }')
echo "branch: $branch"
echo "worktree: ${wt:-none}"

if [ -n "$wt" ]; then
  if [ "$(cd "$wt" && pwd -P)" = "$(git rev-parse --show-toplevel)" ]; then
    echo "error: run from outside $wt (ExitWorktree with keep first)" >&2
    exit 1
  fi
  dirty=$(git -C "$wt" status --porcelain)
  if [ -n "$dirty" ]; then
    echo "error: $wt has uncommitted or untracked files:" >&2
    echo "$dirty" >&2
    exit 1
  fi
fi

if ! git fetch --quiet origin "$branch"; then
  echo "error: origin has no branch $branch; push it first" >&2
  exit 1
fi
unpushed=$(git log --oneline "origin/$branch..$branch")
if [ -n "$unpushed" ]; then
  echo "error: $branch has commits not on origin:" >&2
  echo "$unpushed" >&2
  exit 1
fi
echo "origin/$branch has every commit of $branch"

if [ -n "$wt" ]; then
  git worktree remove "$wt"
  echo "removed worktree $wt"
fi
git branch -D "$branch"
if [ -n "$ticket" ]; then
  gh issue edit "$ticket" --remove-label WIP
  echo "removed WIP from #$ticket"
fi
bash "$(dirname "$0")/../start-ticket/set-status.sh" clear
