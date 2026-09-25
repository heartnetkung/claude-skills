#!/usr/bin/env bash
# Render an SVG to a PNG at 2x its declared width/height.
#   render.sh images/NAME.svg   ->   images/NAME.png
# Uses headless Chrome (best font handling); falls back to LibreOffice.
set -euo pipefail

[[ $# -eq 1 ]] || { echo "usage: render.sh FILE.svg" >&2; exit 2; }
svg="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
png="${svg%.svg}.png"

read -r w h < <(python3 - "$svg" <<'EOF'
import re, sys
head = open(sys.argv[1], encoding="utf-8").read(2000)
w = re.search(r'<svg[^>]*\swidth="(\d+)', head)
h = re.search(r'<svg[^>]*\sheight="(\d+)', head)
if not (w and h):
    sys.exit("error: the <svg> element needs numeric width and height attributes")
print(w.group(1), h.group(1))
EOF
)

chrome="$(command -v google-chrome || command -v chromium || command -v chromium-browser || true)"
if [[ -n "$chrome" ]]; then
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size="$w,$h" --screenshot="$png" "file://$svg" >/dev/null 2>&1
else
  profile="$(mktemp -d)"
  soffice "-env:UserInstallation=file://$profile" --headless --convert-to png \
    --outdir "$(dirname "$svg")" "$svg" >/dev/null 2>&1
  rm -rf "$profile"
fi
[[ -s "$png" ]] || { echo "error: rendering failed for $svg" >&2; exit 1; }
echo "rendered $png"
