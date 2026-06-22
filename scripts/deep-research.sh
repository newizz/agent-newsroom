#!/usr/bin/env bash
# deep-research.sh — Rin's entry point. Runs NotebookLM research for a slug.
#
# Usage:
#   ./scripts/deep-research.sh <slug> [<youtube-csv>] [<web-urls-csv>]
#   ./scripts/deep-research.sh <slug> "" "" --requery <notebook-id>
#
# --requery <notebook-id>: skip notebook creation/web research, ask questions to existing notebook
#
# Robustness layers (P0-P2):
#   - Pre-flight: verify venv, package import, and auth before invoking Python (P2)
#   - stderr is teed to deep-research/stderr.log so crash output is preserved (P1)
#   - research.py writes a startup marker to errors.log immediately on launch (P0)

set -uo pipefail   # NOTE: no `-e` here — we want to capture errors, not die silently

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SLUG="${1:?slug required}"
YOUTUBE_CSV="${2:-}"
WEB_URLS_CSV="${3:-}"

# Parse --requery <notebook-id> flag (arg 4 + 5)
NOTEBOOK_ID=""
if [[ "${4:-}" == "--requery" && -n "${5:-}" ]]; then
  NOTEBOOK_ID="${5}"
fi

BRIEF="runs/$SLUG/brief.md"
OUT="runs/$SLUG/deep-research"
ERR_LOG="$OUT/errors.log"
STDERR_LOG="$OUT/stderr.log"

mkdir -p "$OUT"

# ── helpers ──────────────────────────────────────────────────────────
preflight_fail() {
  local step="$1"
  local msg="$2"
  local hint="${3:-}"
  cat > "$ERR_LOG" <<EOF
# Deep-research pre-flight FAILED (research.py never started)
# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ERROR :: pre_flight::$step
  $msg
${hint:+  --- hint ---}
${hint:+  $hint}
EOF
  echo "✗ pre-flight FAILED: $step — $msg" >&2
  [ -n "$hint" ] && echo "  hint: $hint" >&2
  ./scripts/update-status.sh deep-researcher idle "" 2>/dev/null || true
  exit 10
}

# ── Pre-flight checks (P2) ───────────────────────────────────────────

if [[ ! -f "$BRIEF" ]]; then
  preflight_fail "brief_missing" \
    "Brief not found: $BRIEF" \
    "Intake must run first to produce brief.md"
fi

if ! command -v uv >/dev/null 2>&1; then
  preflight_fail "uv_not_installed" \
    "uv command not found in PATH" \
    "Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

if [[ ! -d "tools/notebooklm/.venv" ]]; then
  preflight_fail "venv_missing" \
    "NotebookLM venv missing at tools/notebooklm/.venv" \
    "Run: ./tools/notebooklm/scripts/setup.sh"
fi

# Test that we can actually import the package (catches broken venv + missing deps)
IMPORT_OUT=$(uv run --directory tools/notebooklm \
  python -c "import notebooklm; print('ok')" 2>&1)
if [[ "$IMPORT_OUT" != *"ok"* ]]; then
  preflight_fail "import_failed" \
    "Cannot import notebooklm package" \
    "Output: ${IMPORT_OUT:0:300} | Try: ./tools/notebooklm/scripts/setup.sh"
fi

# Test auth — quick check, no actual network call to NotebookLM proper
AUTH_OUT=$(uv run --directory tools/notebooklm \
  notebooklm auth check --test --json 2>&1)
AUTH_STATUS=$(echo "$AUTH_OUT" | python3 -c "import sys, json; \
  d = json.loads(sys.stdin.read()); print(d.get('status', 'unknown'))" 2>/dev/null || echo "parse_error")

if [[ "$AUTH_STATUS" != "ok" ]]; then
  preflight_fail "auth_invalid" \
    "NotebookLM authentication failed (status: $AUTH_STATUS)" \
    "Run: ./tools/notebooklm/scripts/login.sh   |   Auth output: ${AUTH_OUT:0:300}"
fi

echo "✓ pre-flight passed (uv ok, package importable, auth status=$AUTH_STATUS)"

# ── Run ──────────────────────────────────────────────────────────────

./scripts/update-status.sh deep-researcher busy "Deep research in NotebookLM..." 2>/dev/null || true

# P1: capture stderr to file while still letting it flow to terminal
# We use `tee` via process substitution so stderr shows live AND lands on disk.
REQUERY_ARGS=""
if [[ -n "$NOTEBOOK_ID" ]]; then
  echo "→ Requery mode: using existing notebook $NOTEBOOK_ID"
  REQUERY_ARGS="--notebook-id $NOTEBOOK_ID"
fi

uv run --directory tools/notebooklm \
  python scripts/research.py \
  --slug "$SLUG" \
  --brief "../../runs/$SLUG/brief.md" \
  --output-dir "../../runs/$SLUG/deep-research" \
  --youtube "$YOUTUBE_CSV" \
  --web-urls "$WEB_URLS_CSV" \
  $REQUERY_ARGS \
  2> >(tee "$STDERR_LOG" >&2)

EXIT=$?

./scripts/update-status.sh deep-researcher idle "" 2>/dev/null || true

if [[ $EXIT -ne 0 ]]; then
  echo "⚠ research.py exited with code $EXIT — see $ERR_LOG and $STDERR_LOG" >&2
fi

exit $EXIT
