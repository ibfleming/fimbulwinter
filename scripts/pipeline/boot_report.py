#!/usr/bin/env python3
"""Turn a boot-test LogOutput.log into report.json; exit 1 if the boot failed.

A boot fails when the server never started accepting connections, when a
plugin that is installed did not load, or when the log contains an error
that means a mod is broken against this game build. Headless-graphics noise
(missing shaders, video decode, intro cinematic) is ignored.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import tslib

FATAL = re.compile(
    r"MissingMethodException|MissingFieldException|TypeLoadException|"
    r"ReflectionTypeLoadException|NullReferenceException|"
    r"Could not load \[|missing dependenc|is incompatible with|"
    r"Error loading|Exception in Awake|HarmonyException|InvalidProgramException")
NOISE = re.compile(
    r"shader|VideoComposite|VideoDecode|video decode|intro cinematic|"
    r"AsyncResourceUpload|custom render path|libParty", re.I)
LOADED = re.compile(r"Loading \[(.+?) ([0-9][^\]]*)\]")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True)
    ap.add_argument("--ready", required=True)
    ap.add_argument("--seconds", type=int, default=0)
    ap.add_argument("--log", required=True)
    ap.add_argument("--stdout")
    ap.add_argument("--plugins", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    bep = Path(a.log).read_text(errors="replace").splitlines()
    loaded = [f"{m.group(1)} {m.group(2)}" for m in map(LOADED.search, bep) if m]
    # Errors can be in either log: Unity's own output only reaches
    # LogOutput.log when BepInEx.cfg enables it.
    lines = bep + (Path(a.stdout).read_text(errors="replace").splitlines()
                   if a.stdout and Path(a.stdout).exists() else [])

    # Every installed package dir that declares a BepInPlugin should load.
    plugins = Path(a.plugins)
    expected = {}
    if plugins.is_dir():
        for d in sorted(p for p in plugins.iterdir() if p.is_dir()):
            guids = tslib.package_guids(d)
            if guids:
                expected[d.name] = guids

    fatal, errors = [], []
    for i, line in enumerate(lines):
        if FATAL.search(line):
            ctx = lines[max(0, i - 2):i + 6]
            fatal.append("\n".join(ctx))
        elif ("[Error" in line or "[Fatal" in line) and not NOISE.search(line):
            errors.append(line)

    ready = a.ready == "true"
    problems = []
    if not ready:
        problems.append("server never started accepting connections")
    if len(loaded) < len(expected):
        problems.append(f"{len(loaded)} plugins loaded, {len(expected)} installed")
    if fatal:
        problems.append(f"{len(fatal)} fatal error(s) in the log")

    report = {
        "mode": a.mode, "ok": not problems, "problems": problems,
        "ready": ready, "seconds_to_ready": a.seconds,
        "plugins_loaded": loaded, "packages_installed": sorted(expected),
        "fatal": fatal[:20], "other_errors": sorted(set(errors))[:40],
    }
    Path(a.out).write_text(json.dumps(report, indent=2) + "\n")
    status = "OK" if report["ok"] else "FAILED: " + "; ".join(problems)
    tslib.log(f"[BOOT:{a.mode}] {len(loaded)}/{len(expected)} plugins, "
              f"{a.seconds}s to ready -- {status}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
