#!/usr/bin/env python3
"""3-way BepInEx config migration: old defaults, new defaults, shipped values.

For every shipped .cfg the rule per setting is:

  shipped == old default, default changed    -> follow the new default (auto)
  shipped customised, default unchanged      -> keep ours (auto)
  shipped customised, default also changed   -> keep ours, flag for review
  setting the old version wrote, the new not -> drop it, flag for review
                                                (with rename candidates)
  setting neither version wrote headless     -> keep our line (the mod
                                                creates it in a client)
  setting added in the new version           -> add at its default (auto)

Section and key names are compared without zero-width characters (some
mods use them for ordering); the rendered file keeps the names exactly as
the new version writes them, because BepInEx matches names exactly.

"Old default" comes from the old-version harvest when given, otherwise from
the `# Default value:` comment BepInEx wrote into the shipped file.
"New default" comes from a harvest boot of the new version (a fresh config
written by the mod itself, so its values are the defaults).

--apply rewrites the shipped file from the new harvest file (keeping the new
descriptions, ordering and added settings) with our values put back, and
keeps the shipped file's line endings and BOM.

Usage:
  config_diff.py --new HARVEST_DIR [--old HARVEST_DIR] [--shipped config]
                 [--files a.cfg b.cfg] [--apply] [--json out.json] [--md out.md]
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

import tslib

KEYBIND_TYPES = {"KeyboardShortcut", "KeyCode"}
ZERO_WIDTH = re.compile("[\u200b\u200c\u200d\u2060\ufeff]")


def read(path: Path) -> tuple[str, bool, str]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig", errors="replace")
    nl = "\r\n" if text.count("\r\n") > text.count("\n") / 2 else "\n"
    return text, bom, nl


def norm(cfg: dict) -> dict:
    """Key settings by section and key name without zero-width characters.

    Some mods prefix section and key names with zero-width characters to
    control ordering in ConfigurationManager, and a new version may add or
    drop them. BepInEx matches names exactly, so the rendered file always
    uses the names the new version itself writes.
    """
    return {(ZERO_WIDTH.sub("", sec), ZERO_WIDTH.sub("", key)): v
            for (sec, key), v in cfg.items()}


def diff_file(rel: str, shipped: Path, new: Path | None, old: Path | None) -> dict:
    s_text, bom, nl = read(shipped)
    s = norm(tslib.parse_cfg(s_text))
    res = {"file": rel, "status": "ok", "changes": [], "review": 0, "auto": 0}
    if new is None or not new.exists():
        res["status"] = "not-generated"
        return res
    n_text, _, _ = read(new)
    n = norm(tslib.parse_cfg(n_text))
    o = norm(tslib.parse_cfg(read(old)[0])) if old and old.exists() else None

    final: dict[tuple[str, str], str] = {}
    for k, nv in n.items():
        typ = nv["type"] or (s.get(k) or {}).get("type")
        entry = {"section": k[0], "key": k[1], "type": typ,
                 "keybind": typ in KEYBIND_TYPES, "new_default": nv["value"]}
        if k not in s:
            entry.update(kind="added", result=nv["value"], review=False)
            res["changes"].append(entry)
            final[k] = nv["value"]
            continue
        sv = s[k]["value"]
        od = (o[k]["value"] if o and k in o else s[k]["default"])
        if od is None:
            od = sv
        entry.update(shipped=sv, old_default=od)
        if sv == od:
            final[k] = nv["value"]
            if nv["value"] != od:
                entry.update(kind="default-changed", result=nv["value"], review=False)
                res["changes"].append(entry)
        else:
            final[k] = sv
            if nv["value"] != od:
                entry.update(kind="customised-default-changed", result=sv, review=True)
                res["changes"].append(entry)

    added_in_section: dict[str, list[str]] = {}
    for k in n:
        if k not in s:
            added_in_section.setdefault(k[0], []).append(k[1])
    keep: list[tuple[str, str, str]] = []      # (section, key, value) to re-add
    for k, sv in s.items():
        if k in n:
            continue
        base = {"section": k[0], "key": k[1], "type": sv["type"],
                "keybind": sv["type"] in KEYBIND_TYPES, "shipped": sv["value"]}
        if o is None or k not in o:
            # Neither version wrote it on a headless server (or there is no
            # old harvest to tell): the mod probably creates it lazily in a
            # client. Keep our line; an unused line is harmless, a dropped
            # customisation is not.
            keep.append((k[0], k[1], sv["value"]))
            res["changes"].append({**base, "kind": "kept-not-generated",
                                   "result": sv["value"], "review": False})
            continue
        cands = difflib.get_close_matches(k[1], added_in_section.get(k[0], []), n=3, cutoff=0.5)
        if not cands:   # moved to another section?
            cands = [f"[{sec}] {key}" for sec, key in n if key == k[1]]
        res["changes"].append({**base, "kind": "removed",
                               "customised": sv["value"] != sv["default"],
                               "rename_candidates": cands, "review": True})

    zw_new, zw_ours = bool(ZERO_WIDTH.search(n_text)), bool(ZERO_WIDTH.search(s_text))
    if zw_new != zw_ours:
        res["changes"].append({
            "section": "*", "key": "*", "type": None, "keybind": False,
            "kind": "zero-width-names", "review": True,
            "mod_writes": zw_new, "ours_has": zw_ours})

    res["review"] = sum(1 for c in res["changes"] if c["review"])
    res["auto"] = sum(1 for c in res["changes"] if not c["review"]
                      and c["kind"] != "kept-not-generated")
    res["kept"] = len(keep)
    res["_render"] = (n_text, final, keep, bom, nl)
    return res


def render(n_text: str, final: dict, keep: list, bom: bool, nl: str) -> bytes:
    """New harvest text with our values put back and kept lines re-added."""
    out: list[str] = []
    section, pending = "", {}
    for sec, key, val in keep:
        pending.setdefault(sec, []).append(f"{key} = {val}")

    def flush(sec: str) -> None:
        for line in pending.pop(sec, []):
            out.append(line)
            out.append("")

    for raw in n_text.splitlines():
        line = raw.rstrip("\r")
        m = re.match(r"^\[(.+)\]\s*$", line)
        if m:
            flush(section)
            section = ZERO_WIDTH.sub("", m.group(1))
        elif line and not line.lstrip().startswith("#"):
            m = re.match(r"^([^#;=][^=]*?)\s*=\s?(.*)$", line)
            k = (section, ZERO_WIDTH.sub("", m.group(1).strip())) if m else None
            if k in final:
                line = f"{m.group(1).strip()} = {final[k]}"
        out.append(line)
    flush(section)
    for sec in list(pending):          # sections the new file doesn't have
        out += ["", f"[{sec}]", ""]
        flush(sec)
    while out and out[-1] == "":
        out.pop()
    text = nl.join(out) + nl
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def to_md(results: list[dict]) -> str:
    rows = ["| File | Setting | Change | Result | Review |", "|---|---|---|---|---|"]
    for r in results:
        if r["status"] == "not-generated":
            rows.append(f"| `{r['file']}` | - | not generated by a headless server "
                        f"(client-only mod?) - check in a client | - | yes |")
        for c in r["changes"]:
            name = f"`[{c['section']}] {c['key']}`" + (" (keybind)" if c["keybind"] else "")
            if c["kind"] == "added":
                what, result = "new setting", f"`{c['result']}` (default)"
            elif c["kind"] == "default-changed":
                what, result = f"default `{c['old_default']}` -> `{c['new_default']}`", f"`{c['result']}`"
            elif c["kind"] == "customised-default-changed":
                what = (f"default `{c['old_default']}` -> `{c['new_default']}`, "
                        f"ours is `{c['shipped']}`")
                result = f"`{c['result']}` (kept ours)"
            elif c["kind"] == "kept-not-generated":
                continue        # unchanged for players; counted in the summary
            elif c["kind"] == "zero-width-names":
                rows.append(f"| `{r['file']}` | (names) | the mod "
                            f"{'writes' if c['mod_writes'] else 'does not write'} zero-width "
                            f"characters in section/key names, our file "
                            f"{'has' if c['ours_has'] else 'does not'}; BepInEx matches "
                            f"names exactly | new file uses the mod's names | yes |")
                continue
            else:
                cands = ", ".join(f"`{x}`" for x in c["rename_candidates"]) or "none"
                what = f"removed (ours `{c['shipped']}`); rename candidates: {cands}"
                result = "dropped"
            rows.append(f"| `{r['file']}` | {name} | {what} | {result} | "
                        f"{'yes' if c['review'] else ''} |")
    return "\n".join(rows) + "\n" if len(rows) > 2 else "No config changes.\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", required=True, type=Path)
    ap.add_argument("--old", type=Path)
    ap.add_argument("--shipped", type=Path, default=tslib.REPO / "config")
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--json", type=Path)
    ap.add_argument("--md", type=Path)
    a = ap.parse_args()

    files = a.files or [p.name for p in sorted(a.shipped.glob("*.cfg"))]
    results = []
    for rel in files:
        if not rel.endswith(".cfg"):
            continue
        r = diff_file(rel, a.shipped / rel, a.new / rel, a.old / rel if a.old else None)
        results.append(r)
        if a.apply and "_render" in r and r["changes"]:
            data = render(*r["_render"])
            if ZERO_WIDTH.search(data.decode("utf-8-sig")):
                tslib.log(f"WARNING {rel}: zero-width characters in the new file")
            (a.shipped / rel).write_bytes(data)
            tslib.log(f"applied {rel}: {r['auto']} auto, {r['review']} for review")

    for r in results:
        r.pop("_render", None)
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(results, indent=2) + "\n")
    md = to_md(results)
    if a.md:
        a.md.parent.mkdir(parents=True, exist_ok=True)
        a.md.write_text(md)
    if not a.json and not a.md:
        print(md, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
