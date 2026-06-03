#!/usr/bin/env bash
# promote-to-published.sh — promote a preview dashboard to /published/
#
# Usage:  ./scripts/promote-to-published.sh <slug>

set -euo pipefail

SLUG="${1:?slug required: ./scripts/promote-to-published.sh <slug>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SRC="preview/$SLUG"
DST="published/$SLUG"

if [[ ! -d "$SRC" ]]; then
  echo "✗ $SRC does not exist." >&2
  exit 1
fi

mkdir -p "$(dirname "$DST")"
rm -rf "$DST"
cp -R "$SRC" "$DST"

git add "$DST"
git commit -m "publish: $SLUG"
git push origin HEAD

echo ""
echo "✓ Promoted $SLUG to /published/. Live in ~30-60s:"
echo "  https://newizz.github.io/agent-newsroom/published/$SLUG/"
