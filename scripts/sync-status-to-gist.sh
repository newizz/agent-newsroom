#!/usr/bin/env bash
# sync-status-to-gist.sh — push local office/status.json to the configured Gist
#
# Called automatically by update-status.sh after every status change.
# Uses `gh` CLI if available, otherwise falls back to `curl + $GITHUB_TOKEN`.
# Silently no-ops if Gist isn't configured or no auth is available (offline dev mode).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

CFG="office/gist-config.json"
STATUS="office/status.json"

[[ -f "$CFG" ]] || exit 0       # no gist configured — silent skip
[[ -f "$STATUS" ]] || exit 0
command -v jq >/dev/null 2>&1 || exit 0

# ── Sanity guards — never sync corrupt data to gist ──
# Guard 1: file must not be empty (0 bytes)
if [[ ! -s "$STATUS" ]]; then
  echo "✗ sync-status-to-gist: $STATUS is empty — refusing to sync" >&2
  exit 2
fi
# Guard 2: file must be valid JSON
if ! jq -e . "$STATUS" >/dev/null 2>&1; then
  echo "✗ sync-status-to-gist: $STATUS is not valid JSON — refusing to sync" >&2
  exit 3
fi
# Guard 3: schema must have agents array with ≥1 entry (catches truncation / wrong file)
AGENT_COUNT=$(jq -r '(.agents // []) | length' "$STATUS" 2>/dev/null || echo 0)
if [[ "$AGENT_COUNT" -lt 1 ]]; then
  echo "✗ sync-status-to-gist: $STATUS has no agents — refusing to sync" >&2
  exit 4
fi

GIST_ID=$(jq -r '.gistId // empty' "$CFG")
[[ -n "$GIST_ID" ]] || exit 0

# Prefer gh, fall back to curl
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  gh gist edit "$GIST_ID" --filename status.json "$STATUS" >/dev/null 2>&1 || true
elif [[ -n "${GITHUB_TOKEN:-}" ]]; then
  PAYLOAD=$(jq -n --rawfile content "$STATUS" \
    '{files: {"status.json": {content: $content}}}')
  curl -sS -X PATCH "https://api.github.com/gists/${GIST_ID}" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    -d "$PAYLOAD" >/dev/null 2>&1 || true
fi
