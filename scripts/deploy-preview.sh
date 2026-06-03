#!/usr/bin/env bash
# deploy-preview.sh — commit and push a preview dashboard
#
# Usage:  ./scripts/deploy-preview.sh <slug>
#
# Behaviour:
#   1. Verifies preview/<slug>/index.html exists
#   2. Stages preview/<slug>/ and office/status.json
#   3. Commits with a sensible message
#   4. Pushes to origin/main → GitHub Actions deploys to Pages
#
# After ~30-60 seconds the URL is live at:
#   https://newizz.github.io/agent-newsroom/preview/<slug>/

set -euo pipefail

SLUG="${1:?slug required: ./scripts/deploy-preview.sh <slug>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PREVIEW_PATH="preview/$SLUG/index.html"

if [[ ! -f "$PREVIEW_PATH" ]]; then
  echo "✗ Missing $PREVIEW_PATH — Builder must produce this file first." >&2
  exit 1
fi

# Reject if any {{...}} placeholder is still in the file
if grep -q '{{' "$PREVIEW_PATH"; then
  echo "✗ Unreplaced placeholders found in $PREVIEW_PATH:" >&2
  grep -o '{{[A-Z_]*}}' "$PREVIEW_PATH" | sort -u >&2
  exit 1
fi

# Verify it's inside a git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "✗ Not inside a git repository. Initialise with: git init && git remote add origin <url>" >&2
  exit 1
fi

git add "preview/$SLUG/" office/status.json 2>/dev/null || git add "preview/$SLUG/"

if git diff --cached --quiet; then
  echo "ℹ Nothing to commit (preview/$SLUG/ unchanged)."
  exit 0
fi

git commit -m "feat: preview $SLUG"
git push origin HEAD

echo ""
echo "✓ Pushed. GitHub Actions will deploy in ~30-60s:"
echo "  https://newizz.github.io/agent-newsroom/preview/$SLUG/"
