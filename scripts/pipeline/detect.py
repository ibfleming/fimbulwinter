#!/usr/bin/env python3
"""Detect pending maintenance work (no AI, no side effects).

Checks every pinned dependency against Thunderstore and reports:
  updates     newer version available and at least --cooldown-hours old
  waiting     newer version available but still inside the cooldown
  deprecated  pinned mods, or anything a pinned version depends on, that
              Thunderstore marks deprecated
  valheim     the current public Valheim dedicated-server build vs. the last
              build this repo was verified on (ci/valheim-build)

Writes JSON to --out and, under GitHub Actions, these step outputs:
  has_work, urgent, fingerprint, update_count, deprecated_count

Usage:
  detect.py [--out ci-out/detect.json] [--cooldown-hours 48]
            [--valheim-build ID] [--extra-dep Namespace-Name=1.0.0 ...]

--extra-dep adds a dependency for this run only (testing, e.g. a known
deprecated package such as Therzie-Warfare).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import tslib


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ci-out/detect.json")
    ap.add_argument("--cooldown-hours", type=float, default=48)
    ap.add_argument("--valheim-build", default="")
    ap.add_argument("--extra-dep", action="append", default=[])
    a = ap.parse_args()

    deps = tslib.pinned_deps()
    for e in a.extra_dep:
        k, _, v = e.partition("=")
        deps[k] = v

    now = tslib.now_utc()
    updates, waiting, deprecated, missing = [], [], [], []
    transitive: dict[str, list[str]] = {}

    for mod, pinned in deps.items():
        pkg = tslib.package(mod)
        if pkg is None:
            tslib.log(f"{mod:50} NOT FOUND")
            missing.append(mod)
            continue
        if pkg.get("is_deprecated"):
            deprecated.append({"mod": mod, "version": pinned, "via": None,
                               "url": tslib.page_url(mod)})
        latest = pkg["latest"]["version_number"]
        if tslib.vkey(latest) > tslib.vkey(pinned):
            released = tslib.parse_time(pkg["latest"]["date_created"])
            age = (now - released).total_seconds() / 3600
            entry = {"mod": mod, "current": pinned, "latest": latest,
                     "side": tslib.side(mod),
                     "released": pkg["latest"]["date_created"],
                     "age_hours": round(age, 1)}
            (updates if age >= a.cooldown_hours else waiting).append(entry)
            tslib.log(f"{mod:50} {pinned} -> {latest} ({age:.0f}h old)")
        else:
            tslib.log(f"{mod:50} ok {pinned}")
        # Transitive deps of the *pinned* version, not of latest.
        info = tslib.version_info(mod, pinned) or {}
        for dep in info.get("dependencies", []):
            full, _ = tslib.split_dep(dep)
            if full not in deps:
                transitive.setdefault(full, []).append(mod)

    for full, via in sorted(transitive.items()):
        pkg = tslib.package(full)
        if pkg and pkg.get("is_deprecated"):
            deprecated.append({"mod": full, "version": None, "via": sorted(via),
                               "url": tslib.page_url(full)})

    verified_file = tslib.REPO / "ci/valheim-build"
    verified = verified_file.read_text().strip() if verified_file.exists() else ""
    current = a.valheim_build.strip()
    valheim = {"verified": verified, "current": current,
               "changed": bool(current) and current != verified}

    # The fingerprint covers what the bot would act on; a waiting update
    # doesn't change it until it matures.
    fp_src = json.dumps({
        "u": sorted((u["mod"], u["latest"]) for u in updates),
        "d": sorted(d["mod"] for d in deprecated),
        "v": current if valheim["changed"] else "",
    }, sort_keys=True)
    fingerprint = hashlib.sha256(fp_src.encode()).hexdigest()[:16]

    result = {
        "generated": now.isoformat(timespec="seconds"),
        "cooldown_hours": a.cooldown_hours,
        "updates": updates, "waiting": waiting,
        "deprecated": deprecated, "missing": missing,
        "valheim": valheim, "fingerprint": fingerprint,
        "urgent": bool(deprecated) or valheim["changed"],
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")

    has_work = bool(updates) or valheim["changed"]
    tslib.write_output(has_work=str(has_work).lower(),
                       urgent=str(result["urgent"]).lower(),
                       fingerprint=fingerprint,
                       update_count=len(updates),
                       deprecated_count=len(deprecated))
    tslib.log(f"\nupdates={len(updates)} waiting={len(waiting)} "
              f"deprecated={len(deprecated)} valheim_changed={valheim['changed']} "
              f"fingerprint={fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
