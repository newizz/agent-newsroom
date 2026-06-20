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


def is_youtube(url: str | None, title: str | None = None) -> bool:
    """Detect YouTube by pattern. Checks BOTH url and title because NotebookLM
    sometimes leaves `url` null and stores the YouTube URL in `title` instead."""
    target = f"{url or ''} {title or ''}"
    return bool(YOUTUBE_RE.search(target))


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


SCRIPT_VERSION = "2026-06-19"  # bump on prompt/code changes for traceability


class ErrorLog:
    """Collects non-fatal errors so the run continues but failures stay visible.

    P0 guarantees:
      - A startup marker is written immediately on init (so even instant crashes
        leave evidence — empty deep-research/ folder = no Python started at all).
      - flush() is idempotent and safe to call multiple times.
      - Designed to be called from a try/finally so the log ALWAYS lands on disk,
        even if the script blows up before reaching the happy-path end.
    """

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.entries: list[dict] = []
        self._started_at = datetime.now(timezone.utc)
        self._wrote_startup_marker = False
        # Write the startup marker SYNCHRONOUSLY before anything else can fail
        self._write_startup_marker()

    def _write_startup_marker(self) -> None:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            marker = self.output_dir / "errors.log"
            with marker.open("w", encoding="utf-8") as f:
                f.write(f"# Deep-research run log (initial — will be rewritten on completion)\n")
                f.write(f"# Started: {self._started_at.isoformat()}\n")
                f.write(f"# Script version: {SCRIPT_VERSION}\n")
                f.write(f"# Python: {sys.version.split()[0]}\n")
                f.write(f"# PID: {sys.argv}\n\n")
                f.write("(no errors yet — this file will be rewritten if the run completes)\n")
            self._wrote_startup_marker = True
        except Exception as e:
            # If we can't even write a marker, surface to stderr loudly
            print(f"✗ FATAL: cannot write to {self.output_dir}: {e}", file=sys.stderr, flush=True)

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
        """Write all entries to errors.log. Idempotent — safe to call multiple times."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            path = self.output_dir / "errors.log"
            now = datetime.now(timezone.utc)
            with path.open("w", encoding="utf-8") as f:
                if not self.entries:
                    f.write(f"# Deep-research run — no errors\n")
                    f.write(f"# Started: {self._started_at.isoformat()}\n")
                    f.write(f"# Completed: {now.isoformat()}\n")
                    f.write(f"# Script version: {SCRIPT_VERSION}\n")
                    return None
                f.write(f"# Deep-research run errors — {len(self.entries)} entry(s)\n")
                f.write(f"# Started: {self._started_at.isoformat()}\n")
                f.write(f"# Flushed: {now.isoformat()}\n")
                f.write(f"# Script version: {SCRIPT_VERSION}\n\n")
                for e in self.entries:
                    f.write(f"[{e['ts']}] {e['severity'].upper()} :: {e['step']}\n")
                    f.write(f"  {e['type']}: {e['message']}\n")
                    if e["traceback"].strip():
                        f.write("  --- traceback ---\n")
                        for line in e["traceback"].splitlines():
                            f.write(f"  {line}\n")
                    f.write("\n")
            return path
        except Exception as e:
            print(f"✗ FATAL: errors.log flush failed: {e}", file=sys.stderr, flush=True)
            return None

    def has_errors(self) -> bool:
        return any(e["severity"] == "error" for e in self.entries)


# ──────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────


async def _main_inner(args, err_log: "ErrorLog") -> int:
    """The actual work — wrapped by main() in try/finally for guaranteed flush."""
    brief_path = Path(args.brief)
    output_dir = Path(args.output_dir)

    if not brief_path.exists():
        err_log.add("brief_missing", FileNotFoundError(f"brief not found: {brief_path}"))
        return 1

    output_dir = Path(args.output_dir)
    brief = parse_brief(brief_path.read_text(encoding="utf-8"))
    youtube_urls = [u.strip() for u in args.youtube.split(",") if u.strip()]
    web_fallback_urls = [u.strip() for u in args.web_urls.split(",") if u.strip()]

    print(f"→ Script ver:  {SCRIPT_VERSION}")
    print(f"→ Slug:        {args.slug}")
    print(f"→ Topic:       {brief['topic']}")
    print(f"→ Refined:     {brief['refined'][:80]}...")
    print(f"→ Questions:   {len(brief['questions'])}")
    print(f"→ YouTube:     {len(youtube_urls)} URL(s)")
    print(f"→ Web fallback:{len(web_fallback_urls)} URL(s)")
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

        # ── 2. Web research (3-step flow + retry + fallback) ────────
        # Strategy (A+C combined):
        #   A. Try mode="deep" with extended timeout (1800s = 30 min)
        #   A. If "no_research" timeout → retry mode="fast" (smaller, more reliable)
        #   C. If both fail OR import < 5 → add Rin's pre-curated web URLs directly
        print("→ Running NotebookLM web research…")
        research_task_id: str | None = None
        research_imported = 0
        research_mode_used: str | None = None
        web_fallback_added = 0

        async def try_research(mode: str, timeout: int) -> int:
            """Run research.start → wait → import. Returns count of imported sources."""
            nonlocal research_task_id, research_mode_used
            print(f"  attempting mode='{mode}' (timeout {timeout}s)...")
            result = await client.research.start(
                nb.id, brief["refined"], source="web", mode=mode
            )
            if result is None:
                err_log.warn(f"research_start_{mode}", "research.start returned None")
                return 0
            research_task_id = result.get("task_id")
            research_mode_used = mode
            print(f"    task_id: {research_task_id}")

            status = await client.research.wait_for_completion(
                nb.id, research_task_id, timeout=timeout, interval=10
            )

            discovered = status.get("sources", [])
            web_only = [
                s for s in discovered
                if s.get("result_type") in (1, None)
                and (s.get("url") or "").startswith("http")
            ]
            print(f"    discovered: {len(discovered)} entries ({len(web_only)} importable)")

            if web_only:
                imported = await client.research.import_sources(
                    nb.id, research_task_id, web_only[:30]
                )
                return len(imported)
            return 0

        # Attempt 1: deep mode, 30 min timeout
        try:
            research_imported = await try_research("deep", timeout=1800)
        except Exception as e:
            err_log.add("web_research_deep", e)
            research_imported = 0

        # Attempt 2: fast mode fallback if deep didn't deliver
        if research_imported < 1:
            print("→ Deep mode returned 0 — trying fast mode...")
            try:
                research_imported = await try_research("fast", timeout=600)
            except Exception as e:
                err_log.add("web_research_fast", e)
                research_imported = 0

        # Attempt 3 (Fallback C): add Rin's pre-curated web URLs directly
        if research_imported < 5 and web_fallback_urls:
            print(f"→ Web research insufficient ({research_imported} sources) — "
                  f"adding {len(web_fallback_urls)} fallback URLs directly...")
            for url in web_fallback_urls:
                try:
                    await client.sources.add_url(nb.id, url, wait=True)
                    web_fallback_added += 1
                    print(f"  ✓ {url}")
                except Exception as e:
                    err_log.add(f"web_fallback_add[{url}]", e, severity="warning")
            print(f"  added {web_fallback_added}/{len(web_fallback_urls)} fallback URLs")

        if research_imported == 0 and web_fallback_added == 0:
            err_log.warn(
                "no_web_sources",
                "Neither NotebookLM research nor fallback URLs produced any web sources. "
                "Notebook will only contain YouTube videos."
            )

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
            title = getattr(s, "title", "Untitled")
            sources_data.append({
                "id": i,
                "title": title,
                "url": url,
                "type": getattr(s, "type", "unknown"),
                # FIX #3: check BOTH url and title — NotebookLM sometimes stores
                # YouTube URL in `title` field and leaves `url` as null
                "kind": "youtube" if is_youtube(url, title) else "web",
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
        # generate_mind_map returns dict (not GenerationStatus). No polling.
        # Reject null mindmap — NotebookLM returns {"mind_map": null} when the
        # notebook has insufficient indexed content (e.g. only video sources).
        print("→ Generating mind map...")
        mindmap_path: Path | None = output_dir / "mindmap.json"

        def _is_valid_mindmap(d: dict | None) -> bool:
            if not d:
                return False
            mm = d.get("mind_map")
            return mm is not None and bool(mm)  # truthy + not None

        async def _generate_mindmap_with_retry(attempts: int = 2) -> dict | None:
            for i in range(attempts):
                try:
                    d = await client.artifacts.generate_mind_map(nb.id)
                    if _is_valid_mindmap(d):
                        return d
                    err_log.warn(
                        f"mind_map_empty_try{i+1}",
                        f"got null/empty mind_map (attempt {i+1}/{attempts})"
                    )
                    if i + 1 < attempts:
                        print(f"  retrying mind map in 20s...")
                        await asyncio.sleep(20)
                except Exception as e:
                    err_log.add(f"mind_map_try{i+1}", e)
                    if i + 1 < attempts:
                        await asyncio.sleep(10)
            return None

        try:
            mm_dict = await _generate_mindmap_with_retry(attempts=2)
            if mm_dict is None:
                # Don't save a useless file — Builder will skip section gracefully
                mindmap_path = None
                err_log.warn(
                    "mind_map_skipped",
                    "All attempts returned empty mind_map — likely insufficient "
                    "notebook content. Skipping mindmap.json (Builder will omit section)."
                )
            else:
                # Try canonical download first, fall back to writing the dict
                try:
                    await client.artifacts.download_mind_map(nb.id, str(mindmap_path))
                    print(f"  ✓ saved (download_mind_map): {mindmap_path}")
                except Exception as e_dl:
                    err_log.warn("mind_map_download", f"download failed: {e_dl}")
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
            f"**Web research:** mode={research_mode_used or 'failed'}, "
            f"imported={research_imported}, fallback_added={web_fallback_added}",
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
                    "research_mode_used": research_mode_used,
                    "research_imported": research_imported,
                    "web_fallback_added": web_fallback_added,
                    "youtube_added": yt_added,
                    "total_sources": len(sources_data),
                    "web_sources": web_count,
                    "video_sources": yt_count,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        # Note: errors.log is flushed by the outer main() finally block (P0).
        print()
        print(f"✓ Done. Output in {output_dir}")
        return 0


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="run slug")
    parser.add_argument("--brief", required=True, help="path to brief.md")
    parser.add_argument("--output-dir", required=True, help="where to write outputs")
    parser.add_argument("--youtube", default="", help="comma-separated YouTube URLs")
    parser.add_argument("--web-urls", dest="web_urls", default="",
                        help="comma-separated web URLs (fallback if NotebookLM auto web research fails)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    # ErrorLog writes a startup marker IMMEDIATELY — so even instant crashes leave evidence
    err_log = ErrorLog(output_dir)

    exit_code = 1
    try:
        exit_code = await _main_inner(args, err_log)
    except BaseException as e:
        # Catch EVERYTHING — including KeyboardInterrupt, SystemExit
        err_log.add("fatal_uncaught", e, severity="error")
        exit_code = 99
        # Re-raise non-Exception (KeyboardInterrupt etc) after flushing
        if not isinstance(e, Exception):
            err_log.flush()
            raise
    finally:
        # P0: guaranteed flush — errors.log ALWAYS lands on disk
        path = err_log.flush()
        if path and err_log.entries:
            print(f"\n⚠ {len(err_log.entries)} issue(s) logged to {path}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
