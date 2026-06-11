# agent-newsroom — Build Log & Decisions

Chronological record of how this project was built — every decision, every issue, every fix.
Read this when extending the project or building something similar.

---

## 1. Project Genesis

### 1.1 Original request
User wanted a Virtual Agent Office workflow:
1. Agent#1 — receives topic from user, understands it
2. Agent#2 — does deep research, summarizes
3. Agent#3 — builds interactive HTML dashboard, deploys to GitHub Pages
4. Agent#4 — summarizes everything as a report with the URL

Plus a pixel-art "virtual office" UI to watch agents work in real time.

### 1.2 Naming
- Repo: `agent-newsroom` (newsroom metaphor: intake → reporter → editor → publisher)
- GitHub username: `newizz`
- Tagline: *"A 4-agent virtual newsroom that turns any topic into a deep-research interactive dashboard, auto-published to GitHub Pages."*
- Agent names: **Iris** (intake), **Ravi** (research), **Bram** (builder), **Rosa** (reporter). Later added **Rin** (deep researcher via NotebookLM).

### 1.3 Core architectural choice
**Sequential pipeline + file-based handoff** — no backend, no queue, no DB. Each agent reads files from prior agent and writes its own. Claude Code runs the whole thing locally.

```
User topic → brief.md → research.md → published/<slug>/index.html → report.md

> **2026-06 update:** previously Builder wrote to `preview/<slug>/` and a separate `promote-to-published.sh` was used to publish. That two-stage workflow was collapsed — Builder now writes directly to `published/<slug>/`. The `preview/` folder and `promote-to-published.sh` were removed.
```

---

## 2. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Orchestrator | **Claude Code** (1 session) | Has `Task` tool for subagents already |
| Frontend (office UI) | **Inline HTML** + Tailwind CDN | No build step, deploys to GH Pages |
| Pixel art | **Inline SVG** | No image assets, scales responsively |
| Dashboard templates | **Single-file HTML** per topic | One file = ready to deploy |
| Charts | **Chart.js CDN** | Used by data-story, simulator templates |
| Mind map (deep mode) | **markmap-autoloader CDN** | Renders markdown as interactive map |
| Status sync | **JSON file polling** (every 2-5s) | No WebSocket complexity |
| Live status on Pages | **GitHub Gist** (PATCH-on-update) | Static Pages can't see local file |
| Deep research | **notebooklm-py via uv** | Unofficial NotebookLM Python wrapper |
| Hosting | **GitHub Pages** (Actions deploy) | Free, no server |

---

## 3. Phases of Build

### Phase 1 — Foundation
- `README.md` with project description
- `.gitignore`
- `.github/workflows/deploy-pages.yml` — assembles `_site/` from `office/` + `published/`, generates `manifest.json`

### Phase 2 — Agent prompts
Five markdown files defining each agent's contract:
- `orchestrator.md` — Editor-in-Chief, sequences subagents
- `agents/intake.md` — produces `brief.md`
- `agents/researcher.md` — produces `research.md` + `sources.json`
- `agents/builder.md` — produces `published/<slug>/index.html`
- `agents/reporter.md` — produces `report.md`

Each prompt has: deliverables, step-by-step procedure, quality bar, hard rules.

### Phase 3 — 5 fixed dashboard templates
- `concept-explorer.html` — "Explain X" / "How does Y work"
- `data-story.html` — "Analyze trends in X"
- `comparison-matrix.html` — "X vs Y"
- `timeline.html` — "History of X"
- `simulator.html` — "Calculate X / what-if"

All share design system: monochrome base + **indigo `#6366F1`** accent, Inter font, Tailwind CDN, Lucide icons, Chart.js. Placeholder pattern: `{{TITLE}}`, `{{CONTENT_*}}`, `{{SOURCES_HTML}}`.

### Phase 4 — Virtual Office UI
First iteration: 4 desks arranged in a row. Each with avatar emoji, status dot, role label.

Then user asked for **pixel-art top-down office** (like reference image). Rewrote with:
- Inline SVG scene (800x500 viewBox)
- Wood floor pattern + dark wood back wall
- Back-wall furniture: coffee maker, printer, file cabinet, water cooler
- 4 desks with monitors + decorative items
- 4 pixel characters (each unique hair/shirt color)
- 4 plants in corners + 2 side decoration desks
- Neon gradient border (cyan → indigo → purple) with glow
- Title banner + LIVE chip + current-run indicator

