#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-0 侦察：连上就抓，全部"无损优先"，破坏性探针每条单开一个连接。
用法:
  python3 probe.py recon          # 只跑无损命令，一条连接
  python3 probe.py edges          # 数值边界探针，每条一个连接
  python3 probe.py hierarchy      # 命令树/隐藏子命令探测
"""
import sys, re, time, game

SEP = "-" * 70


def dump(tag, out):
    print(SEP)
    print(f"[{tag}]")
    print(out.rstrip() if out.strip() else "<empty / timeout>")


def rupees(out):
    m = re.search(r"Rupees=(-?\d+)", out)
    return int(m.group(1)) if m else None


def hp(out):
    m = re.search(r"HP=(-?\d+) Stamina=(-?\d+) Rupees=(-?\d+) Arrows=(-?\d+) BossHP=(-?\d+)", out)
    return m.groups() if m else None


def one(cmds, quiet=0.45):
    """单连接跑一串命令, 返回最后一条的输出; 连接挂了返回 None"""
    try:
        g = game.Game()
    except Exception as e:
        print("[!] connect failed:", e)
        return None
    print("[banner]", g.buf.decode("utf-8", "replace").strip())
    out = ""
    for c in cmds:
        print(f">>> {c}")
        try:
            out = g.cmd(c, quiet)
        except Exception as e:
            print("[!] send failed:", e)
            g.close()
            return None
        print(out.rstrip() if out.strip() else "<empty>")
    g.close()
    return out


def recon():
    print("== 无损基线 ==")
    one(["help", "mw show", "inv list", "shop list", "map show"])
    print(SEP)
    print("== 跨连接持久性 (关键: 判断状态是否全局共享) ==")
    one(["mw show"])


def hierarchy():
    # 只探测帮助文本, 不改变状态
    one(["help help", "help mw", "help shop", "help map", "help battle",
         "? ", "commands", "mw", "shop", "map", "inv", "battle help"])


EDGE = [
    ("shop buy 3 -1",            "负数数量"),
    ("shop buy 3 0",             "零数量"),
    ("shop buy 3 2147483647",    "int32 上界"),
    ("shop buy 3 4294967296",    "2^32"),
    ("shop buy 3 67108864",      "64*2^26 = 2^32 溢出"),
    ("shop buy 3 999999999999999999999", "atoll/饱和"),
    ("shop buy 3 1abc",          "atoi 前缀解析"),
    ("shop buy 3 +5",            "正号"),
    ("shop buy 3 0x10",          "十六进制"),
    ("shop buy 3 1.9",           "浮点截断"),
    ("shop buy 0 -1",            "负数量买剑"),
    ("shop sell 0",              "卖初始树枝(看卖价规则)"),
    ("shop sell -1",             "负索引卖"),
    ("shop sell 99",             "越界索引卖"),
    ("inv equip -1",             "负索引装备"),
    ("inv equip 99",             "越界装备"),
    ("inv drop -1",              "负索引丢弃"),
    ("inv unequip 99",           "越界卸下"),
    ("mw throw -1",              "负索引投掷"),
    ("mw pickup -1",             "负索引拾取(空 drops)"),
    ("mw pickup 0",              "索引0拾取(空 drops)"),
    ("mw pickup 99",             "越界拾取"),
    ("mw whisper 0 41",          "whisper 单字节(未装备时)"),
    ("inv sort",                 "排序"),
    ("map teleport nowhere",     "非法地点"),
    ("map teleport castle",      "直达城堡(看是否被门禁)"),
]


def edges():
    for cmd, note in EDGE:
        print("\n" + "#" * 70)
        print(f"# 探针: {cmd}   ({note})")
        one([cmd, "mw show", "inv list", "shop list"])


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "recon"
    {"recon": recon, "edges": edges, "hierarchy": hierarchy}[what]()
