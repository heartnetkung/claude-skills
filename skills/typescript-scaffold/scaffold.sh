#!/usr/bin/env bash
# Copies the frozen assets for one scope into a target directory.
#
#   scaffold.sh <fullstack|back|front|script> <target-dir> <project> [<npm-scope>]
#               [--ci] [--package <name>]...
#   scaffold.sh package <target-dir> <name> <npm-scope>
#
# --package adds an empty packages/<name>/ to a workspace scope. The second form adds one to a
# project scaffolded earlier.
# A file or directory named dot-<name> lands as .<name>. {{PROJECT}} and {{SCOPE}} are
# substituted in every copied file. Refuses to overwrite: if any file it would write already
# exists, it lists them and writes nothing.
set -euo pipefail

ASSETS="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)/assets"

ci=false
args=()
packages=()
while [ $# -gt 0 ]; do
  case "$1" in
    --ci) ci=true ;;
    --package) shift; packages+=("${1:?--package needs a name}") ;;
    *) args+=("$1") ;;
  esac
  shift
done
kind=${args[0]:-}
target=${args[1]:-}
project=${args[2]:-}
scope=${args[3]:-}

usage() {
  sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' >&2
  exit 2
}
[ -n "$kind" ] && [ -n "$target" ] && [ -n "$project" ] || usage

# "<asset dir>:<path under target>" pairs, applied in order; later ones overlay earlier ones.
case "$kind" in
  fullstack)
    parts="shared:. workspace:. root-fullstack:. interface:packages/interface server:apps/server
           web:apps/web web-fullstack:apps/web e2e:e2e e2e-fullstack:e2e" ;;
  back)
    parts="shared:. workspace:. root-back:. interface:packages/interface server:apps/server" ;;
  front)
    parts="shared:. workspace:. root-front:. web:apps/web web-front:apps/web e2e:e2e e2e-front:e2e" ;;
  script)
    parts="shared:. root-script:." ;;
  package)
    parts=""
    packages+=("$project") ;;
  *) usage ;;
esac
if [ "$kind" != script ] && [ -z "$scope" ]; then
  echo "scope '$kind' needs an npm scope (the <npm-scope> in @<npm-scope>/server)" >&2
  exit 2
fi

stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

for part in $parts; do
  mkdir -p "$stage/${part#*:}"
  cp -R "$ASSETS/${part%%:*}/." "$stage/${part#*:}/"
done
if [ "$kind" = script ] && [ ${#packages[@]} -gt 0 ]; then
  echo "scope 'script' is one flat package; it takes no --package" >&2
  exit 2
fi
for name in ${packages[@]+"${packages[@]}"}; do
  mkdir -p "$stage/packages/$name"
  cp -R "$ASSETS/package/." "$stage/packages/$name/"
  find "$stage/packages/$name" -type f -print0 | xargs -0 sed -i "s|{{PACKAGE}}|$name|g"
done
if $ci; then
  mkdir -p "$stage/.github/workflows"
  cp "$ASSETS/ci.yml" "$stage/.github/workflows/checks.yml"
fi

# Deepest first, so a renamed directory does not invalidate the paths still to visit.
find "$stage" -depth -name 'dot-*' | while IFS= read -r p; do
  mv "$p" "$(dirname "$p")/.$(basename "$p" | cut -c5-)"
done

find "$stage" -type f -print0 |
  xargs -0 sed -i -e "s|{{PROJECT}}|$project|g" -e "s|{{SCOPE}}|$scope|g"

mkdir -p "$target"
target=$(cd "$target" && pwd)
clash=$(cd "$stage" && find . -type f | while IFS= read -r f; do
  [ -e "$target/$f" ] && echo "  $f"
done || true)
if [ -n "$clash" ]; then
  printf 'refusing to overwrite:\n%s\n' "$clash" >&2
  exit 1
fi

cp -R "$stage/." "$target/"
echo "scaffolded $kind into $target"
