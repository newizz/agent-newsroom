#!/usr/bin/env bash
# deploy.sh — commit and push a published dashboard
#
# Usage:  ./scripts/deploy.sh <slug>
#
# Behaviour:
#   1. Verifies published/<slug>/index.html exists
#   2. Stages published/<slug>/ and office/status.json
#   3. Commits with a sensible message
#   4. Pushes to origin/main → GitHub Actions deploys to Pages
#
# After ~30-60 seconds the URL is live at:
#   https://newizz.github.io/agent-newsroom/published/<slug>/

set -euo pipefail

SLUG="${1:?slug required: ./scripts/deploy.sh <slug>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DASH_PATH="published/$SLUG/index.html"

if [[ ! -f "$DASH_PATH" ]]; then
  echo "✗ Missing $DASH_PATH — Builder must produce this file first." >&2
  exit 1
fi

# Reject if any {{...}} placeholder is still in the file
if grep -q '{{' "$DASH_PATH"; then
  echo "✗ Unreplaced placeholders found in $DASH_PATH:" >&2
  grep -o '{{[A-Z_]*}}' "$DASH_PATH" | sort -u >&2
  exit 1
fi

# Verify it's inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "✗ Not inside a git repository. Initialise with: git init && git remote add origin <url>" >&2
  exit 1
fi

git add "published/$SLUG/" office/status.json 2>/dev/null || git add "published/$SLUG/"

if git diff --cached --quiet; then
  echo "ℹ Nothing to commit (published/$SLUG/ unchanged)."
  exit 0
fi

git commit -m "publish: $SLUG"
git push origin HEAD

echo ""
echo "✓ Pushed. GitHub Actions will deploy in ~30-60s:"
echo "  https://newizz.github.io/agent-newsroom/published/$SLUG/"
