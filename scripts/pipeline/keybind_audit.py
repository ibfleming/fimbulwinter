#!/usr/bin/env python3
"""Keybind conflict audit and keybind change list.

Collects every KeyboardShortcut/KeyCode setting in config/*.cfg plus the
admin binds in config/binds.yaml, then:

  audit    lists binds that share a key combination with another bind, and
           bare binds that shadow a vanilla key. With --base REF, only
           conflicts that are new since REF are failures (exit 1); the ones
           already present at REF are reported as known. Binds listed in
           ci/keybinds-accepted.txt are reviewed shares and don't fail
           either.
  changes  lists binds added, removed or moved between --from REF and the
           working tree (or --to REF). With --players the labels use mod and
           setting names; that form goes into the player changelog.

Usage:
  keybind_audit.py audit [--base REF] [--md out.md]
  keybind_audit.py changes --from REF [--to REF] [--players] [--md out.md]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import tslib

KEYBIND_TYPES = {"KeyboardShortcut", "KeyCode"}
ACCEPTED = tslib.REPO / "ci" / "keybinds-accepted.txt"
# Bare vanilla keys a mod must never take over (CLAUDE.md "Keybind Rules").
VANILLA = {"W", "A", "S", "D", "Space", "LeftControl", "E", "Q", "R", "F", "Tab",
           "M", "X", "V", "F5", *(f"Alpha{i}" for i in range(1, 9))}


def files_at(ref: str | None) -> dict[str, str]:
    root = tslib.REPO / "config"
    if ref is None:
        return {p.name: p.read_text(encoding="utf-8-sig", errors="replace")
                for p in root.iterdir() if p.is_file()}
    names = subprocess.run(["git", "-C", str(tslib.REPO), "ls-tree", "--name-only",
                            f"{ref}:config/"], capture_output=True, text=True).stdout.split()
    out = {}
    for n in names:
        t = tslib.git_show(ref, f"config/{n}")
        if t is not None:
            out[n] = t.lstrip("﻿")
    return out


def norm_key(k: str) -> str:
    k = k.strip()
    if len(k) == 1:
        return k.upper() if k.isalpha() else {"`": "BackQuote"}.get(k, f"Alpha{k}" if k.isdigit() else k)
    return k[0].upper() + k[1:]


def binds(ref: str | None) -> dict[str, tuple[str, frozenset]]:
    """{'file [section] key': (main_key, modifiers)}"""
    out: dict[str, tuple[str, frozenset]] = {}
    for name, text in files_at(ref).items():
        if name.endswith(".cfg"):
            for (sec, key), v in tslib.parse_cfg(text).items():
                if v["type"] not in KEYBIND_TYPES:
                    continue
                parts = [p.strip() for p in v["value"].split("+") if p.strip()]
                if not parts or parts[0] in ("None", ""):
                    continue
                out[f"{name} [{sec}] {key}"] = (parts[0], frozenset(parts[1:]))
        elif name == "binds.yaml":
            for i, m in enumerate(re.finditer(r"keys:\s*(.+?)\s*\n\s*command:\s*(.+)", text)):
                parts = [norm_key(p) for p in re.split(r"[,\s]+", m.group(1)) if p]
                out[f"binds.yaml #{i + 1} ({m.group(2).strip()})"] = (parts[0], frozenset(parts[1:]))
    return out


def combo(main: str, mods: frozenset) -> str:
    return " + ".join(sorted(mods) + [main])


def conflicts(b: dict) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for name, (main, mods) in b.items():
        groups[combo(main, mods)].append(name)
        if not mods and main in VANILLA:
            groups[combo(main, mods)].append(f"vanilla {main}")
    # A combination used several times in one file is that mod's own choice
    # (usually different contexts); only cross-file sharing is a conflict.
    out = {}
    for c, names in groups.items():
        owners = {n.split(" ", 1)[0] for n in names}
        if len(owners) > 1:
            # binds.yaml lines bound to the same key are one admin macro.
            out[c] = sorted(set(names))
    return out


def accepted() -> dict[str, set[str]]:
    """{combo: {bind name, ...}} from ci/keybinds-accepted.txt.

    One line per bind: `<keys> | <bind name> | <reason>`, exactly as the
    audit prints them. Each line accepts that one bind sharing that key
    combination, so a further mod joining the same keys is still new."""
    out: dict[str, set[str]] = defaultdict(set)
    if not ACCEPTED.exists():
        return out
    for n, line in enumerate(ACCEPTED.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split(" | ")]
        if len(parts) != 3 or not all(parts):
            raise SystemExit(f"{ACCEPTED.name}:{n}: expected '<keys> | <bind name> | <reason>'")
        out[parts[0]].add(parts[1])
    return out


def cmd_audit(a) -> int:
    head = conflicts(binds(None))
    base = conflicts(binds(a.base)) if a.base else {}
    acc = accepted()
    unresolved = {c: sorted(set(n) - set(base.get(c, [])) - acc.get(c, set()))
                  for c, n in head.items()}
    new = {c: u for c, u in unresolved.items() if u}
    lines = ["| Keys | Bound by | Status |", "|---|---|---|"]
    for c, names in sorted(head.items()):
        if c in new:
            status = "**new**"
        elif a.base and set(names) - set(base.get(c, [])):
            status = "accepted"
        else:
            status = "known"
        lines.append(f"| `{c}` | {'<br>'.join(names)} | {status} |")
    md = "\n".join(lines) + "\n" if head else "No shared key combinations.\n"
    if a.md:
        Path(a.md).write_text(md)
    else:
        print(md, end="")
    if new and a.base:
        tslib.log(f"{len(new)} new keybind conflict(s) since {a.base}")
        tslib.log(f"After review, accept a share by adding its lines to ci/{ACCEPTED.name}:")
        for c, names in sorted(new.items()):
            for n in names:
                tslib.log(f"  {c} | {n} | <reason>")
        return 1
    return 0


def player_label(name: str) -> str:
    """'shudnal.ExtraSlots.cfg [Section] Next row shortcut' ->
    'ExtraSlots: Next row shortcut' (the pinned mod's name when it matches
    the config file name, otherwise the file name's last part)."""
    if name.startswith("binds.yaml"):
        return "Admin binds: " + name.split("(", 1)[-1].rstrip(")")
    file, _, rest = name.partition(" ")
    setting = rest.split("] ", 1)[-1]
    tail = file.removesuffix(".cfg").split(".")[-1]
    flat = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    mod = next((m.split("-", 1)[1].replace("_", " ") for m in tslib.pinned_deps()
                if flat(m.split("-", 1)[1]) == flat(tail)), tail)
    return f"{mod}: {setting}"


def pretty_combo(main: str, mods: frozenset) -> str:
    spaced = lambda k: re.sub(r"(?<=[a-z])(?=[A-Z0-9])", " ", k)
    return " + ".join(spaced(k) for k in sorted(mods) + [main])


def cmd_changes(a) -> int:
    old, new = binds(getattr(a, "from")), binds(a.to)
    rows = []
    for name in sorted(set(old) | set(new)):
        o, n = old.get(name), new.get(name)
        if o == n:
            continue
        if a.players:
            label, fmt = player_label(name), pretty_combo
        else:
            label, fmt = name.replace(".cfg", ""), lambda *c: f"`{combo(*c)}`"
        if o is None:
            rows.append(f"- New: {fmt(*n)} -- {label}" if a.players
                        else f"- New key: {fmt(*n)} ({label})")
        elif n is None:
            rows.append(f"- Removed: {fmt(*o)} -- {label}" if a.players
                        else f"- Removed key: {fmt(*o)} ({label})")
        else:
            rows.append(f"- {fmt(*o)} is now {fmt(*n)} -- {label}" if a.players
                        else f"- {fmt(*o)} -> {fmt(*n)} ({label})")
    md = "\n".join(rows) + "\n" if rows else ""
    if a.md:
        Path(a.md).write_text(md)
    else:
        print(md, end="")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("audit")
    p.add_argument("--base")
    p.add_argument("--md")
    p = sub.add_parser("changes")
    p.add_argument("--from", required=True)
    p.add_argument("--to")
    p.add_argument("--md")
    p.add_argument("--players", action="store_true",
                   help="player-facing labels (mod and setting names, spaced key names)")
    a = ap.parse_args()
    return cmd_audit(a) if a.cmd == "audit" else cmd_changes(a)


if __name__ == "__main__":
    sys.exit(main())
