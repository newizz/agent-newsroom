---
name: build-virtual-office
description: Build a multi-agent "virtual office" dashboard system (like agent-newsroom) — research pipeline of named AI agents that intake a topic, research it, generate an interactive HTML dashboard, and deploy to GitHub Pages, with a pixel-art office UI showing agents walking and working in real time. Use when the user wants to create a similar multi-agent dashboard system, virtual newsroom, research automation pipeline, or any project that combines (a) Claude Code subagents via Task tool, (b) file-based agent handoff, (c) pixel-art top-down office UI in SVG, (d) status syncing via JSON polling, and (e) GitHub Pages deploy. Triggers on phrases like "build a virtual office", "agent-newsroom style", "multi-agent dashboard", "create a research pipeline like agent-newsroom", or "add Rin to my project".
---

# Build a Virtual Office Multi-Agent System

This skill captures the full methodology, patterns, and gotchas for building a `agent-newsroom`-style multi-agent dashboard system.

## When to use

- User wants to build a multi-agent pipeline that produces an HTML dashboard
- User mentions "virtual office", "newsroom of agents", "agent dashboard"
- User wants to add a similar pipeline to an existing project
- User wants to extend agent-newsroom itself (add agents, modes, features)

## Read first

Before any work, **READ** the full build log:

```
docs/BUILD_LOG.md
```

It contains: design decisions, every issue we hit + resolution, file inventory, setup checklist, and lessons learned. Don't skip this — most of the gotchas (SVG `<use>` shadow DOM, CSS variable theming, gh-pages vs gist sync) are non-obvious.

## Architectural blueprint

```
User topic
    ↓
Orchestrator (Claude Code session reading orchestrator.md)
    ↓
[Intake]   produces runs/<slug>/brief.md
    ↓
[Research] ─ parallel optional ─ [Deep Research via NotebookLM]
    ↓                                     ↓
research.md + sources.json       deep-research/{summary.md, mindmap.json, infographic.png}
    └──────────┬──────────────────────────┘
               ↓
[Builder]  produces published/<slug>/index.html (single-file dashboard)
               ↓
           GitHub Pages auto-deploy
               ↓
[Reporter] produces runs/<slug>/report.md + URL
```

## Required files (minimum viable)

| File | Purpose |
|---|---|
| `orchestrator.md` | Top-level prompt; sequences subagents via `Task` tool |
| `agents/*.md` | One file per agent — contract, steps, quality bar |
| `templates/*.html` | Fixed single-file HTML templates with `{{PLACEHOLDER}}` substitution |
| `office/index.html` | Virtual Office UI (inline SVG pixel scene) |
| `office/status.json` | Single source of truth for agent status |
| `scripts/update-status.sh` | Hook target — modifies status.json via jq |
| `.claude/settings.json` | Claude Code hooks (PreToolUse/PostToolUse/Stop) |
| `.github/workflows/deploy-pages.yml` | Builds `_site/` + deploys |

Optional layers:
- `scripts/setup-gist.sh` + `sync-status-to-gist.sh` — live status on GH Pages
- `tools/notebooklm/` (uv) — deep mode via NotebookLM
- `scripts/deep-research.sh` — wrapper for Rin agent

## Critical patterns — copy these, don't re-invent

### Pattern 1: SVG character template (avoid shadow DOM colour trap)

```html
<svg>
  <defs>
    <!-- Use <g>, NOT <symbol viewBox=...> -->
    <g id="char-body">
      <rect fill="var(--shirt)" ... />
      <rect fill="var(--hair)" ... />
    </g>
  </defs>
  <g id="char-1" data-agent="alice" transform="translate(200,220)">
    <!-- Legs/feet as DIRECT children (CSS animations don't pierce <use>) -->
    <rect class="leg leg-l" .../>
    <rect class="leg leg-r" .../>
    <use href="#char-body"/>
  </g>
</svg>
<style>
  /* Theme via CSS custom properties — they inherit through <use> */
  [data-agent="alice"] { --shirt: #6366f1; --hair: #d97757; }
  [data-agent="bob"]   { --shirt: #10b981; --hair: #1a1a1a; }
</style>
```

### Pattern 2: HTML overlay for name + bubble (independently positioned)

```html
<div class="overlay-layer">
  <div class="bubble-ov" id="bub-alice" data-status="offline">offline</div>
  <div class="name-ov"   id="name-alice">Alice</div>
</div>
```

```js
function updatePos(id, x, y) {
  const bub = document.getElementById('bub-' + id);
  const nm  = document.getElementById('name-' + id);
  bub.style.left = (x / 800) * 100 + '%';
  bub.style.top  = ((y - 40) / 500) * 100 + '%';   // above head
  nm.style.left  = (x / 800) * 100 + '%';
  nm.style.top   = ((y + 42) / 500) * 100 + '%';   // below feet
}
```

### Pattern 3: Walking state machine + activity wandering

