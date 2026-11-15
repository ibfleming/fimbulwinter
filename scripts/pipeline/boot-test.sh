#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Fimbulwinter — Headless boot test (CI and local)
#
# Boots a throwaway Valheim dedicated server with BepInEx and a mod set,
# waits until it is accepting connections, stops it, and writes a report.
#
# Usage:
#   boot-test.sh harvest|verify --valheim DIR --repo-dir DIR --out DIR
#                [--timeout SECONDS]
#
#   harvest   EVERY mod (client-only included) on an EMPTY config dir, so
#             each mod writes fresh defaults. Output: <out>/config/
#   verify    the real server mod set with the repo's config/ overlaid,
#             exactly like scripts/deploy.sh full
#
#   --valheim   an installed dedicated server (scripts/pipeline/steam.sh
#               install). It is never modified: each boot runs in a
#               hard-linked copy.
#   --repo-dir  a directory holding thunderstore.toml and config/ (a repo
#               checkout, or an exported older revision)
#   --out       report directory: LogOutput.log, config/, report.json
#
# Exit: 0 boot clean, 1 boot failed (see report.json), 2 usage error.
# Requires: bash, curl, jq, unzip, python3
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${HERE}/../.." && pwd)"

MODE="${1:-}"; shift || true
VALHEIM="" REPO_DIR="" OUT="" TIMEOUT=900
while [ $# -gt 0 ]; do
    case "$1" in
        --valheim)  VALHEIM="$2"; shift 2 ;;
        --repo-dir) REPO_DIR="$2"; shift 2 ;;
        --out)      OUT="$2"; shift 2 ;;
        --timeout)  TIMEOUT="$2"; shift 2 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done
case "$MODE" in harvest|verify) ;; *) sed -n '2,25p' "$0"; exit 2 ;; esac
[ -x "${VALHEIM}/valheim_server.x86_64" ] || { echo "--valheim must be an installed server" >&2; exit 2; }
[ -f "${REPO_DIR}/thunderstore.toml" ] || { echo "--repo-dir needs thunderstore.toml" >&2; exit 2; }
[ -n "$OUT" ] || { echo "--out is required" >&2; exit 2; }

log() { echo "[BOOT:${MODE}] $*" >&2; }

mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/fw-boot.XXXXXX")"
SERVER="${WORK}/server"
SAVES="${WORK}/saves"
PID=""
cleanup() {
    [ -n "$PID" ] && kill "$PID" 2>/dev/null && wait "$PID" 2>/dev/null || true
    rm -rf "$WORK"
}
trap cleanup EXIT

# ── Server copy (hard links: instant, no extra disk) ─────────────
log "Preparing server copy in ${WORK}"
cp -al "${VALHEIM}/." "$SERVER" 2>/dev/null || cp -a "${VALHEIM}/." "$SERVER"
mkdir -p "$SAVES"

# ── Mods ─────────────────────────────────────────────────────────
install_args=(--server-dir "$SERVER" --source local --repo-dir "$REPO_DIR" --full)
[ "$MODE" = harvest ] && install_args+=(--include-client --no-config)
log "Installing mod set (${MODE})"
bash "${REPO}/scripts/install-mods.sh" "${install_args[@]}" >"${OUT}/install.log" 2>&1 \
    || { log "install-mods.sh failed (see ${OUT}/install.log)"; tail -20 "${OUT}/install.log" >&2; exit 1; }
if [ "$MODE" = harvest ]; then
    # Mods may ship sample configs in their zip; harvest wants only what
    # the plugins themselves write on first boot.
    rm -rf "${SERVER}/BepInEx/config"
    mkdir -p "${SERVER}/BepInEx/config"
fi

# ── Boot ─────────────────────────────────────────────────────────
PORT=$(( 20000 + RANDOM % 20000 ))
log "Booting on port ${PORT} (timeout ${TIMEOUT}s)"
(
    cd "$SERVER"
    export SteamAppId=892970
    export DOORSTOP_ENABLED=1
    export DOORSTOP_TARGET_ASSEMBLY=./BepInEx/core/BepInEx.Preloader.dll
    export LD_LIBRARY_PATH="./doorstop_libs:./linux64:${LD_LIBRARY_PATH:-}"
    export LD_PRELOAD="libdoorstop_x64.so:${LD_PRELOAD:-}"
    exec ./valheim_server.x86_64 -nographics -batchmode -name "CI boot test" \
        -port "$PORT" -world "CIBoot" -password "ci-boot-$RANDOM" -public 0 \
        -savedir "$SAVES"
    # No -crossplay: it is a bare switch, so passing it with any value
    # turns PlayFab networking on.
) >"${OUT}/stdout.log" 2>&1 &
PID=$!

LOGFILE="${SERVER}/BepInEx/LogOutput.log"
ready=false
start=$SECONDS
while (( SECONDS - start < TIMEOUT )); do
    if ! kill -0 "$PID" 2>/dev/null; then
        log "Server process exited early"
        break
    fi
    # Unity's own log reaches LogOutput.log only when BepInEx.cfg says so
    # (a harvest boot runs on defaults, where it doesn't), so watch stdout
    # too. "Opened Steam server" is logged once the world is loaded or
    # generated; "Game server connected" can come before world generation.
    if grep -q "Opened Steam server" "${OUT}/stdout.log" "$LOGFILE" 2>/dev/null; then
        ready=true
        break
    fi
    sleep 3
done
elapsed=$(( SECONDS - start ))
if $ready; then
    log "Ready after ${elapsed}s; letting late initialisers settle"
    sleep 15
fi
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true
PID=""

# ── Collect ──────────────────────────────────────────────────────
cp "$LOGFILE" "${OUT}/LogOutput.log" 2>/dev/null || : >"${OUT}/LogOutput.log"
rm -rf "${OUT}/config"
cp -r "${SERVER}/BepInEx/config" "${OUT}/config"

python3 "${HERE}/boot_report.py" --mode "$MODE" --ready "$ready" --seconds "$elapsed" \
    --log "${OUT}/LogOutput.log" --stdout "${OUT}/stdout.log" --plugins "${SERVER}/BepInEx/plugins" \
    --out "${OUT}/report.json"
