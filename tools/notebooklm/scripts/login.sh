#!/usr/bin/env bash
# login.sh — authenticate with NotebookLM (reuses cookies from local Chrome if available)
#
# Usage:  ./tools/notebooklm/scripts/login.sh
#
# Cookies expire ~every 2 weeks — rerun this when auth check fails.

set -euo pipefail

TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$TOOL_DIR"

# Prefer reusing existing Chrome session; fall back to interactive login
if uv run notebooklm login --browser-cookies chrome 2>/dev/null; then
  echo "✓ Reused Chrome cookies"
else
  echo "→ Falling back to interactive login (browser will open)"
  uv run notebooklm login
fi

echo ""
echo "→ Verifying auth..."
uv run notebooklm auth check --test --json
