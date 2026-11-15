#!/usr/bin/env python3
"""Checks that keep the player changelog clean.

Errors (exit 1):
  - a CHANGELOG.md heading that isn't `## [X.Y.Z] - YYYY-MM-DD`
  - a .changes/vX.Y.Z.md whose heading doesn't match its file name
  - CHANGELOG.md out of date with .changes/ (run `changie merge`)
  - thunderstore.toml versionNumber != the newest .changes/ version
  - an unreleased note with an unknown kind or an empty body
  - with --base REF: mod pins or config/ changed since REF but no new note
    in .changes/unreleased/ (set SKIP_CHANGELOG=1 to allow, e.g. for a
    `skip-changelog` PR label)

Warnings: developer jargon in player-facing text.

Usage: changelog_lint.py [--base REF] [--changie PATH]
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import tslib

REPO = tslib.REPO
CHANGES = REPO / ".changes"
KINDS = {"Heads-up", "Added", "Changed", "Fixed", "Removed"}
HEADING = re.compile(r"^## \[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}$")
JARGON = re.compile(
    r"\b(DLL|GUID|ZDOs?|RPCs?|Harmony|strings -e|BepInPlugin|\w+\.(cfg|sh|py|yaml|toml)|"
    r"BepInEx/|config/|scripts/|LogOutput)\b")


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True,
                          text=True, check=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    ap.add_argument("--changie", default=os.environ.get("CHANGIE", "changie"))
    a = ap.parse_args()
    errors, warnings = [], []

    changelog = (REPO / "CHANGELOG.md").read_text()
    for n, line in enumerate(changelog.splitlines(), 1):
        if line.startswith("## ") and not HEADING.match(line):
            errors.append(f"CHANGELOG.md:{n}: heading must be '## [X.Y.Z] - YYYY-MM-DD': {line!r}")

    versions = []
    for p in sorted(CHANGES.glob("v*.md")):
        first = p.read_text().splitlines()[0] if p.read_text() else ""
        ver = p.stem[1:]
        versions.append(ver)
        if not first.startswith(f"## [{ver}] - ") or not HEADING.match(first):
            errors.append(f"{p.relative_to(REPO)}: heading {first!r} doesn't match file name")
        for m in JARGON.finditer(p.read_text()):
            warnings.append(f"{p.relative_to(REPO)}: developer jargon {m.group()!r}")

    if versions:
        newest = max(versions, key=tslib.vkey)
        toml_ver = tslib.load_toml()["package"]["versionNumber"]
        if toml_ver != newest:
            errors.append(f"thunderstore.toml versionNumber {toml_ver} != newest .changes/ version {newest}")

    try:
        merged = subprocess.run([a.changie, "merge", "--dry-run"], cwd=REPO,
                                capture_output=True, text=True, check=True).stdout
        if merged.strip() != changelog.strip():
            errors.append("CHANGELOG.md is out of date with .changes/ -- run `changie merge`")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        warnings.append(f"skipped the CHANGELOG.md freshness check (changie: {e})")

    notes = sorted((CHANGES / "unreleased").glob("*.yaml"))
    for p in notes:
        text = p.read_text()
        kind = re.search(r"^kind:\s*(.+)$", text, re.M)
        body = re.search(r"^body:\s*(.*)$", text, re.M)
        if not kind or kind.group(1).strip() not in KINDS:
            errors.append(f"{p.relative_to(REPO)}: kind must be one of {sorted(KINDS)}")
        if not body or not body.group(1).strip().strip("'\"|>"):
            errors.append(f"{p.relative_to(REPO)}: empty body")
        elif JARGON.search(text):
            warnings.append(f"{p.relative_to(REPO)}: developer jargon "
                            f"{JARGON.search(text).group()!r} -- write for players")

    if a.base:
        changed = git("diff", "--name-only", f"{a.base}...HEAD").split()
        old_deps = tslib.pinned_deps(tslib.git_show(a.base, "thunderstore.toml"))
        deps_changed = old_deps != tslib.pinned_deps()
        cfg_changed = any(f.startswith("config/") for f in changed)
        added_notes = [f for f in git("diff", "--name-only", "--diff-filter=A",
                                      f"{a.base}...HEAD").split()
                       if f.startswith(".changes/unreleased/") and f.endswith(".yaml")]
        if (deps_changed or cfg_changed) and not added_notes and not os.environ.get("SKIP_CHANGELOG"):
            errors.append("mod pins or config/ changed but no note was added in "
                          ".changes/unreleased/ (`make change`), or label the PR skip-changelog")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"changelog-lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