### Phase 5 — Scripts + hooks
- `scripts/update-status.sh <agent> <status> [task]` — modifies `office/status.json` via `jq`
- `scripts/deploy.sh <slug>` — git commit + push for a published dashboard
- ~~`scripts/promote-to-published.sh`~~ — **REMOVED** in 2026-06 (preview/published consolidation, see top of file)
- `.claude/settings.json` — hooks: PreToolUse (Task → busy), PostToolUse (Task → idle), Stop (--reset)

### Phase 6 — Demo content
Created 2 sample runs:
- `published/llm-explained/` — Concept Explorer
- `published/stablecoin-peg/` — Data Story
- Each had full `runs/<slug>/brief.md + research.md + sources.json + report.md`

### Phase 7 — Names + walking animation + activities
User wanted characters to **move around** and have status-driven behavior:
- Added name tags below characters
- Built a state machine: `sitting | walking | standing`
- 9 activity points: coffee, printer, cabinet, cooler, meeting center, plants, side desks
- Status → behavior mapping:
  - `busy` → at desk typing (no movement)
  - `idle` → wander to random activity → stand 2-5s → walk back → wait 1.5-3.5s → wander again
  - `online` → at desk relaxed
  - `offline` → at desk dimmed (45% opacity)
- Bubble shows: walking…/activity label/status word/task description (in priority order)

### Phase 8 — Gist sync for GH Pages live status
GH Pages is static — can't poll local `status.json`. Solution:
- One-time: `setup-gist.sh` creates a public Gist
- Every status change: `sync-status-to-gist.sh` PATCHes the gist (called via `trap EXIT` in `update-status.sh`)
- Office UI on `*.github.io` reads from `gist-config.json` and switches `STATUS_URL` to gist raw URL
- Localhost still reads local file (faster)
- Indicator: 🟢 LIVE / 🟡 DEMO / 🔴 ERROR

