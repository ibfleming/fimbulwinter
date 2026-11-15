#!/usr/bin/env python3
"""Generated parts of the release notes (no AI).

  prep     Before `changie batch`: writes .changes/unreleased/header.md
           (the optional player summary, then the computed "Do I need to
           update?" line) and footer.md (mod updates, key changes, link to
           the technical notes), from the diff between --from and HEAD.
  readme   Rewrites the README "What's new" block from the newest
           .changes/v*.md.
  github   Writes the GitHub Release body: the player notes, mod updates
           with links to each mod's changelog, the key-level config diff,
           and the git-cliff commit log ("Under the hood").
  level    Prints the changie batch argument for the next release: auto
           if there are notes, otherwise patch.

Usage:
  release_notes.py prep [--from REF] [--repo-url URL]
  release_notes.py readme
  release_notes.py github --version X.Y.Z [--from REF] [--cliff PATH] --out FILE
  release_notes.py level
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

import tslib

REPO_URL = "https://github.com/ibfleming/fimbulwinter"
CHANGES = tslib.REPO / ".changes"
UNRELEASED = CHANGES / "unreleased"
README = tslib.REPO / "README.md"
START, END = "<!-- whats-new:start -->", "<!-- whats-new:end -->"


def last_tag() -> str | None:
    r = subprocess.run(["git", "-C", str(tslib.REPO), "describe", "--tags", "--abbrev=0",
                        "--match", "v[0-9]*"], capture_output=True, text=True)
    return r.stdout.strip() or None


def base_ref(given: str | None) -> str:
    if given:
        return given
    tag = last_tag()
    if tag:
        return tag
    return subprocess.run(["git", "-C", str(tslib.REPO), "rev-list", "--max-parents=0", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.split()[0]


def mod_changes(ref: str) -> list[dict]:
    old = tslib.pinned_deps(tslib.git_show(ref, "thunderstore.toml"))
    new = tslib.pinned_deps()
    out = []
    for mod in list(new) + [m for m in old if m not in new]:
        o, n = old.get(mod), new.get(mod)
        if o != n:
            out.append({"mod": mod, "old": o, "new": n, "side": tslib.side(mod)})
    return out


def pretty(mod: str) -> str:
    return mod.split("-", 1)[1].replace("_", " ")


def need_update(changes: list[dict], heads_up: bool) -> str:
    sides = {c["side"] for c in changes}
    if "both" in sides:
        return ("**Do I need to update?** Yes. The server and every player need this "
                "version; mismatched installs can be refused when joining.")
    if "client" in sides:
        return ("**Do I need to update?** Recommended. Only player-side mods changed; "
                "you can still join without updating, but you won't get the changes.")
    if "server" in sides:
        return ("**Do I need to update?** No. Only the server changed; players don't "
                "need to do anything.")
    if heads_up:
        return "**Do I need to update?** See the heads-up below."
    return "**Do I need to update?** Only if you want the changes below."


def keybind_changes(ref: str) -> str:
    r = subprocess.run(["python3", str(Path(__file__).with_name("keybind_audit.py")),
                        "changes", "--from", ref], capture_output=True, text=True, check=True)
    return r.stdout.strip()


def cmd_prep(a) -> int:
    ref = base_ref(a.ref)
    changes = mod_changes(ref)
    heads_up = any("kind: Heads-up" in p.read_text() for p in UNRELEASED.glob("*.yaml"))
    summary_file = UNRELEASED / "summary.md"
    header = []
    if summary_file.exists():
        header.append(summary_file.read_text().strip())
        summary_file.unlink()
    header.append(need_update(changes, heads_up))
    (UNRELEASED / "header.md").write_text("\n\n".join(header))

    footer = [""]
    if changes:
        footer += ["", "### Mod updates"]
        for c in changes:
            if c["old"] is None:
                footer.append(f"- {pretty(c['mod'])}: added {c['new']} ({c['side']})")
            elif c["new"] is None:
                footer.append(f"- {pretty(c['mod'])}: removed ({c['side']})")
            else:
                footer.append(f"- {pretty(c['mod'])} {c['old']} -> {c['new']} ({c['side']})")
    keys = keybind_changes(ref)
    if keys:
        footer += ["", "### Key changes", keys]
    footer += ["", f"Technical details: [GitHub Releases]({a.repo_url}/releases)", ""]
    (UNRELEASED / "footer.md").write_text("\n".join(footer))
    tslib.log(f"prep: {len(changes)} mod change(s) since {ref}")
    return 0


def latest_version_file() -> Path:
    files = sorted(CHANGES.glob("v*.md"), key=lambda p: tslib.vkey(p.stem[1:]))
    if not files:
        raise SystemExit("no .changes/v*.md files")
    return files[-1]


def cmd_readme(_a) -> int:
    path = latest_version_file()
    text = path.read_text()
    head = text.splitlines()[0]
    m = re.match(r"## \[(.+?)\] - (\S+)", head)
    ver, date = m.group(1), m.group(2)
    body = text.split("\n", 1)[1]
    # Summary + "Do I need to update?" + Heads-up only: the README is the
    # landing page, the full list is on the Changelog tab.
    parts = re.split(r"(?m)^### ", body)
    intro = parts[0].strip()
    heads = next((p for p in parts[1:] if p.startswith("Heads-up")), "")
    block = [START, f"## What's new in {ver}", "", f"_Released {date}. Full list on the Changelog tab._", ""]
    if intro:
        block += [intro, ""]
    if heads:
        block += ["**Heads-up**", "", heads.split("\n", 1)[1].strip(), ""]
    block.append(END)
    readme = README.read_text()
    if START not in readme:
        raise SystemExit(f"README.md has no {START} marker")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: "\n".join(block),
                 readme, flags=re.S)
    README.write_text(new)
    tslib.log(f"README What's new -> {ver}")
    return 0


def config_value_diff(ref: str) -> list[str]:
    rows = []
    for p in sorted((tslib.REPO / "config").glob("*.cfg")):
        old_t = tslib.git_show(ref, f"config/{p.name}")
        new = tslib.parse_cfg(p.read_text(encoding="utf-8-sig", errors="replace"))
        if old_t is None:
            rows.append(f"| `{p.name}` | (new file) | | |")
            continue
        old = tslib.parse_cfg(old_t.lstrip("﻿"))
        for k in sorted(set(old) | set(new)):
            o, n = old.get(k, {}).get("value"), new.get(k, {}).get("value")
            if o != n:
                rows.append(f"| `{p.name}` | `[{k[0]}] {k[1]}` | "
                            f"{'`'+o+'`' if o is not None else '(added)'} | "
                            f"{'`'+n+'`' if n is not None else '(removed)'} |")
    return rows


def cmd_github(a) -> int:
    ref = base_ref(a.ref)
    vfile = CHANGES / f"v{a.version}.md"
    player = vfile.read_text().split("\n", 1)[1].strip() if vfile.exists() else ""
    # The player notes already list mod updates; replace that list with a
    # linked table here and drop the self-referencing technical link.
    player = re.sub(r"(?ms)^### Mod updates\n.*?(?=^### |\Z)", "", player)
    player = re.sub(r"(?m)^Technical details:.*$", "", player).strip()
    out = [player, ""]

    changes = mod_changes(ref)
    if changes:
        out += ["## Mod updates", "", "| Mod | From | To | Side |", "|---|---|---|---|"]
        for c in changes:
            link = f"[{c['mod']}]({tslib.page_url(c['mod'])}changelog/)"
            out.append(f"| {link} | {c['old'] or '-'} | {c['new'] or '-'} | {c['side']} |")
        out.append("")
    rows = config_value_diff(ref)
    if rows:
        out += ["## Config changes", "", "<details><summary>"
                f"{len(rows)} setting(s) changed</summary>", "",
                "| File | Setting | Old | New |", "|---|---|---|---|", *rows, "", "</details>", ""]
    if a.cliff:
        r = subprocess.run([a.cliff, "--config", str(tslib.REPO / "cliff.toml"),
                            "--strip", "all", f"{ref}..HEAD"],
                           cwd=tslib.REPO, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            out += ["## Under the hood", "", r.stdout.strip(), ""]
        else:
            tslib.log(f"git-cliff failed: {r.stderr.strip()}")
    Path(a.out).write_text("\n".join(out).strip() + "\n")
    tslib.log(f"wrote {a.out}")
    return 0


def cmd_level(_a) -> int:
    # With notes, changie picks the bump from their kinds (Heads-up, Added
    # and Removed are minor). Mod bumps alone are a patch release.
    print("auto" if any(UNRELEASED.glob("*.yaml")) else "patch")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep")
    p.add_argument("--from", dest="ref")
    p.add_argument("--repo-url", default=REPO_URL)
    sub.add_parser("readme")
    p = sub.add_parser("github")
    p.add_argument("--version", required=True)
    p.add_argument("--from", dest="ref")
    p.add_argument("--cliff")
    p.add_argument("--out", required=True)
    sub.add_parser("level")
    a = ap.parse_args()
    return {"prep": cmd_prep, "readme": cmd_readme, "github": cmd_github,
            "level": cmd_level}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
