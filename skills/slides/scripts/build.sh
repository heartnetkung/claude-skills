#!/usr/bin/env bash
# Lint a Markdown deck, then build its .pptx with pandoc.
#   build.sh path/to/NAME-slides.md   ->   path/to/NAME.pptx
# Template: the deck folder's template.pptx if present, else its reference.pptx,
# else the skill's own assets/reference.pptx.
set -euo pipefail

[[ $# -eq 1 ]] || { echo "usage: build.sh DECK.md" >&2; exit 2; }
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
deck_dir="$(cd "$(dirname "$1")" && pwd)"
deck="$(basename "$1")"
name="${deck%.md}"
out="${name%-slides}.pptx"

ref="$here/../assets/reference.pptx"
[[ -f "$deck_dir/reference.pptx" ]] && ref="$deck_dir/reference.pptx"
[[ -f "$deck_dir/template.pptx" ]] && ref="$deck_dir/template.pptx"

python3 "$here/lint_deck.py" "$deck_dir/$deck"

cd "$deck_dir"
pandoc "$deck" -o "$out" --slide-level=3 --reference-doc="$ref"
echo "built $deck_dir/$out (template: $ref)"
