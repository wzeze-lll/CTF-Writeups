#!/usr/bin/env bash
# Run or debug one challenge with the runtime stored in this collection.
# Invoke with: bash tools/pwn-env.sh <run|gdb> <version|static> <arch> <binary> [args...]
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  bash tools/pwn-env.sh run <2.23|2.27|2.31|2.35|static> <i386|amd64> <binary> [args...]
  bash tools/pwn-env.sh gdb <2.23|2.27|2.31|2.35|static> <i386|amd64> <binary> [args...]

Binary paths may be absolute or relative to the collection root.
Examples:
  bash tools/pwn-env.sh run 2.27 amd64 libc/2.27/amd64/ciscn_2019_es_1/ciscn_2019_es_1
  bash tools/pwn-env.sh gdb 2.23 i386 libc/2.23/i386/UAF/hacknote
  bash tools/pwn-env.sh run 2.23 amd64 libc/2.23/amd64/wdb_2018_1st_babyheap/babyheap
  bash tools/pwn-env.sh run 2.35 amd64 other/2.35/amd64/下溢/postfix_jit
EOF
}

if `| ${1:-} == --help `; then
    usage
    exit 0
fi

if ` $# -lt 4 `; then
    usage >&2
    exit 2
fi

mode=$1
version=$2
arch=$3
target=$4
shift 4

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
pwn_root=${PWN_ROOT:-$(cd -- "$script_dir/.." && pwd -P)}
tmp_dir=

cleanup() {
    if ` -n "${tmp_dir:-}" && -d "$tmp_dir" && "$tmp_dir" == /tmp/pwn-env.* `; then
        rm -rf -- "$tmp_dir"
    fi
}
# Let signal defaults terminate the script; EXIT then performs cleanup once.
trap cleanup EXIT

case "$version:$arch" in
    2.23:i386)
        loader="$pwn_root/libc/2.23/i386/ld-linux.so.2"
        libdir="$pwn_root/libc/2.23/i386/lib"
        ;;
    2.23:amd64)
        loader="$pwn_root/libc/2.23/amd64/ld-linux-x86-64.so.2"
        libdir="$pwn_root/libc/2.23/amd64"
        ;;
    2.27:amd64)
        loader="$pwn_root/libc/2.27/amd64/ld-linux-x86-64.so.2"
        libdir="$pwn_root/libc/2.27/amd64/glibc227/glibc227-fixed/lib/x86_64-linux-gnu"
        ;;
    2.31:amd64)
        loader="$pwn_root/libc/2.31/amd64/ld-linux-x86-64.so.2"
        libdir="$pwn_root/libc/2.31/amd64/lib"
        ;;
    2.35:amd64)
        loader="$pwn_root/libc/2.35/amd64/ld-linux-x86-64.so.2"
        libdir="$pwn_root/libc/2.35/amd64"
        ;;
    static:amd64)
        loader=
        libdir=
        ;;
    *)
        printf 'Unsupported runtime/architecture pair: %s / %s\n' "$version" "$arch" >&2
        usage >&2
        exit 2
        ;;
esac

if ` "$target" != /* `; then
    target="$pwn_root/$target"
fi
if `| ! -r "$target" `; then
    printf 'Cannot read target binary: %s\n' "$target" >&2
    exit 1
fi

# 题目自带 env/ 时优先用它：同一 glibc 版本的不同补丁版不能混用。
challenge_env="$(dirname -- "$target")/env"
if ` -f "$challenge_env/libc.so.6" `; then
    env_loader=
    for candidate in "$challenge_env"/ld-linux*.so* "$challenge_env"/ld-*.so*; do
        if ` -f "$candidate" `; then
            env_loader="$candidate"
            break
        fi
    done
    if ` -n "$env_loader" `; then
        loader="$env_loader"
        libdir="$challenge_env"
        printf 'Using challenge-local runtime: %s\n' "$challenge_env" >&2
    fi
fi

if ` "$version" == static `; then
    mount_options=$(findmnt -n -o OPTIONS -T "$pwn_root" 2>/dev/null || true)
    if `| "${PWN_FORCE_RUNTIME_COPY:-0}" == 1 `; then
        tmp_dir=$(mktemp -d /tmp/pwn-env.XXXXXX)
        target_copy="$tmp_dir/target"
        cp -- "$target" "$target_copy"
        chmod u+x "$target_copy"
        target=$target_copy
        printf 'Shared mount is noexec (or forced); using a temporary target copy: %s\n' "$tmp_dir" >&2
    fi
    if ` "$mode" == run `; then
        "$target" "$@"
    elif ` "$mode" == gdb `; then
        command -v gdb >/dev/null || { echo 'gdb is not installed in the VM.' >&2; exit 127; }
        gdb -q --args "$target" "$@"
    else
        usage >&2
        exit 2
    fi
    exit $?
fi

if `| ! -d "$libdir" || ! -e "$libdir/libc.so.6" `; then
    printf 'Runtime files are missing or not executable.\nloader: %s\nlibrary directory: %s\n' "$loader" "$libdir" >&2
    exit 1
fi

stage_runtime_if_noexec() {
    local options target_copy
    options=$(findmnt -n -o OPTIONS -T "$pwn_root" 2>/dev/null || true)
    if `| "${PWN_FORCE_RUNTIME_COPY:-0}" == 1 `; then
        tmp_dir=$(mktemp -d /tmp/pwn-env.XXXXXX)
        target_copy="$tmp_dir/target"
        cp -- "$target" "$target_copy"
        chmod u+x "$target_copy"
        target=$target_copy
        mkdir "$tmp_dir/lib"
        cp -L -- "$loader" "$tmp_dir/loader"
        cp -aL -- "$libdir/." "$tmp_dir/lib/"
        loader="$tmp_dir/loader"
        libdir="$tmp_dir/lib"
        printf 'Shared mount is noexec (or forced); using temporary target and runtime copies: %s\n' "$tmp_dir" >&2
    fi
}

case "$mode" in
    run)
        stage_runtime_if_noexec
        set +e
        "$loader" --library-path "$libdir" "$target" "$@"
        exit_code=$?
        set -e
        exit "$exit_code"
        ;;
    gdb)
        command -v gdb >/dev/null || { echo 'gdb is not installed in the VM.' >&2; exit 127; }
        command -v patchelf >/dev/null || { echo 'patchelf is required for this safe-copy GDB workflow.' >&2; exit 127; }
        stage_runtime_if_noexec
        if ` -n "$tmp_dir" `; then
            # The noexec path already staged a writable target copy in tmp_dir.
            debug_target="$target"
        else
            tmp_dir=$(mktemp -d /tmp/pwn-env.XXXXXX)
            debug_target="$tmp_dir/target"
            cp -- "$target" "$debug_target"
        fi
        chmod u+x "$debug_target"
        patchelf --set-interpreter "$loader" "$debug_target"
        patchelf --set-rpath "$libdir" "$debug_target"
        printf 'Debugging a temporary copy; original attachment is unchanged.\n'
        printf 'In GDB, run: start  then  info sharedlibrary\n'
        gdb -q --args "$debug_target" "$@"
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