```js
const STATE = {};
for (const id of agentIds) STATE[id] = { pos: home, target: home, state: 'sitting', status: 'offline' };

function setStatus(id, status) {
  STATE[id].status = status;
  if (status === 'idle') scheduleWander(id);
  else /* busy/online/offline */ goHome(id);
}

function scheduleWander(id) {
  STATE[id].target = randomActivityPoint();
  STATE[id].state = 'walking';
}

function tick() {
  for (const [id, s] of Object.entries(STATE)) {
    if (s.state === 'walking') stepTowardsTarget(s);
    updateOverlayPos(id, s.pos);
    document.getElementById('char-' + id).setAttribute('transform', `translate(${s.pos.x},${s.pos.y})`);
  }
  requestAnimationFrame(tick);
}
```

### Pattern 4: Hook-driven status updates

```jsonc
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Task", "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/scripts/update-status.sh ${CLAUDE_HOOK_AGENT:-intake} busy 'spawning'" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/scripts/update-status.sh --reset" }] }
    ]
  }
}
```

### Pattern 5: Gist sync via trap (live status on GH Pages)

```bash
# In update-status.sh
sync_to_gist() {
  if [[ -f "$REPO_ROOT/office/gist-config.json" ]]; then
    ( "$REPO_ROOT/scripts/sync-status-to-gist.sh" >/dev/null 2>&1 & ) || true
  fi
}
trap sync_to_gist EXIT
```

```js
// In office/index.html — switch URL on Pages
if (location.hostname.endsWith('.github.io')) {
  const cfg = await (await fetch('gist-config.json')).json();
  STATUS_URL = cfg.gistRawUrl;
}
```

### Pattern 6: Deep mode via uv tool subfolder

```
tools/notebooklm/
├── pyproject.toml        # deps: notebooklm-py[browser]
├── .python-version       # 3.12
├── uv.lock               # committed
├── .venv/                # gitignored
└── scripts/
    ├── setup.sh          # uv venv + uv sync + playwright install
    ├── login.sh          # auth (reuse Chrome cookies)
    └── research.py       # async worker
```

Call from outer scripts: `uv run --directory tools/notebooklm python scripts/research.py ...`

## Setup checklist (for any new project)

1. **Repo** — `git init -b main`, set up remote, `.gitignore`
2. **GH Pages** — Settings → Pages → Source: **GitHub Actions** (NOT branch deploy)
3. **Workflow** — `.github/workflows/deploy-pages.yml` builds `_site/` from `office/` + `published/`, generates `manifest.json`
4. **Agent prompts** — write `orchestrator.md` + one `agents/<role>.md` per agent
5. **Templates** — at least one `templates/<type>.html` with placeholders
6. **Office UI** — copy SVG patterns from `office/index.html`
7. **Status pipeline** — `office/status.json` + `scripts/update-status.sh` + `.claude/settings.json` hooks
8. **(Optional) Gist sync** — `setup-gist.sh` + `sync-status-to-gist.sh` for live GH Pages status
9. **(Optional) NotebookLM** — `tools/notebooklm/` with uv for deep research

## Common pitfalls — do NOT do these

❌ Use `<symbol viewBox="...">` in defs — characters render as full-viewport blobs
❌ Style SVG via descendant selectors that cross `<use>` boundaries — use CSS variables
❌ Embed chair / animatable parts in the `<use>` template — they won't animate or stay put
❌ Put status bubble + name in same flex column — split into independent overlays
❌ Show absolute time on LIVE indicator — use relative ("5s ago"), tick every second
❌ Open `office/index.html` via `file://` — fetch fails silently due to CORS
❌ Set GH Pages Source to "Deploy from a branch" — must be "GitHub Actions" for our workflow
❌ Commit your PAT / API keys — only `gist-config.json` (public URL) is safe to commit
❌ Use `read -sp "..." VAR` in zsh — that's bash syntax, zsh needs `read -s "VAR?..."`
❌ Run NotebookLM tool installed globally — use `uv` in `tools/notebooklm/` for clean isolation

## Workflow during build

1. **Plan first** — present architecture + decision points before writing code
2. **Phased commits** — Foundation → Agents → Templates → Office UI → Scripts → Demo → Verify
3. **Track via TaskCreate/TaskUpdate** — one task per phase, completed before moving on
4. **Test layout** — for SVG changes, suggest opening office/index.html and screenshot
5. **Don't auto-deploy first attempt** — keep things local until structure is right

## Reference files in agent-newsroom

When implementing similar features, read these as canonical examples:

- `office/index.html` — full pixel scene + walking system + Gist sync + polling
- `agents/researcher.md` + `agents/deep-researcher.md` — agent prompt structure
- `agents/builder.md` — template merging + deep-mode extras (markmap + infographic)
- `tools/notebooklm/scripts/research.py` — async NotebookLM worker pattern
- `scripts/update-status.sh` — jq-based JSON mutation + trap-EXIT sync
- `.github/workflows/deploy-pages.yml` — assembles `_site/` from multiple sources

## When user asks "extend the office"

Ask clarifying questions before building:
- New agent? (need character colour palette, home position, status semantics)
- New activity? (just coords + label, easy)
- New template? (placeholders, design system compliance)
- New mode? (orchestrator branch logic + UI selector + status schema field)

Use AskUserQuestion tool for decision points — don't guess.

## Tone

- Be concise — user prefers minimal verbosity
- Show the plan first, get confirmation, then build
- Phased commits with task tracking
- Honest about trade-offs (unofficial APIs, latency, costs)
