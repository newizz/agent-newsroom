#!/usr/bin/env python
"""
research.py — Deep Research worker called by Rin (Deep Researcher agent)

Pipeline:
  1. Parse brief.md to extract topic, refined question, and Key Questions
  2. Create a new NotebookLM notebook for this run
  3. Auto-discover web sources via NotebookLM's research agent (3-step flow:
     research.start → wait_for_completion → import_sources)
  4. Add YouTube sources (URLs passed via --youtube)
  5. Ask synthesis + per-question questions in the notebook
  6. Generate mind map (JSON inline) and infographic (PNG)
  7. Write outputs to runs/<slug>/deep-research/:
       summary.md, sources.json, mindmap.json, infographic.png, notebook.json, errors.log

Usage:
  uv run python research.py \\
    --slug cat-life-stories \\
    --brief ../../runs/cat-life-stories/brief.md \\
    --output-dir ../../runs/cat-life-stories/deep-research \\
    --youtube "https://youtube.com/watch?v=abc,https://youtube.com/watch?v=def"
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

try:
    from notebooklm import NotebookLMClient
except ImportError:
    print("✗ notebooklm-py not installed. Run: ./tools/notebooklm/scripts/setup.sh", file=sys.stderr)
    sys.exit(1)

# Infographic enums — may not be exported on older versions
try:
    from notebooklm import InfographicOrientation, InfographicDetail
    _HAS_INFOGRAPHIC_ENUMS = True
except ImportError:
    InfographicOrientation = None
    InfographicDetail = None
    _HAS_INFOGRAPHIC_ENUMS = False


# ──────────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────────

YOUTUBE_RE = re.compile(r"(youtube\.com/watch|youtu\.be/|youtube\.com/shorts/)", re.IGNORECASE)


def is_youtube(url: str | None) -> bool:
    """Detect YouTube URLs by pattern (NotebookLM's `type` field is always 'unknown')."""
    return bool(url and YOUTUBE_RE.search(url))


def parse_brief(brief_text: str) -> dict:
    """Extract topic, refined question, and Key Questions from brief.md."""
    topic_m = re.search(r"^# Brief:\s*(.+)$", brief_text, re.MULTILINE)
    topic = topic_m.group(1).strip() if topic_m else "Untitled"

    refined_m = re.search(
        r"## Refined question\s*\n+(.+?)(?=\n##|\Z)", brief_text, re.DOTALL
    )
    refined = refined_m.group(1).strip() if refined_m else topic

    questions: list[str] = []
    q_section_m = re.search(
        r"## Key questions Research must answer\s*\n+((?:\d+\..*\n?)+)", brief_text
    )
    if q_section_m:
        for line in q_section_m.group(1).splitlines():
            m = re.match(r"\s*\d+\.\s*(.+)", line)
            if m:
                questions.append(m.group(1).strip())

    return {"topic": topic, "refined": refined, "questions": questions}


class ErrorLog:
    """Collects non-fatal errors so the run continues but failures stay visible."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.entries: list[dict] = []

    def add(self, step: str, exc: BaseException, severity: str = "error") -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "step": step,
            "severity": severity,
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        self.entries.append(entry)
        # Surface immediately to stderr too — Reporter or operator should see this
        print(
            f"  ✗ [{step}] {entry['type']}: {entry['message']}",
            file=sys.stderr,
            flush=True,
        )

    def warn(self, step: str, message: str) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "step": step,
            "severity": "warning",
            "type": "Warning",
            "message": message,
            "traceback": "",
        }
        self.entries.append(entry)
        print(f"  ⚠ [{step}] {message}", file=sys.stderr, flush=True)

    def flush(self) -> Path | None:
        if not self.entries:
            return None
        path = self.output_dir / "errors.log"
        with path.open("w", encoding="utf-8") as f:
            f.write(f"# Deep-research run errors — {len(self.entries)} entry(s)\n")
            f.write(f"# Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
            for e in self.entries:
                f.write(f"[{e['ts']}] {e['severity'].upper()} :: {e['step']}\n")
                f.write(f"  {e['type']}: {e['message']}\n")
                if e["traceback"].strip():
                    f.write("  --- traceback ---\n")
                    for line in e["traceback"].splitlines():
                        f.write(f"  {line}\n")
                f.write("\n")
        return path

    def has_errors(self) -> bool:
        return any(e["severity"] == "error" for e in self.entries)


# ──────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="run slug")
    parser.add_argument("--brief", required=True, help="path to brief.md")
    parser.add_argument("--output-dir", required=True, help="where to write outputs")
    parser.add_argument("--youtube", default="", help="comma-separated YouTube URLs")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    err_log = ErrorLog(output_dir)

    if not brief_path.exists():
        print(f"✗ brief not found: {brief_path}", file=sys.stderr)
        return 1

    brief = parse_brief(brief_path.read_text(encoding="utf-8"))
    youtube_urls = [u.strip() for u in args.youtube.split(",") if u.strip()]

    print(f"→ Slug:      {args.slug}")
    print(f"→ Topic:     {brief['topic']}")
    print(f"→ Refined:   {brief['refined'][:80]}...")
    print(f"→ Questions: {len(brief['questions'])}")
    print(f"→ YouTube:   {len(youtube_urls)} URL(s)")
    print()

    async with await NotebookLMClient.from_storage() as client:
        # ── 1. Create notebook ──────────────────────────────────────
        print("→ Creating NotebookLM notebook...")
        try:
            nb = await client.notebooks.create(f"{args.slug} — agent-newsroom")
            print(f"  notebook id: {nb.id}")
        except Exception as e:
            err_log.add("notebook_create", e)
            err_log.flush()
            return 2

        # ── 2. Web research (3-step flow per notebooklm-py docs) ────
        # FIX #1: was `client.sources.add_research()` (does not exist).
        # Correct API is client.research.start → wait_for_completion → import_sources.
        print("→ Running NotebookLM web research (deep mode)…")
        research_task_id: str | None = None
        research_imported = 0
        try:
            result = await client.research.start(
                nb.id, brief["refined"], source="web", mode="deep"
            )
            if result is None:
                err_log.warn("web_research_start", "research.start returned None")
            else:
                research_task_id = result.get("task_id")
                print(f"  task_id: {research_task_id}")

                status = await client.research.wait_for_completion(
                    nb.id, research_task_id, timeout=900, interval=8
                )

                discovered = status.get("sources", [])
                # result_type==1 means web entry; type==5 is the report markdown itself (skip)
                web_only = [
                    s for s in discovered if s.get("result_type") in (1, None)
                    and (s.get("url") or "").startswith("http")
                ]
                print(f"  discovered: {len(discovered)} entries ({len(web_only)} importable)")

                if web_only:
                    imported = await client.research.import_sources(
                        nb.id, research_task_id, web_only[:30]
                    )
                    research_imported = len(imported)
                    print(f"  ✓ imported {research_imported} web sources")
                else:
                    err_log.warn("web_research_import", "no web sources to import")
        except Exception as e:
            err_log.add("web_research", e)

        # ── 3. Add YouTube sources ──────────────────────────────────
        yt_added = 0
        for url in youtube_urls:
            print(f"→ Adding YouTube: {url}")
            try:
                await client.sources.add_url(nb.id, url, wait=True)
                yt_added += 1
            except Exception as e:
                err_log.add(f"add_youtube[{url}]", e, severity="warning")

        # ── 4. List all sources in notebook ─────────────────────────
        try:
            sources = await client.sources.list(nb.id)
        except Exception as e:
            err_log.add("sources_list", e)
            sources = []

        sources_data = []
        for i, s in enumerate(sources, 1):
            url = getattr(s, "url", None)
            sources_data.append({
                "id": i,
                "title": getattr(s, "title", "Untitled"),
                "url": url,
                "type": getattr(s, "type", "unknown"),
                "kind": "youtube" if is_youtube(url) else "web",  # FIX #3: URL-based detection
            })
        print(f"  total sources in notebook: {len(sources_data)}")

        # ── 5. Synthesis ────────────────────────────────────────────
        synthesis_text = ""
        print("→ Asking for synthesis...")
        try:
            synthesis_q = (
                f"Write a clear 3-paragraph synthesis answering: {brief['refined']}. "
                "Use inline citations like [1], [2] referencing sources in this notebook."
            )
            synth = await client.chat.ask(nb.id, synthesis_q)
            synthesis_text = getattr(synth, "answer", str(synth))
        except Exception as e:
            err_log.add("synthesis", e)
            synthesis_text = "_(synthesis failed — see errors.log)_"

        # ── 6. Per-question answers ─────────────────────────────────
        answers = []
        for i, q in enumerate(brief["questions"], 1):
            print(f"→ Q{i}: {q[:70]}...")
            try:
                a = await client.chat.ask(nb.id, q)
                answers.append({"q": q, "a": getattr(a, "answer", str(a))})
            except Exception as e:
                err_log.add(f"question_{i}", e, severity="warning")
                answers.append({"q": q, "a": f"_(failed: {type(e).__name__}: {e})_"})

        # ── 7. Mind map ─────────────────────────────────────────────
        # FIX #2: generate_mind_map returns a dict (not GenerationStatus). No polling.
        print("→ Generating mind map...")
        mindmap_path: Path | None = output_dir / "mindmap.json"
        try:
            mm_dict = await client.artifacts.generate_mind_map(nb.id)
            # mm_dict is the inline JSON itself — write it directly, but also try
            # download_mind_map for the canonical format with metadata
            try:
                await client.artifacts.download_mind_map(nb.id, str(mindmap_path))
                print(f"  ✓ saved (download_mind_map): {mindmap_path}")
            except Exception as e_dl:
                # Fall back to writing the dict we already have
                err_log.warn("mind_map_download", f"download failed, using inline dict: {e_dl}")
                with mindmap_path.open("w", encoding="utf-8") as f:
                    json.dump(mm_dict, f, indent=2, ensure_ascii=False)
                print(f"  ✓ saved (inline dict): {mindmap_path}")
        except Exception as e:
            err_log.add("mind_map", e)
            mindmap_path = None

        # ── 8. Infographic ──────────────────────────────────────────
        print("→ Generating infographic...")
        infographic_path: Path | None = output_dir / "infographic.png"
        try:
            if _HAS_INFOGRAPHIC_ENUMS:
                ig = await client.artifacts.generate_infographic(
                    nb.id,
                    orientation=InfographicOrientation.LANDSCAPE,
                    detail=InfographicDetail.STANDARD,
                )
            else:
                ig = await client.artifacts.generate_infographic(nb.id)

            await client.artifacts.wait_for_completion(nb.id, ig.task_id)
            await client.artifacts.download_infographic(nb.id, str(infographic_path))
            print(f"  ✓ saved: {infographic_path}")
        except TypeError as e:
            err_log.warn("infographic_signature", f"retrying with defaults: {e}")
            try:
                ig = await client.artifacts.generate_infographic(nb.id)
                await client.artifacts.wait_for_completion(nb.id, ig.task_id)
                await client.artifacts.download_infographic(nb.id, str(infographic_path))
                print(f"  ✓ saved (defaults): {infographic_path}")
            except Exception as e2:
                err_log.add("infographic", e2)
                infographic_path = None
        except Exception as e:
            err_log.add("infographic", e)
            infographic_path = None

        # ── 9. Counts (FIX #3) — by URL pattern, not type field ─────
        yt_count = sum(1 for s in sources_data if s["kind"] == "youtube")
        web_count = len(sources_data) - yt_count

        # ── 10. Write summary.md ────────────────────────────────────
        print("→ Writing summary.md...")
        artifacts_listed = ", ".join(filter(None, [
            "mindmap.json" if mindmap_path else None,
            "infographic.png" if infographic_path else None,
        ])) or "(none)"

        md = [f"# Deep Research: {brief['topic']}", ""]
        md += [
            f"**Slug:** {args.slug}",
            f"**Source:** NotebookLM (via notebooklm-py)",
            f"**Notebook:** {nb.id}",
            f"**Sources:** {len(sources_data)} ({web_count} web · {yt_count} YouTube)",
            f"**Web research import:** {research_imported} sources from NotebookLM auto-discovery",
            f"**Artifacts:** {artifacts_listed}",
        ]
        if err_log.entries:
            md.append(f"**Run errors:** {len(err_log.entries)} (see `errors.log`)")
        md += [
            "",
            "## Synthesis",
            "",
            synthesis_text.strip(),
            "",
            "## Per-question findings",
            "",
        ]
        for i, qa in enumerate(answers, 1):
            md += [f"### Q{i}: {qa['q']}", "", qa["a"].strip(), ""]

        md += [
            "## Source breakdown",
            "",
            f"- Web sources: {web_count}",
            f"- YouTube videos: {yt_count}",
            "",
        ]
        (output_dir / "summary.md").write_text("\n".join(md), encoding="utf-8")

        # ── 11. sources.json + notebook.json ────────────────────────
        (output_dir / "sources.json").write_text(
            json.dumps({"sources": sources_data}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (output_dir / "notebook.json").write_text(
            json.dumps(
                {
                    "notebook_id": nb.id,
                    "notebook_title": getattr(nb, "title", ""),
                    "research_task_id": research_task_id,
                    "research_imported": research_imported,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        # ── 12. errors.log (FIX #4) — surface failures ──────────────
        errors_path = err_log.flush()
        print()
        if errors_path:
            print(f"⚠ {len(err_log.entries)} non-fatal issue(s) logged to {errors_path}")
        print(f"✓ Done. Output in {output_dir}")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
