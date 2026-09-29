#!/usr/bin/env bash
# Screenshot a state of the running prototype with headless Chrome.
# Usage: shot.sh <out.png> "<url query, e.g. page=a&preset=mature&panel=0>" [width=1500] [height=1000] [base=http://localhost:5173/]
set -euo pipefail
out="$1"; query="${2:-}"; w="${3:-1500}"; h="${4:-1000}"; base="${5:-http://localhost:5173/}"
chrome="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || true)"
if [ -z "$chrome" ] && [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
fi
[ -n "$chrome" ] || { echo "No Chrome/Chromium found" >&2; exit 1; }
mkdir -p "$(dirname "$out")"
timeout 40 "$chrome" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size="$w,$h" --virtual-time-budget=5000 \
  --screenshot="$out" "${base}?${query}" 2>/dev/null
echo "$out"
