# Knowledge Base

Long-term archive of every research run. One file per topic — self-contained, citation-rich, future-proof.

## Layout

```
kb/
├── README.md            (this file)
├── <slug-1>.md          (e.g. llm-explained.md)
├── <slug-2>.md
└── …
```

Each `<slug>.md` is produced by the **Reporter agent (Rosa)** at the end of every run. It merges:
- `runs/<slug>/brief.md`
- `runs/<slug>/research.md` + `sources.json`
- `runs/<slug>/deep-research/*` (if deep mode)
- Pointers to the published dashboard and any artifacts

## Why a separate `kb/` folder

- **Flat, searchable** — `grep -l "stablecoin" kb/*.md` works
- **Self-contained** — each file readable without any other context
- **Stable citations** — bibliography at the bottom of each KB stays stable even if `runs/<slug>/` is later cleaned
- **LLM-friendly** — feed one KB file as context to refresh a topic later
- **Backup** — even if `runs/` or `published/` are pruned, the knowledge survives here

## Searching

```bash
# Find all KBs touching a term
grep -l "stablecoin" kb/*.md

# Get the TL;DR of every KB
for f in kb/*.md; do
  echo "── $(basename "$f") ──"
  awk '/^> \*\*TL;DR\*\*/,/^##/' "$f" | head -5
done

# Sort by date (newest first)
ls -lt kb/*.md
```

## Frontmatter schema

Every KB starts with YAML frontmatter:

```yaml
---
slug: <slug>
title: <Topic Title>
mode: quick | deep
date: <YYYY-MM-DD>
dashboard: <URL>
agents: [...]
source_count_web: N
source_count_video: M
confidence: high | medium | low
tags: [...]
---
```

Tools / future agents can read the frontmatter to filter without parsing the markdown body.

## Lifecycle

- Created automatically by Reporter at the end of every run
- Never overwritten by a later run with the same slug — Reporter should refuse and warn (or write `<slug>-2.md` instead)
- Manually editable if you want to add notes after the fact

## Not to be confused with…

- `runs/<slug>/` — intermediate per-run files (brief, research, sources, deep-research). May be cleaned up over time.
- `published/<slug>/` — the user-facing dashboard. The "product".
- `kb/<slug>.md` — the "research archive". The "memory".
