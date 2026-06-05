#!/usr/bin/env bash
# setup.sh — one-time install of notebooklm-py inside this folder via uv
#
# Usage:  ./tools/notebooklm/scripts/setup.sh
#
# Prereq: uv installed (https://docs.astral.sh/uv/getting-started/installation/)

set -euo pipefail

TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$TOOL_DIR"

command -v uv >/dev/null 2>&1 || {
  echo "✗ uv is required — install with:" >&2
  echo "    curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
  exit 1
}

echo "→ Creating venv at $TOOL_DIR/.venv (python 3.12)"
uv venv --python 3.12

echo "→ Installing notebooklm-py[browser]..."
uv sync

echo "→ Installing Chromium for Playwright (one-time, ~170 MB)..."
uv run playwright install chromium

echo ""
echo "✓ NotebookLM tool installed in $TOOL_DIR"
echo ""
echo "Next: authenticate with Google"
echo "  ./tools/notebooklm/scripts/login.sh"
