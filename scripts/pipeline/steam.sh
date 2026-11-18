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
        # Docker's default seccomp profile blocks a socket call the current
        # Steam client makes on GitHub's ubuntu-26.04 runners (kernel 7.0):
        # every login fails with "CreateBoundSocket ... (38)" / "No
        # Connection". The container still keeps its namespaces and mounts.
        docker run --rm --security-opt seccomp=unconfined "${mount[@]}" "$IMAGE" "$@"
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
    target="$dir"
    command -v steamcmd >/dev/null || target=/data
    # A fresh SteamCMD sometimes fails app_update with "Missing
    # configuration" until the app info is loaded, so load it first and
    # retry a few times.
    ok=0
    for attempt in 1 2 3; do
        if steamcmd_run "$dir" +force_install_dir "$target" +login anonymous \
            +app_info_update 1 +app_update "$APP_ID" validate +quit; then
            ok=1; break
        fi
        echo "steam.sh: install attempt $attempt failed" >&2
        sleep $((attempt * 15))
    done
    if ! command -v steamcmd >/dev/null; then
        # The image runs as root; hand the files back to the caller.
        docker run --rm -v "${dir}:/data" --entrypoint chown "$IMAGE" -R "$(id -u):$(id -g)" /data
    fi
    [ "$ok" = 1 ] || { echo "steam.sh: install failed after 3 attempts" >&2; exit 1; }
    [ -x "${dir}/valheim_server.x86_64" ] || { echo "steam.sh: install failed" >&2; exit 1; }
    ;;
*)
    sed -n '2,15p' "$0"; exit 2 ;;
esac
