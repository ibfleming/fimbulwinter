"""Shared helpers for the mod-maintenance pipeline (stdlib only).

Everything here is deterministic: Thunderstore API access, the pinned
dependency list, which side each mod runs on, package download/extract, and
BepInEx .cfg parsing. The CI agent never needs network access because these
scripts fetch everything up front.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
API = "https://thunderstore.io/api/experimental/package"
DOWNLOAD = "https://thunderstore.io/package/download"
# Browser UA: the download CDN rejects obvious bot UAs from datacenter IPs
# (same reason scripts/install-mods.sh uses one).
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0"

LOADER = "denikson-BepInExPack_Valheim"


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# ── Versions ────────────────────────────────────────────────────

def vkey(v: str) -> tuple[int, ...]:
    return tuple(int(p) if p.isdigit() else 0 for p in re.split(r"[.\-+]", v))


def split_dep(dep: str) -> tuple[str, str]:
    """'Namespace-Name-1.2.3' -> ('Namespace-Name', '1.2.3')."""
    full, _, ver = dep.rpartition("-")
    return full, ver


# ── Repo state ──────────────────────────────────────────────────

def load_toml(text: str | None = None) -> dict:
    if text is None:
        text = (REPO / "thunderstore.toml").read_text()
    return tomllib.loads(text)


def pinned_deps(text: str | None = None) -> dict[str, str]:
    return dict(load_toml(text)["package"]["dependencies"])


def git_show(ref: str, path: str) -> str | None:
    r = subprocess.run(["git", "-C", str(REPO), "show", f"{ref}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def _bash_array(path: Path, name: str) -> set[str]:
    text = path.read_text()
    m = re.search(rf"^{name}=\((.*?)^\)", text, re.S | re.M)
    if not m:
        raise SystemExit(f"{name} not found in {path}")
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def _python_set(path: Path, name: str) -> set[str]:
    text = path.read_text()
    m = re.search(rf"^{name} = \{{(.*?)^\}}", text, re.S | re.M)
    if not m:
        raise SystemExit(f"{name} not found in {path}")
    return set(re.findall(r'"([^"]+)"', m.group(1)))


def client_only() -> set[str]:
    return _bash_array(REPO / "scripts/install-mods.sh", "CLIENT_ONLY_MODS")


def server_only() -> set[str]:
    return _python_set(REPO / "scripts/export-profile.sh", "SERVER_ONLY_MODS")


def side(mod: str) -> str:
    """client | server | both -- where the mod is installed."""
    if mod in client_only():
        return "client"
    if mod in server_only():
        return "server"
    return "both"


# ── HTTP ────────────────────────────────────────────────────────

def _get(url: str, *, attempts: int = 3, timeout: int = 30) -> bytes:
    last: Exception | None = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            last = e
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"GET {url} failed: {last}")


def get_json(url: str):
    return json.loads(_get(url))


_pkg_cache: dict[str, dict | None] = {}


def package(full: str) -> dict | None:
    """Package listing (latest version, is_deprecated). None if not found."""
    if full not in _pkg_cache:
        ns, name = full.split("-", 1)
        try:
            _pkg_cache[full] = get_json(f"{API}/{ns}/{name}/")
        except urllib.error.HTTPError:
            _pkg_cache[full] = None
        time.sleep(0.2)
    return _pkg_cache[full]


def version_info(full: str, ver: str) -> dict | None:
    ns, name = full.split("-", 1)
    try:
        return get_json(f"{API}/{ns}/{name}/{ver}/")
    except urllib.error.HTTPError:
        return None


def changelog(full: str, ver: str) -> str:
    ns, name = full.split("-", 1)
    try:
        return get_json(f"{API}/{ns}/{name}/{ver}/changelog/").get("markdown") or ""
    except (urllib.error.HTTPError, RuntimeError):
        return ""


def page_url(full: str) -> str:
    ns, name = full.split("-", 1)
    return f"https://thunderstore.io/c/valheim/p/{ns}/{name}/"


def parse_time(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def now_utc() -> datetime:
    override = os.environ.get("PIPELINE_NOW")
    return parse_time(override) if override else datetime.now(timezone.utc)


# ── Packages on disk ────────────────────────────────────────────

def fetch_package(full: str, ver: str, cache: Path) -> Path:
    """Download and extract a package; returns the extracted directory."""
    dest = cache / f"{full}-{ver}"
    if (dest / ".ok").exists():
        return dest
    ns, name = full.split("-", 1)
    log(f"  download {full} {ver}")
    data = _get(f"{DOWNLOAD}/{ns}/{name}/{ver}/", timeout=300)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            # Normalise Windows separators and refuse path traversal.
            rel = Path(info.filename.replace("\\", "/"))
            if rel.is_absolute() or ".." in rel.parts:
                continue
            target = dest / rel
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(info))
    (dest / ".ok").touch()
    return dest


def dlls(pkg_dir: Path) -> list[Path]:
    return sorted(p for p in pkg_dir.rglob("*.dll") if p.is_file())


_UTF16 = re.compile(rb"(?:[\x20-\x7e]\x00){3,}")


def utf16_strings(data: bytes) -> set[str]:
    """Equivalent of `strings -e l`: UTF-16LE literals (the #US heap)."""
    return {m.group().decode("utf-16-le") for m in _UTF16.finditer(data)}


_VERSION = re.compile(rb"^\d+(\.\d+){1,3}$")


def plugin_guids(data: bytes) -> list[str]:
    """GUIDs declared by [BepInPlugin(guid, name, version)] in a DLL.

    The attribute is stored as a custom-attribute blob: prolog 01 00, then
    three length-prefixed UTF-8 strings, then 00 00 (no named args). A
    [BepInDependency] blob has one string followed by an int32 instead, so it
    does not match -- which matters because a sub-module's DLL names its
    parent's GUID as a dependency.
    """
    out: list[str] = []
    i = data.find(b"\x01\x00")
    while i != -1:
        pos, strs = i + 2, []
        for _ in range(3):
            if pos >= len(data):
                break
            n = data[pos]
            if not 0 < n < 0x80:
                break
            s = data[pos + 1:pos + 1 + n]
            if len(s) != n or not all(0x20 <= c < 0x7f for c in s):
                break
            strs.append(s)
            pos += 1 + n
        if len(strs) == 3 and _VERSION.match(strs[2]) and data[pos:pos + 2] == b"\x00\x00":
            g = strs[0].decode()
            if g not in out:
                out.append(g)
        i = data.find(b"\x01\x00", i + 1)
    return out


def package_guids(pkg_dir: Path) -> list[str]:
    guids: list[str] = []
    for d in dlls(pkg_dir):
        for g in plugin_guids(d.read_bytes()):
            if g not in guids:
                guids.append(g)
    return guids


# Config files that aren't named after a plugin GUID.
CONFIG_OWNER_OVERRIDES = {
    "BepInEx.cfg": LOADER,
    "binds.yaml": "JereKuusela-Server_devcommands",
    "permissions.yaml": "JereKuusela-Server_devcommands",
}


def config_guid(rel: str) -> str:
    """config/ relative path -> the GUID it belongs to (by BepInEx naming)."""
    first = rel.split("/", 1)[0]
    if "/" in rel:          # e.g. shudnal.ConditionalConfigSync/<file>
        return first
    return first[:-4] if first.endswith(".cfg") else first


def shipped_configs() -> list[str]:
    root = REPO / "config"
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


# ── BepInEx .cfg parsing ────────────────────────────────────────

_SECTION = re.compile(r"^\[(.+)\]\s*$")
_ENTRY = re.compile(r"^([^#;=][^=]*?)\s*=\s?(.*)$")


def parse_cfg(text: str) -> dict[tuple[str, str], dict]:
    """{(section, key): {value, type, default}} for a BepInEx .cfg."""
    out: dict[tuple[str, str], dict] = {}
    section, typ, default = "", None, None
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        m = _SECTION.match(line)
        if m:
            section, typ, default = m.group(1), None, None
            continue
        if line.startswith("# Setting type:"):
            typ = line.split(":", 1)[1].strip()
            continue
        if line.startswith("# Default value:"):
            default = line.split(":", 1)[1].strip()
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _ENTRY.match(line)
        if m:
            out[(section, m.group(1).strip())] = {
                "value": m.group(2).strip(), "type": typ, "default": default}
            typ, default = None, None
    return out


def write_output(**kv) -> None:
    """Append key=value pairs to $GITHUB_OUTPUT (multi-line safe)."""
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a") as f:
        for k, v in kv.items():
            v = str(v)
            if "\n" in v:
                f.write(f"{k}<<__EOF__\n{v}\n__EOF__\n")
            else:
                f.write(f"{k}={v}\n")
