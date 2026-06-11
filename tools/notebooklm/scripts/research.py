#!/usr/bin/env python
"""
research.py — Deep Research worker called by Rin (Deep Researcher agent)

Pipeline:
  1. Parse brief.md to extract topic, refined question, and Key Questions
  2. Create a new NotebookLM notebook for this run
  3. Auto-discover web sources via NotebookLM's research agent (deep mode)
  4. Add YouTube sources (URLs passed via --youtube)
  5. Ask synthesis + per-question questions in the notebook
  6. Generate mind map (JSON) and infographic (PNG)
  7. Write outputs to runs/<slug>/deep-research/:
       summary.md, sources.json, mindmap.json, infographic.png, notebook.json

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
from pathlib import Path

try:
    from notebooklm import NotebookLMClient
except ImportError as e:
    print("✗ notebooklm-py not installed. Run: ./tools/notebooklm/scripts/setup.sh", file=sys.stderr)
    sys.exit(1)

# Infographic enums (may not be exported on older versions — fall back to defaults if missing)
try:
    from notebooklm import InfographicOrientation, InfographicDetail
    _HAS_INFOGRAPHIC_ENUMS = True
except ImportError:
    InfographicOrientation = None
    InfographicDetail = None
    _HAS_INFOGRAPHIC_ENUMS = False


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


def safe(coro):
    """Wrap an async call so a failure doesn't kill the whole pipeline."""
    async def _run():
        try:
            return await coro
        except Exception as e:
            return e
    return _run()


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
        # 1. Create notebook
        print("→ Creating NotebookLM notebook...")
        nb = await client.notebooks.create(f"{args.slug} — agent-newsroom")
        print(f"  notebook id: {nb.id}")

        # 2. Web research auto-discovery (NotebookLM finds sources itself)
        print("→ Running NotebookLM web research (deep mode)…")
        try:
            await client.sources.add_research(
                nb.id, brief["refined"], mode="deep", wait=True
            )
        except Exception as e:
            print(f"  ⚠ web research failed (continuing): {e}")

        # 3. Add YouTube sources
        for url in youtube_urls:
            print(f"→ Adding YouTube: {url}")
            try:
                await client.sources.add_url(nb.id, url, wait=True)
            except Exception as e:
                print(f"  ⚠ failed: {e}")

        # 4. List sources
        sources = await client.sources.list(nb.id)
        sources_data = []
        for i, s in enumerate(sources, 1):
            sources_data.append({
                "id": i,
                "title": getattr(s, "title", "Untitled"),
                "url": getattr(s, "url", None),
                "type": getattr(s, "type", "unknown"),
            })
        print(f"  total sources: {len(sources_data)}")

        # 5. Synthesis
        print("→ Asking for synthesis...")
        synthesis_q = (
            f"Write a clear 3-paragraph synthesis answering: {brief['refined']}. "
            "Use inline citations like [1], [2] referencing sources in this notebook."
        )
        synth = await client.chat.ask(nb.id, synthesis_q)
        synthesis_text = getattr(synth, "answer", str(synth))

        # 6. Per-question answers
        answers = []
        for i, q in enumerate(brief["questions"], 1):
            print(f"→ Q{i}: {q[:70]}...")
            try:
                a = await client.chat.ask(nb.id, q)
                answers.append({"q": q, "a": getattr(a, "answer", str(a))})
            except Exception as e:
                print(f"  ⚠ failed: {e}")
                answers.append({"q": q, "a": f"_(failed: {e})_"})

        # 7. Mind map
        print("→ Generating mind map...")
        mindmap_path = output_dir / "mindmap.json"
        try:
            mm = await client.artifacts.generate_mind_map(nb.id)
            await client.artifacts.wait_for_completion(nb.id, mm.task_id)
            await client.artifacts.download_mind_map(nb.id, str(mindmap_path))
            print(f"  saved: {mindmap_path}")
        except Exception as e:
            print(f"  ⚠ failed: {e}")
            mindmap_path = None

        # 8. Infographic — uses Enum params (orientation/detail), NOT strings
        print("→ Generating infographic...")
        infographic_path = output_dir / "infographic.png"
        try:
            # Try with explicit enum args first (preferred, library v0.5+)
            if _HAS_INFOGRAPHIC_ENUMS:
                ig = await client.artifacts.generate_infographic(
                    nb.id,
                    orientation=InfographicOrientation.LANDSCAPE,
                    detail=InfographicDetail.STANDARD,
                )
            else:
                # Fallback: defaults (PORTRAIT / STANDARD per library spec)
                ig = await client.artifacts.generate_infographic(nb.id)

            await client.artifacts.wait_for_completion(nb.id, ig.task_id)
            await client.artifacts.download_infographic(nb.id, str(infographic_path))
            print(f"  saved: {infographic_path}")
        except TypeError as e:
            # Library signature changed — retry with bare call
            print(f"  ⚠ signature mismatch, retrying with defaults: {e}")
            try:
                ig = await client.artifacts.generate_infographic(nb.id)
                await client.artifacts.wait_for_completion(nb.id, ig.task_id)
                await client.artifacts.download_infographic(nb.id, str(infographic_path))
                print(f"  saved (defaults): {infographic_path}")
            except Exception as e2:
                print(f"  ✗ failed: {e2}")
                infographic_path = None
        except Exception as e:
            print(f"  ⚠ failed: {e}")
            infographic_path = None

        # 9. Write summary.md
        print("→ Writing summary.md...")
        web_count = sum(
            1 for s in sources_data
            if (s.get("type") or "").lower() not in ("youtube", "video")
        )
        yt_count = len(sources_data) - web_count

        md = [f"# Deep Research: {brief['topic']}", ""]
        md += [
            f"**Slug:** {args.slug}",
            f"**Source:** NotebookLM (via notebooklm-py)",
            f"**Notebook:** {nb.id}",
            f"**Sources:** {len(sources_data)} ({web_count} web · {yt_count} YouTube)",
            f"**Artifacts:** "
            + ", ".join(filter(None, [
                "mindmap.json" if mindmap_path else None,
                "infographic.png" if infographic_path else None,
            ])),
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

        # 10. sources.json
        (output_dir / "sources.json").write_text(
            json.dumps({"sources": sources_data}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (output_dir / "notebook.json").write_text(
            json.dumps(
                {"notebook_id": nb.id, "notebook_title": getattr(nb, "title", "")},
                indent=2,
            ),
            encoding="utf-8",
        )

        print()
        print(f"✓ Done. Output in {output_dir}")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
