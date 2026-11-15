#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Fimbulwinter — SteamCMD helper for the maintenance pipeline
#
# Usage:
#   steam.sh build-id      Print the public build ID of the Valheim
#                          dedicated server (app 896660)
#   steam.sh install DIR   Install/update the dedicated server into DIR
#
# The dedicated server is free and installs with an anonymous login.
# Uses `steamcmd` from PATH if present, otherwise the official
# steamcmd/steamcmd Docker image (needs no 32-bit host libraries).
#
# Requires: bash, awk, and steamcmd or docker
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

APP_ID=896660
IMAGE="${STEAMCMD_IMAGE:-steamcmd/steamcmd:latest}"

steamcmd_run() {
    # $1 = install dir to mount (or ""), rest = steamcmd arguments
    local dir="$1"; shift
    if command -v steamcmd >/dev/null; then
        steamcmd "$@"
    elif command -v docker >/dev/null; then
        local mount=()
        [ -n "$dir" ] && mount=(-v "${dir}:/data")
        docker run --rm "${mount[@]}" "$IMAGE" "$@"
    else
        echo "steam.sh: need steamcmd or docker" >&2
        exit 1
    fi
}

case "${1:-}" in
build-id)
    out=$(steamcmd_run "" +login anonymous +app_info_update 1 +app_info_print "$APP_ID" +quit)
    id=$(awk '/"branches"/{b=1} b&&/"public"/{p=1} p&&/"buildid"/{gsub(/"/,"",$2); print $2; exit}' <<<"$out")
    [ -n "$id" ] || { echo "steam.sh: could not read build id" >&2; exit 1; }
    echo "$id"
    ;;
install)
    dir="${2:?usage: steam.sh install DIR}"
    mkdir -p "$dir"
    dir="$(cd "$dir" && pwd)"
    if command -v steamcmd >/dev/null; then
        steamcmd +force_install_dir "$dir" +login anonymous +app_update "$APP_ID" validate +quit
    else
        steamcmd_run "$dir" +force_install_dir /data +login anonymous +app_update "$APP_ID" validate +quit
        # The image runs as root; hand the files back to the caller.
        docker run --rm -v "${dir}:/data" --entrypoint chown "$IMAGE" -R "$(id -u):$(id -g)" /data
    fi
    [ -x "${dir}/valheim_server.x86_64" ] || { echo "steam.sh: install failed" >&2; exit 1; }
    ;;
*)
    sed -n '2,15p' "$0"; exit 2 ;;
esac
