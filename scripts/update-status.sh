#!/usr/bin/env bash
# update-status.sh — update office/status.json for a specific agent
#
# Usage:
#   ./scripts/update-status.sh <agent-id> <status> [task-description]
#
# agent-id: intake | researcher | builder | reporter
# status:   busy | idle | online | offline
# task:     optional speech-bubble text shown in office UI
#
# Also accepts:
#   ./scripts/update-status.sh --run <slug>      → sets currentSlug
#   ./scripts/update-status.sh --clear-run        → clears currentSlug
#   ./scripts/update-status.sh --reset            → all agents back to offline

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATUS_FILE="$REPO_ROOT/office/status.json"

command -v jq >/dev/null 2>&1 || { echo "jq is required — install with: brew install jq" >&2; exit 1; }

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Fire-and-forget sync to Gist after every status change (silent if not configured)
sync_to_gist() {
  if [[ -f "$REPO_ROOT/office/gist-config.json" ]]; then
    ( "$REPO_ROOT/scripts/sync-status-to-gist.sh" >/dev/null 2>&1 & ) || true
  fi
}
trap sync_to_gist EXIT

case "${1:-}" in
  --run)
    SLUG="${2:?slug required}"
    jq --arg slug "$SLUG" --arg now "$NOW" \
      '.currentSlug = $slug | .currentRun = $slug | .lastUpdate = $now' \
      "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"
    exit 0
    ;;
  --clear-run)
    jq --arg now "$NOW" '.currentSlug = null | .currentRun = null | .lastUpdate = $now' \
      "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"
    exit 0
    ;;
  --reset)
    jq --arg now "$NOW" \
      '.currentSlug = null | .currentRun = null | .lastUpdate = $now |
       .agents = (.agents | map(.status = "offline" | .task = ""))' \
      "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"
    exit 0
    ;;
esac

AGENT="${1:?agent-id required: intake|researcher|builder|reporter}"
STATUS="${2:?status required: busy|idle|online|offline}"
TASK="${3:-}"

jq --arg id "$AGENT" --arg status "$STATUS" --arg task "$TASK" --arg now "$NOW" \
  '.lastUpdate = $now |
   .agents = (.agents | map(
     if .id == $id
     then .status = $status | .task = $task
     else .
     end
   ))' \
  "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"

echo "✓ $AGENT → $STATUS${TASK:+ ($TASK)}"
