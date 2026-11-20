#!/usr/bin/env python3
"""Compose the rolling maintenance PR description from ci-out/.

Usage: pr_body.py --ci-out ci-out --run-url URL --out body.md
                  [--previous old-body.md] [--base origin/main]
Sets the step outputs `title` and `draft` (true when the verify boot failed).

With --previous (append mode: the bot adds to a branch it doesn't rewrite),
this run's batch goes on top and the earlier batches from the open PR's
description are kept below it under "Earlier in this PR". The title counts
every mod bumped on the branch since --base, not only this batch.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import tslib

LIMIT = 60000   # GitHub's PR body limit is 65536 characters
EARLIER = "<!-- maintenance:earlier -->"
FOOTER = "<!-- maintenance:footer -->"
FP_RE = re.compile(r"^<!-- maintenance:fp=[0-9a-f]* -->\n?", re.M)
# Footers written before FOOTER existed: "---" then one "One commit per mod" line.
LEGACY_FOOTER_RE = re.compile(r"\n*---\nOne commit per mod:[^\n]*\n?")
DETAILS_RE = re.compile(r"\n*<details>.*?</details>", re.S)


def load(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def earlier_batches(previous: str) -> str:
    """The batches in an open PR's description, without its marker and footer."""
    text = FP_RE.sub("", previous)
    if FOOTER in text:
        text = text.split(FOOTER, 1)[0]
    text = LEGACY_FOOTER_RE.sub("\n", text).strip()
    if EARLIER in text:
        latest, older = text.split(EARLIER, 1)
        older = re.sub(r"^\s*# Earlier in this PR\s*", "", older).strip()
        latest = re.sub(r"\n*---\s*$", "", latest.strip())
        text = latest + "\n\n" + older
    return text.strip()


def bumped_mods(base: str) -> set[str]:
    r = subprocess.run(["git", "log", "--format=%s", f"{base}..HEAD"],
                       capture_output=True, text=True)
    return set(re.findall(r"^chore\(deps\): bump (\S+) from", r.stdout, re.M))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ci-out", type=Path, default=Path("ci-out"))
    ap.add_argument("--run-url", default="")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--previous", type=Path,
                    help="the open PR's description, to keep its earlier batches")
    ap.add_argument("--base", default="origin/main")
    a = ap.parse_args()
    d = a.ci_out

    detect = load(d / "detect.json") or {}
    verify = load(d / "boot/verify/report.json")
    ups = detect.get("updates", [])
    fp = detect.get("fingerprint", "")

    n = len(ups)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    parts = [f"<!-- maintenance:fp={fp} -->",
             f"# Batch {today}: {n} update{'s' if n != 1 else ''}", ""]
    summary = d / "agent-summary.md"
    if summary.exists():
        parts.append(summary.read_text().strip())
    else:
        parts += ["## Summary",
                  "Automated update batch. **The agent review did not run** (no "
                  "`CLAUDE_CODE_OAUTH_TOKEN`, or it failed), so check the config "
                  "report's review rows and write the player notes by hand.",
                  "", "| Mod | From -> To | Side |", "|---|---|---|"]
        parts += [f"| [{u['mod']}]({tslib.page_url(u['mod'])}changelog/) | "
                  f"{u['current']} -> {u['latest']} | {u['side']} |" for u in ups]

    parts.append("\n## Headless boot")
    if verify is None:
        parts.append("Not run.")
    else:
        status = "passed" if verify["ok"] else "**failed**: " + "; ".join(verify["problems"])
        parts.append(f"Verify boot {status} -- {len(verify['plugins_loaded'])} plugins, "
                     f"ready in {verify['seconds_to_ready']} s.")
        if verify["fatal"]:
            parts += ["", "```text", "\n---\n".join(verify["fatal"][:5]), "```"]
    v = detect.get("valheim", {})
    if v.get("current"):
        parts.append(f"\nValheim dedicated server build `{v['current']}`"
                     + (f" (last verified `{v['verified'] or 'never'}`)." if v.get("changed") else "."))

    if detect.get("waiting"):
        parts.append(f"\n## Waiting (released less than {detect['cooldown_hours']:.0f} h ago)")
        parts += [f"- {w['mod']} {w['current']} -> {w['latest']} ({w['age_hours']:.0f} h old)"
                  for w in detect["waiting"]]
    if detect.get("deprecated"):
        parts.append("\n## Deprecated on Thunderstore")
        parts += [f"- [{x['mod']}]({x['url']})" + (f" (needed by {', '.join(x['via'])})" if x["via"] else "")
                  for x in detect["deprecated"]]
        parts.append("Each has its own `mod-deprecated` issue.")

    for title, f in (("Keybinds", "keybinds.md"), ("Config migration", "config-report.md")):
        p = d / f
        if p.exists() and p.read_text().strip():
            parts += [f"\n<details><summary>{title}</summary>\n", p.read_text().strip(), "\n</details>"]

    earlier = ""
    if a.previous and a.previous.exists():
        earlier = earlier_batches(a.previous.read_text())
    if earlier:
        parts += ["\n---\n", EARLIER, "# Earlier in this PR", "", earlier]

    parts.append("\n" + FOOTER + "\n---\nOne commit per mod: drop any you don't want with `git revert`. "
                 "Push your own commits or add the `hold` label and the bot will only add to "
                 "this branch, never rewrite it. Merge with a **merge commit** (not squash) "
                 "so the release notes keep the per-mod commits."
                 + (f" Evidence and logs: [workflow run]({a.run_url})." if a.run_url else ""))

    body = "\n".join(parts)
    if len(body) > LIMIT and earlier:
        # Earlier batches lose their collapsed tables first; this run keeps its own.
        head, tail = body.split(EARLIER, 1)
        body = head + EARLIER + DETAILS_RE.sub("", tail)
    if len(body) > LIMIT:
        body = body[:LIMIT] + "\n\n_[truncated -- full reports are in the workflow artifacts]_"
    a.out.write_text(body + "\n")

    total = max(len(bumped_mods(a.base)), n)
    title = (f"Mod maintenance: {total} update{'s' if total != 1 else ''}" if total
             else f"Mod maintenance: verify Valheim build {v.get('current', '')}")
    draft = "true" if verify is not None and not verify["ok"] else "false"
    tslib.write_output(title=title, draft=draft)
    tslib.log(f"title: {title} (draft: {draft})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
