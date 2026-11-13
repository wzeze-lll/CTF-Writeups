#!/usr/bin/env bash
# 检查题型库的运行库材料在 UTM 9p 共享目录里是否可用。
#
# 背景：这台 Mac 通过 virtio-9p 把 ~/Desktop/work 共享给 Linux 虚拟机。
# 实测（2026-10-27）：宿主机侧创建的任何软链接，在虚拟机里都读不了——
# readlink 返回空，访问报 ELOOP（Too many levels of symbolic links）。
# 因此本库约定：libc.so.6、ld-linux-*.so.* 这类别名一律用真实文件副本，
# 不要用 ln -s。
#
# 用法：bash tools/check-env.sh
# 退出码 0 表示干净，1 表示发现问题。

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

echo "[1/2] 软链接检查（本库不允许软链接）"
found=0
while IFS= read -r -d '' link; do
    found=1
    fail=1
    echo "  软链接: ${link#$ROOT/} -> $(readlink "$link" 2>/dev/null || echo '?')"
done < <(find "$ROOT" -type l -print0 2>/dev/null)
[ "$found" -eq 0 ] && echo "  OK：没有软链接"

echo "[2/2] 运行库文件检查（必须是真实 ELF，不能是文本占位）"
bad=0
while IFS= read -r -d '' f; do
    if ! file -b "$f" 2>/dev/null | grep -q '^ELF'; then
        echo "  非 ELF: ${f#$ROOT/}（疑似提取失败的文本占位）"
        bad=1
        fail=1
    fi
done < <(find "$ROOT/libc" -type f \
    \( -name 'libc.so.6' -o -name 'libc-*.so' -o -name 'ld-*.so*' \) -print0 2>/dev/null)
[ "$bad" -eq 0 ] && echo "  OK：libc/ld 都是 ELF"

# 在虚拟机里额外验证：真实可解析（能抓到 ELOOP，即宿主机软链的典型症状）
if [ "$(uname -s)" = "Linux" ]; then
    echo "[附加] 虚拟机内解析检查"
    parse_bad=0
    while IFS= read -r -d '' f; do
        if ! stat -L "$f" >/dev/null 2>&1; then
            echo "  无法解析: ${f#$ROOT/}"
            parse_bad=1
            fail=1
        fi
    done < <(find "$ROOT/libc" -type l -print0 2>/dev/null)
    [ "$parse_bad" -eq 0 ] && echo "  OK：没有无法解析的条目"
fi

if [ "$fail" -ne 0 ]; then
    echo
    echo "检查未通过。修复方法：用真实文件副本替换软链接，例如"
    echo "  cp -L <别名> <别名>.tmp && mv <别名>.tmp <别名>"
    echo "不要在 Mac 侧对共享目录执行 ln -s。"
    exit 1
fi
echo
echo "检查通过：运行库材料在共享目录里可直接使用。"
