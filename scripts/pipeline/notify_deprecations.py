#!/usr/bin/env python3
"""Keep one GitHub issue open per deprecated mod (notification only).

Reads detect.json. For every deprecated package (pinned directly, or pulled
in by a pinned version) it makes sure exactly one open issue labelled
`mod-deprecated` exists, identified by a hidden marker
`<!-- deprecated:Namespace-Name -->`. Issues whose package is no longer
deprecated, or no longer used by the pack, are closed.

Nothing in the pack is changed: replacing or dropping a deprecated mod is a
human decision.

Usage: notify_deprecations.py ci-out/detect.json [--dry-run]
Needs: gh (GH_TOKEN with issues:write), GH_REPO or GITHUB_REPOSITORY.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess

LABEL = "mod-deprecated"
MARKER = re.compile(r"<!-- deprecated:([A-Za-z0-9_]+-[A-Za-z0-9_]+) -->")


def gh(*args: str, dry: bool = False) -> str:
    if dry and args[:2] != ("issue", "list"):
        print("DRY-RUN gh", " ".join(args))
        return ""
    return subprocess.run(["gh", *args], check=True, capture_output=True,
                          text=True).stdout


def body(d: dict) -> str:
    lines = [f"<!-- deprecated:{d['mod']} -->",
             f"**[{d['mod']}]({d['url']})** is marked deprecated on Thunderstore."]
    if d["via"]:
        lines.append("")
        lines.append("It isn't pinned directly; it is a dependency of: "
                     + ", ".join(f"`{v}`" for v in d["via"]) + ".")
    else:
        lines.append("")
        lines.append(f"Pinned version: `{d['version']}`.")
    lines += [
        "",
        "Deprecated packages still install and keep working, but they get no",
        "further fixes, and a future Valheim update may break them. Decide",
        "whether to keep it, replace it or drop it.",
        "",
        "_This issue is maintained by the mod-maintenance workflow and closes "
        "itself once the package is no longer deprecated or no longer used._",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("detect")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if "GH_REPO" not in os.environ and "GITHUB_REPOSITORY" in os.environ:
        os.environ["GH_REPO"] = os.environ["GITHUB_REPOSITORY"]

    deprecated = {d["mod"]: d for d in json.load(open(a.detect))["deprecated"]}
    # Listing is read-only, so it runs even in --dry-run when a repo is known.
    raw = "[]"
    if os.environ.get("GH_REPO") or not a.dry_run:
        raw = gh("issue", "list", "--label", LABEL, "--state", "open",
                 "--limit", "100", "--json", "number,body", dry=a.dry_run)
    open_issues: dict[str, int] = {}
    for issue in json.loads(raw or "[]"):
        m = MARKER.search(issue["body"] or "")
        if m:
            open_issues[m.group(1)] = issue["number"]

    if deprecated:
        gh("label", "create", LABEL, "--force", "--color", "B60205",
           "--description", "A mod the pack uses is deprecated on Thunderstore",
           dry=a.dry_run)

    for mod, d in deprecated.items():
        if mod in open_issues:
            print(f"#{open_issues[mod]} already open for {mod}")
            continue
        gh("issue", "create", "--label", LABEL,
           "--title", f"Deprecated on Thunderstore: {mod}",
           "--body", body(d), dry=a.dry_run)
        print(f"opened issue for {mod}")

    for mod, number in open_issues.items():
        if mod not in deprecated:
            gh("issue", "close", str(number), "--reason", "completed", "--comment",
               f"`{mod}` is no longer deprecated, or the pack no longer uses it.",
               dry=a.dry_run)
            print(f"closed #{number} ({mod})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
