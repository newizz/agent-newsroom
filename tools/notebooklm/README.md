# tools/notebooklm/

NotebookLM integration used by **Rin** (Deep Researcher).

Self-contained, installed via [uv](https://docs.astral.sh/uv/) inside this folder.
Does NOT pollute global Python.

## Install (one-time)

```bash
# from repo root
./tools/notebooklm/scripts/setup.sh
./tools/notebooklm/scripts/login.sh
```

`setup.sh` runs `uv venv` + `uv sync` + `playwright install chromium`.
`login.sh` reuses cookies from local Chrome (fastest) or falls back to interactive Google sign-in.

## Refresh auth (every ~2 weeks)

```bash
./tools/notebooklm/scripts/login.sh
```

## What's inside

| File | Purpose |
|---|---|
| `pyproject.toml` | uv project manifest — depends on `notebooklm-py[browser]` |
| `.python-version` | pinned Python 3.12 |
| `uv.lock` | reproducible lock (committed) |
| `.venv/` | virtualenv (gitignored) |
| `scripts/setup.sh` | one-time install |
| `scripts/login.sh` | auth (reuse Chrome cookies or interactive) |
| `scripts/research.py` | main worker — called by Rin via `scripts/deep-research.sh` |

## How Rin calls it

```bash
uv run --directory tools/notebooklm python scripts/research.py \
  --slug "cat-life-stories" \
  --brief "../../runs/cat-life-stories/brief.md" \
  --output-dir "../../runs/cat-life-stories/deep-research" \
  --youtube "https://youtube.com/watch?v=abc,https://youtube.com/watch?v=def"
```

Wrapped in `scripts/deep-research.sh` at the repo root for convenience.

## Output

Writes to `runs/<slug>/deep-research/`:

```
deep-research/
├── summary.md         # 3-paragraph synthesis + per-question answers
├── sources.json       # all sources NotebookLM collected (web + YouTube)
├── mindmap.json       # NotebookLM-generated mind map (rendered by Builder)
├── infographic.png    # NotebookLM-generated overview image
└── notebook.json      # reference to the NotebookLM notebook id
```

## Troubleshooting

```bash
# Verify auth
uv run --directory tools/notebooklm notebooklm auth check --test --json

# Inspect sources of a notebook
uv run --directory tools/notebooklm notebooklm metadata --json

# Force re-auth
rm -f ~/.config/notebooklm-py/storage_state.json
./tools/notebooklm/scripts/login.sh
```

## Caveats

- **Unofficial Google API** — endpoints can change without notice
- **Rate limits** apply — heavy parallel usage may be throttled
- **Cookies expire** every ~2 weeks
- **Best for personal / research use** — not production-grade
