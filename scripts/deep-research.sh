#!/usr/bin/env bash
# deep-research.sh — Rin's entry point. Runs NotebookLM research for a slug.
#
# Usage:
#   ./scripts/deep-research.sh <slug> [<youtube-urls-csv>]
#
# Example:
#   ./scripts/deep-research.sh cat-life-stories "https://youtu.be/abc,https://youtu.be/def"

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SLUG="${1:?slug required}"
YOUTUBE_CSV="${2:-}"

BRIEF="runs/$SLUG/brief.md"
OUT="runs/$SLUG/deep-research"

if [[ ! -f "$BRIEF" ]]; then
  echo "✗ brief not found: $BRIEF (Intake must run first)" >&2
  exit 1
fi

if [[ ! -d "tools/notebooklm/.venv" ]]; then
  echo "✗ NotebookLM tool not installed. Run: ./tools/notebooklm/scripts/setup.sh" >&2
  exit 1
fi

mkdir -p "$OUT"

# Tell the office UI Rin is busy
./scripts/update-status.sh deep-researcher busy "Deep research in NotebookLM..." 2>/dev/null || true

# Run from tool dir so its .venv is picked up
uv run --directory tools/notebooklm \
  python scripts/research.py \
  --slug "$SLUG" \
  --brief "../../runs/$SLUG/brief.md" \
  --output-dir "../../runs/$SLUG/deep-research" \
  --youtube "$YOUTUBE_CSV"

EXIT=$?

./scripts/update-status.sh deep-researcher idle "" 2>/dev/null || true

exit $EXIT
