#!/usr/bin/env bash
# setup-gist.sh — one-time: create a public Gist that mirrors office/status.json
#
# Uses `gh` CLI if available, otherwise falls back to `curl + $GITHUB_TOKEN`.
#
# Requirements (either path):
#   - Path A:  gh CLI authenticated  (`gh auth login`)
#   - Path B:  $GITHUB_TOKEN env var with a PAT that has `gist` scope
#   - jq installed (both paths)
#
# Usage:
#   ./scripts/setup-gist.sh           # creates gist if not configured
#   ./scripts/setup-gist.sh --force   # recreate even if already configured

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

command -v jq >/dev/null 2>&1 || { echo "✗ jq required" >&2; exit 1; }

CFG="office/gist-config.json"
STATUS="office/status.json"

if [[ -f "$CFG" ]] && [[ "${1:-}" != "--force" ]]; then
  echo "ℹ Gist already configured. Use --force to recreate."
  echo ""
  cat "$CFG"
  exit 0
fi

# ── Detect auth method ───────────────────────────────────────────
USE_GH=0
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  USE_GH=1
elif [[ -n "${GITHUB_TOKEN:-}" ]]; then
  USE_GH=0
else
  cat >&2 <<EOF
✗ No GitHub authentication found.

Pick ONE of these paths:

  A) Install gh CLI + authenticate:
       brew install gh  (or via winget/scoop/MSI)
       gh auth login

  B) Create a Personal Access Token (scope: gist) and export it:
       export GITHUB_TOKEN="github_pat_xxxxxxxx"
       (add to ~/.zshrc or ~/.bashrc to persist)

Then re-run this script.
EOF
  exit 1
fi

# ── Create gist ──────────────────────────────────────────────────
echo "→ Creating public Gist..."

if [[ $USE_GH -eq 1 ]]; then
  URL=$(gh gist create "$STATUS" --public --desc "agent-newsroom live status" --filename status.json)
  ID=$(echo "$URL" | sed 's|.*/||')
  USER=$(gh api user --jq .login)
else
  # Build JSON payload with jq (safe escaping)
  PAYLOAD=$(jq -n --rawfile content "$STATUS" \
    '{description: "agent-newsroom live status", public: true, files: {"status.json": {content: $content}}}')

  RESPONSE=$(curl -sS -X POST https://api.github.com/gists \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    -d "$PAYLOAD")

  ID=$(echo "$RESPONSE"  | jq -r '.id // empty')
  URL=$(echo "$RESPONSE" | jq -r '.html_url // empty')
  USER=$(echo "$RESPONSE" | jq -r '.owner.login // empty')

  if [[ -z "$ID" || -z "$USER" ]]; then
    echo "✗ Gist creation failed. Response:" >&2
    echo "$RESPONSE" | jq . >&2
    exit 1
  fi
fi

RAW_URL="https://gist.githubusercontent.com/${USER}/${ID}/raw/status.json"
API_URL="https://api.github.com/gists/${ID}"

cat > "$CFG" <<EOF
{
  "gistId": "${ID}",
  "user": "${USER}",
  "gistUrl": "${URL}",
  "gistRawUrl": "${RAW_URL}",
  "gistApiUrl": "${API_URL}"
}
EOF

echo ""
echo "✓ Gist created"
echo "  ID:  ${ID}"
echo "  Web: ${URL}"
echo "  Raw: ${RAW_URL}"
echo ""
echo "✓ Saved to ${CFG}"
echo ""
echo "Next steps:"
echo "  git add ${CFG}"
echo "  git commit -m 'feat: add live-status gist'"
echo "  git push"
echo ""
echo "After Pages redeploys, the Virtual Office will fetch from the Gist automatically."
