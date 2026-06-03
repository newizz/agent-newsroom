# agent-newsroom

> A 4-agent virtual newsroom that turns any topic into a deep-research interactive dashboard, auto-published to GitHub Pages.

**agent-newsroom** is a minimal pipeline that runs entirely on top of [Claude Code](https://docs.claude.com/en/docs/claude-code). Give it a topic and four specialized agents take it from question to published artifact:

- 🎙️ **Intake Agent** — clarifies the brief, asks back if vague
- 🔍 **Research Agent** — deep-researches the topic with cited sources
- 🎨 **Builder Agent** — picks a template and ships a polished interactive HTML dashboard
- 📋 **Reporter Agent** — summarizes the run and hands back the live URL

The output is a single-file HTML dashboard, auto-deployed to GitHub Pages. A pixel-style "virtual office" UI lets you watch the agents work and submit new topics from the browser.

**Live site:** https://newizz.github.io/agent-newsroom/

---

## How it works

```
User topic
   │
   ▼
┌──────────────────┐
│ 🎙️  Intake        │  → runs/<slug>/brief.md
└──────────────────┘
   │
   ▼
┌──────────────────┐
│ 🔍  Research     │  → runs/<slug>/research.md + sources.json
└──────────────────┘
   │
   ▼
┌──────────────────┐
│ 🎨  Builder      │  → preview/<slug>/index.html (auto-deployed)
└──────────────────┘
   │
   ▼
┌──────────────────┐
│ 📋  Reporter     │  → runs/<slug>/report.md + URL back to user
└──────────────────┘
```

All four agents are spawned as subagents (via Claude Code's `Task` tool) from a single orchestrator session. Hand-off between agents is via files in `runs/<slug>/`. No backend, no database, no queue.

## Repo layout

```
agent-newsroom/
├── orchestrator.md         # top-level prompt for Claude Code
├── agents/                 # 1 file per agent system prompt
│   ├── intake.md
│   ├── researcher.md
│   ├── builder.md
│   └── reporter.md
├── templates/              # 5 fixed HTML templates the Builder picks from
│   ├── concept-explorer.html
│   ├── data-story.html
│   ├── comparison-matrix.html
│   ├── timeline.html
│   └── simulator.html
├── office/                 # Virtual Office UI (GitHub Pages landing)
│   ├── index.html
│   └── status.json
├── scripts/                # Shell helpers used by hooks
│   ├── update-status.sh
│   ├── deploy-preview.sh
│   └── promote-to-published.sh
├── .claude/settings.json   # Hooks that update status.json in real time
├── runs/<slug>/            # One folder per topic run (intermediate files)
├── preview/<slug>/         # Auto-deployed draft dashboards
├── published/<slug>/       # Promoted (approved) dashboards
└── .github/workflows/      # GitHub Pages deploy
```

## Usage

### One-time setup

1. Clone this repo
2. Install [Claude Code](https://docs.claude.com/en/docs/claude-code/quickstart) and authenticate
3. Enable GitHub Pages → settings → Pages → source: GitHub Actions
4. Push to `main` — GitHub Actions deploys the site

### Run a topic

In the repo directory, start Claude Code and tell it:

```
@orchestrator.md Run the newsroom on this topic:
"Explain how stablecoins maintain their peg, with worked examples"
```

The orchestrator will:
1. Spawn Intake to clarify and produce `brief.md`
2. Spawn Research to produce `research.md`
3. Spawn Builder to write `preview/<slug>/index.html` and commit
4. Spawn Reporter to produce `report.md` and return the live URL

### Submit from the browser

Open https://newizz.github.io/agent-newsroom/ — type a topic into the form. The page copies a ready-made command to your clipboard. Paste it into your local Claude Code session to start a run.

### Promote a preview to published

When you're happy with a `/preview/<slug>/` dashboard, run:

```bash
./scripts/promote-to-published.sh <slug>
```

This copies it to `/published/<slug>/` and pushes — that URL becomes the "official" version.

## Live status on GitHub Pages

Because GitHub Pages serves static files, the `office/status.json` baked into a push is stale until the next deploy. To make the Virtual Office show **live** status while you run the pipeline locally, agent-newsroom syncs `status.json` to a **public GitHub Gist** on every change.

### One-time setup

```bash
brew install gh jq           # if not already installed
gh auth login                # authenticate with GitHub
./scripts/setup-gist.sh      # creates the gist, writes office/gist-config.json
git add office/gist-config.json
git commit -m "feat: live-status gist"
git push                      # Pages picks up the gist URL
```

### How it works

- **Local dev** (`localhost`, `python3 -m http.server`) → Office UI reads `office/status.json` directly (sub-second updates)
- **On `*.github.io`** → Office UI fetches the Gist raw URL listed in `office/gist-config.json` (a few seconds CDN lag, but truly live)
- **Hook flow**: agent activity → `update-status.sh` → `office/status.json` updated → `sync-status-to-gist.sh` called automatically → Gist updated → public visitors see it within seconds

### Disabling

Delete `office/gist-config.json` (and stop committing it). The sync becomes a silent no-op and Pages falls back to DEMO mode for visitors.

## Templates

The Builder Agent auto-picks one of 5 templates based on the topic:

| Template | When picked | Best for |
|---|---|---|
| 🧭 Concept Explorer | "Explain X" / "What is Y" | Definitions, theory, concepts |
| 📊 Data Story | "Analyze X" / "Trends in Y" | Markets, time series, statistics |
| ⚖️ Comparison Matrix | "X vs Y" / "Best Z" | Trade-offs, alternatives |
| 🕰️ Timeline | "History of X" / "Evolution of Y" | Chronologies, milestones |
| 🎛️ Simulator | "Calculate X" / "Simulate Y" | Tunable parameters, what-ifs |

All templates use the same design system: Tailwind via CDN, Inter font, Lucide icons, Chart.js, indigo (`#6366F1`) accent on a monochrome base.

## Design philosophy

- **Ultra-minimal** — Linear / Stripe / Apple aesthetic
- **Single-file output** — every dashboard is one self-contained HTML
- **No build step** — no npm, no bundler, just open the file
- **Cited sources only** — Research Agent must cite every claim
- **Two-stage publish** — auto-deploy to `/preview/`, manual promote to `/published/`

## License

MIT
