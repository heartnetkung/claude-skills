#!/usr/bin/env bash
# The whole edit loop in one call: build (lint + pandoc) → check → reload.
#   loop.sh DECK_DIR/NAME-slides.md [--png OUT_DIR]
# A lint or build error stops before anything is shown. A check error still reloads,
# so the user sees the overflowing slide; the exit code is then 1.
set -uo pipefail

[[ $# -ge 1 ]] || { echo "usage: loop.sh DECK.md [--png OUT_DIR]" >&2; exit 2; }
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
md="$1"; shift
name="$(basename "${md%.md}")"
pptx="$(cd "$(dirname "$md")" && pwd)/${name%-slides}.pptx"

"$here/build.sh" "$md" || exit 1
/usr/bin/python3 "$here/check.py" "$pptx" "$@"; status=$?
/usr/bin/python3 "$here/reload.py" "$pptx" || status=1
exit $status