### Phase 9 — Deep mode (Rin + NotebookLM)
Added 5th agent **Rin** that runs in parallel with Ravi via [notebooklm-py](https://github.com/teng-lin/notebooklm-py):
- Self-contained `tools/notebooklm/` folder with `pyproject.toml` + `uv` venv (no global Python pollution)
- `tools/notebooklm/scripts/research.py` — async worker that creates notebook, runs web research, adds YouTube, asks Key Questions, generates mind map + infographic
- `scripts/deep-research.sh` — wrapper called by Rin
- Office UI: 3+2 layout (5 chars), Rin = silver hair + teal shirt
- Mode badge in LIVE chip: 🔬 DEEP / ⚡ QUICK
- Submit form: research mode (quick/deep) + deploy mode (auto/approve) selectors
- Builder merges Ravi's research + Rin's deep-research, **preferring Rin on conflict** (NotebookLM grounding is stricter), embeds markmap + infographic

---

## 4. Issues Hit & Resolutions

### 4.1 `<symbol>` inside SVG defs → characters rendered as huge blocks in corner
**Cause:** `<symbol viewBox="...">` causes `<use>` to behave as a new viewport (full size of available area).
**Fix:** Replace `<symbol id="char-body" viewBox="...">` with `<g id="char-body">` inside `<defs>`. `<use>` now inherits parent's `transform` correctly.

### 4.2 Chair followed character when walking
**Cause:** Chair was inside `#char-body` template, so it moved with the character.
**Fix:** Separated chair into **static `<g class="static-chair">`** placed at each home position. When character walks away, chair stays. Removed chair from character template.

### 4.3 Characters rendered as solid black blobs (looked like chairs)
**Cause:** CSS descendant selectors (`[data-agent="..."] .shirt-back { fill: ... }`) **don't pierce `<use>` shadow DOM**. Rects inside transcluded template got default fill = black.
**Fix:** Use **CSS custom properties** (`--shirt`, `--hair`) set on `[data-agent="..."]` parent. Variables DO inherit through shadow DOM. In template: `<rect fill="var(--shirt)"/>`.

### 4.4 Name tag overlapped with status bubble above character's head
**Cause:** Both inside a single `.agent-overlay` flexbox column above character.
**Fix:** Split into **two independent overlays** per agent (`.bubble-ov` above head, `.name-ov` below feet). JS positions both via percentage of viewBox coords.

### 4.5 Walking legs didn't animate when inside `<use>`
**Cause:** Same shadow DOM issue — CSS animations don't trigger on rects inside `<use>`.
**Fix:** Place `<rect class="leg">` and `<rect class="foot">` as **direct children of each character `<g>`**, NOT inside the `<use>` template. CSS keyframe `step` with `alternate` and `alternate-reverse` makes L/R legs bob opposite phase.

### 4.6 GitHub Pages 404 even after push
**Cause:** Pages Source was set to "Deploy from a branch" or "None", but our workflow uses `actions/deploy-pages@v4`.
**Fix:** Settings → Pages → Source: **GitHub Actions** (NOT branch deploy). Then either push triggers workflow, or manually run via Actions tab.

### 4.7 Office UI showed all agents as "offline" despite status.json being correct
**Cause:** User opened `office/index.html` via `file://` protocol → browser blocked `fetch('status.json')` due to CORS → silently failed (the error was swallowed).
**Fix:** 
- Added visible error banner when `location.protocol === 'file:'`
- LIVE/DEMO/ERROR mode indicator (color-coded pulse dot)
- Documented: must serve via `python3 -m http.server` (or GH Pages)

### 4.8 LIVE time stuck on last data update timestamp
**Cause:** UI displayed `data.lastUpdate` (from JSON) as absolute time. If JSON didn't change, the time looked frozen.
**Fix:** Compute **relative time** (`just now` / `5s ago` / `2m ago`) and **tick every second** so user always sees something moving — confirms polling is alive.

### 4.9 `read: -p: no coprocess` error on macOS zsh
**Cause:** `read -sp "prompt" VAR` is bash syntax. In zsh, `-p` is for coprocesses.
**Fix:** zsh syntax: `read -s "VAR?prompt"` (note the `?` after var name).

### 4.10 No brew on macOS / Windows
**Cause:** User couldn't install `gh` and `jq` via brew.
**Fix:** Documented alternatives:
- `gh` → winget / scoop / chocolatey / MSI / direct binary
- `jq` → download binary from jqlang.org/download, drop in `~/.local/bin`, add to PATH
- Also made `setup-gist.sh` and `sync-status-to-gist.sh` **fallback to `curl + $GITHUB_TOKEN`** when `gh` isn't available

### 4.11 GH Pages can't show live status (static hosting)
**Cause:** GH Pages serves whatever was last pushed. `office/status.json` updated by hooks only affects local file.
**Fix:** **Gist sync layer.** `setup-gist.sh` creates a public gist, `office/gist-config.json` (committed) points to it. Office UI on `*.github.io` reads from gist URL. Every `update-status.sh` call triggers async `sync-status-to-gist.sh` via `trap EXIT &`.
- Latency: ~5-30s (gist CDN cache)
- Free tier: PAT auth allows 5,000 req/hour (plenty)

### 4.12 Need to embed NotebookLM artifacts but no official API
**Cause:** Google has no public NotebookLM API.
**Fix:** Use [notebooklm-py](https://github.com/teng-lin/notebooklm-py) — unofficial Python wrapper (15k stars, MIT). Install via `uv` in a dedicated folder so it doesn't pollute global Python. Browser cookie reuse means no manual re-login each session.

---

## 5. Key Design Patterns

### 5.1 File-based agent handoff
Each agent writes one or more files; the next agent reads them. No queues, no events, no shared state. The filesystem IS the message bus.

```
runs/<slug>/
├── brief.md            ← Intake
├── research.md         ← Ravi (researcher)
├── sources.json        ← Ravi
├── deep-research/      ← Rin (optional, deep mode only)
│   ├── summary.md
│   ├── sources.json
│   ├── mindmap.json
│   └── infographic.png
└── report.md           ← Reporter
published/<slug>/index.html ← Builder
```

### 5.2 Template + placeholder substitution
Builder reads `templates/<type>.html`, replaces `{{PLACEHOLDER}}` strings with content. No build step needed.

### 5.3 Hook-driven status updates
`.claude/settings.json` hooks call `update-status.sh` on every tool use. UI polls JSON. Effort = 1 bash line per event.

### 5.4 Sequential trap-based sync
```bash
sync_to_gist() { ( ./sync-status-to-gist.sh & ) || true; }
trap sync_to_gist EXIT
```
Every script exit → fire-and-forget gist sync. Async so the script returns immediately.

### 5.5 CSS custom properties for SVG `<use>` colour theming
The only reliable way to vary colours per-instance when using SVG `<use>` references.

### 5.6 Relative time for "is it alive?" indicator
Ticking counter is better UX than static timestamp. Always shows the system is breathing.

### 5.7 Mode-aware orchestrator (quick vs deep)
Two pipelines from same orchestrator. Mode flag travels through brief.md, controlled by user via submit form or natural language.

### 5.8 Parallel research, sequential everything else
Ravi and Rin work on the same input (brief.md) and write to different output files. Builder reads both, merges with conflict resolution rule (prefer Rin).

---

## 6. Full file inventory

```
agent-newsroom/
├── README.md
├── .gitignore
├── .github/workflows/deploy-pages.yml
├── .claude/settings.json
├── docs/
│   └── BUILD_LOG.md                    (this file)
├── orchestrator.md
├── agents/
│   ├── intake.md
│   ├── researcher.md
│   ├── deep-researcher.md              (Rin, deep mode)
│   ├── builder.md
│   └── reporter.md
├── templates/
│   ├── concept-explorer.html
│   ├── data-story.html
│   ├── comparison-matrix.html
│   ├── timeline.html
│   └── simulator.html
├── office/
│   ├── index.html                      (Virtual Office pixel scene)
│   ├── status.json                     (5 agents + currentMode)
│   ├── gist-config.json                (after setup-gist.sh)
│   └── manifest.json                   (generated by GH Actions)
├── scripts/
│   ├── update-status.sh
│   ├── deploy.sh
│   └── (no promote script — preview/published consolidation, 2026-06)
│   ├── setup-gist.sh                   (curl OR gh)
│   ├── sync-status-to-gist.sh          (curl OR gh)
│   └── deep-research.sh                (Rin wrapper)
├── tools/notebooklm/                   (deep mode — self-contained uv venv)
│   ├── pyproject.toml
│   ├── .python-version
│   ├── uv.lock
│   ├── README.md
│   └── scripts/
│       ├── setup.sh
│       ├── login.sh
│       └── research.py                 (async worker)
├── runs/<slug>/                        (intermediate outputs per topic)
├── (preview/ removed — Builder writes straight to published/)
└── published/<slug>/                   (manually promoted)
```

---

## 7. Setup Checklist (recreating from scratch)

```bash
# A. Repo
git init -b main
git remote add origin https://github.com/USER/REPO.git
git add . && git commit -m "init" && git push -u origin main

# B. GitHub Pages
# → github.com/USER/REPO/settings/pages → Source: GitHub Actions
# → wait ~1 min for first workflow run

# C. Live status (Gist)
brew install gh jq           # OR see Section 4.10 for alternatives
gh auth login
./scripts/setup-gist.sh
git add office/gist-config.json
git commit -m "feat: live gist" && git push

# D. Deep mode (optional, ~5 min setup)
curl -LsSf https://astral.sh/uv/install.sh | sh
./tools/notebooklm/scripts/setup.sh
./tools/notebooklm/scripts/login.sh
```

## 8. Run Checklist

```bash
# Local dev — see real status in real-time
cd office && python3 -m http.server 8000
# → http://localhost:8000/

# Run pipeline (Claude Code session)
@orchestrator.md Run the newsroom in deep mode on: "<topic>"

# Re-deploy a dashboard you edited
./scripts/deploy.sh <slug>
```

---

## 9. Lessons Learned (Generalizable)

1. **SVG `<use>` doesn't inherit CSS class selectors** — use CSS custom properties for theming.
2. **`<symbol viewBox>` makes `<use>` a new viewport** — use `<g>` in `<defs>` for transcluding templates.
3. **CSS animations on rects inside `<use>` don't fire** — put animatable elements as direct children of the visible group.
4. **`file://` blocks fetch** — always serve via HTTP for local dev, document this prominently.
5. **Static hosting can't show live data without a sync layer** — Gist / Cloudflare Worker / Pusher are good free options.
6. **Show "alive" with relative time, not absolute** — ticking counter beats frozen timestamp.
7. **zsh's `read` syntax differs from bash** — `read -s "VAR?prompt"` not `read -sp "prompt" VAR`.
8. **`uv` in a subfolder = clean Python isolation** — pin `.python-version`, commit `uv.lock`, gitignore `.venv/`.
9. **Hooks > polling > pubsub for local dev** — Claude Code hooks let you update UI state from inside the agent loop with one bash line.
10. **For parallel agent work, file-based handoff scales further than expected** — race conditions are tractable if each agent writes to its own subdirectory.

---

## 10. Future Extensions Not Yet Built

- Cloudflare Worker live-status (lower latency than Gist CDN)
- Audio overview (NotebookLM podcast MP3) embedded in dashboard
- Quiz/Flashcards interactive section (from NotebookLM)
- Cost tracker (tokens per agent per run)
- Multi-language support (auto-detect from user prompt)
- Critic agent (quality gate between Builder and Reporter)
- Schedule-based re-runs for time-sensitive topics
- Customer-facing share links with selective publish

---

_Last updated: this is the live build log. Append new entries when extending the project._
