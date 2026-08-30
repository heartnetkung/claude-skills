#!/usr/bin/env bash
# Files the one issue this skill produces. The title prefix is fixed so the dedupe below can
# find it again — freehand titles are what make duplicates. Matching is done client-side on
# purpose: `--search` reads an index that lags issue creation by seconds, so two runs close
# together both miss and both file.
set -euo pipefail

total=${1:-}
[ -n "$total" ] || {
	echo "usage: file-issue.sh <suite total, e.g. 18.2s>" >&2
	exit 2
}

existing=$(gh issue list --state open --label maintenance --json url,title \
	--jq '[.[] | select(.title | startswith("pytest runtime:"))][0].url // empty')
[ -z "$existing" ] || {
	echo "already filed: $existing"
	exit 0
}

gh issue create --label maintenance \
	--title "pytest runtime: $total exceeds the 15s threshold" \
	--body "Observed mid-task. Run \`uv run pytest --durations=15\` for the breakdown."
