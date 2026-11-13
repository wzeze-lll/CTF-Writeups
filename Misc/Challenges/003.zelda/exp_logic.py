#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H2 纯逻辑速通: 负数/溢出购买 -> 无限卢比 -> Master Sword -> castle -> Ganon

流程:
  1) 卢比阶梯: 依次尝试各种边界数量, 只认 "Rupees 变大" 这一个信号
  2) 买 Master Sword(price=10000 stock=1) 并装备
  3) map teleport castle -> battle -> 自适应回合(先测伤害, 再算预算)
  4) 抓 flag / 关键行

用法:
  python3 exp_logic.py            # 全流程
  python3 exp_logic.py money      # 只跑卢比阶梯
  python3 exp_logic.py fight      # 假设已有 Master Sword, 直接打
"""
import re, sys, time, game

SEP = "=" * 78
FLEE_AT = 18          # 玩家 HP 低于此值且回合数不足时尝试脱战
MAX_TURN = 80

MONEY_LADDER = [
    "shop buy 3 -1",
    "shop buy 3 -200",
    "shop buy 3 -10000",
    "shop buy 3 1000000",
    "shop buy 3 67108864",          # 64 * 2^26 == 2^32
    "shop buy 3 33554432",          # 64 * 2^25 == 2^31 (int32 负数)
    "shop buy 3 2147483647",
    "shop buy 3 4294967296",
    "shop buy 3 +999999999999999999999",
    "shop buy 0 -1",
]


class S:
    def __init__(self):
        self.g = game.Game()
        print("[banner]", self.g.buf.decode("utf-8", "replace").strip())

    def c(self, cmd, quiet=0.45):
        print(f">>> {cmd}")
        out = self.g.cmd(cmd, quiet)
        print(out.rstrip() if out.strip() else "<empty>")
        return out

    def close(self):
        self.g.close()


def parse_show(t):
    d = {}
    m = re.search(r"HP=(-?\d+) Stamina=(-?\d+) Rupees=(-?\d+) Arrows=(-?\d+) BossHP=(-?\d+)", t)
    if m:
        d.update(hp=int(m.group(1)), stamina=int(m.group(2)), rupees=int(m.group(3)),
                 arrows=int(m.group(4)), boss_hp=int(m.group(5)))
    m = re.search(r"Location=([^ ]+) Enemy=([^ ]+) EnemyDefeated=(\w+)", t)
    if m:
        d.update(loc=m.group(1), enemy=m.group(2), defeated=m.group(3))
    m = re.search(r"EXP=(-?\d+) Battle=(\S+) Turn=(-?\d+)", t)
    if m:
        d.update(exp=int(m.group(1)), battle=m.group(2), turn=int(m.group(3)))
    return d


def parse_battle(t):
    m = re.search(r"enemy=(\S+) phase=(\S+) turn=(\d+) player_hp=(\d+) enemy_hp=(\d+)/(\d+)", t)
    if not m:
        return None
    return dict(enemy=m.group(1), phase=m.group(2), turn=int(m.group(3)),
                php=int(m.group(4)), ehp=int(m.group(5)), emax=int(m.group(6)))


def money_phase(s):
    """返回成功的那条命令或 None"""
    base = parse_show(s.c("mw show"))
    print(f"[base rupees] {base.get('rupees')}")
    if base.get("rupees", 0) >= 10000:
        return "already rich"
    for cmd in MONEY_LADDER:
        print("\n" + "-" * 70)
        try:
            s.c(cmd)
            st = parse_show(s.c("mw show"))
        except Exception as e:
            print("[!] connection died:", e)
            return None
        r = st.get("rupees")
        print(f"[rupees now] {r}")
        if r is not None and r != base.get("rupees"):
            print(f"[+] 命中: {cmd}  -> Rupees {base.get('rupees')} => {r}")
            return cmd
    return None


def inv_index_of(out, needle):
    for ln in out.splitlines():
        if needle.lower() in ln.lower():
            m = re.search(r"\[(\d+)\]", ln)
            if m:
                return int(m.group(1))
    return None


def buy_and_equip(s):
    s.c("shop list")
    out = s.c("shop buy 2 1")
    inv = s.c("inv list")
    idx = inv_index_of(inv, "Master Sword")
    if idx is None:
        print("[!] 没买到 Master Sword, 输出如上")
        return None
    s.c(f"inv equip {idx}")
    s.c("mw show")
    return idx


def goto(s, place):
    out = s.c(f"map teleport {place}")
    s.c("map show")
    s.c("mw show")
    return out


def fight(s, use_item_first=False):
    s.c("battle")
    st = parse_battle(s.c("battle")) or {}
    print(f"[battle start] {st}")
    dmg = None
    edmg = None
    first = True
    for _ in range(MAX_TURN):
        cur = parse_battle(s.c("battle"))
        if cur is None:
            print("[!] 没有 battle status, 可能已结束")
            break
        print(f"[state] {cur}")
        if cur["ehp"] <= 0:
            print("[+] 敌人已死")
            break
        if cur["php"] <= 0:
            print("[!] 玩家死亡")
            break

        # 决策
        if use_item_first and first:
            act = "use item"
        else:
            act = "attack"
        # HP 预算不足且还有距离 -> 先嗑药/道具争取输出
        if dmg and cur["php"] <= FLEE_AT:
            need = (cur["ehp"] + dmg - 1) // dmg
            if need * (edmg or 0) >= cur["php"]:
                act = "use item"
        first = False

        before = cur
        out = s.c(act)
        after = parse_battle(out)
        if after:
            if before["ehp"] - after["ehp"] > 0:
                dmg = before["ehp"] - after["ehp"]
            if before["php"] - after["php"] > 0:
                edmg = before["php"] - after["php"]
            if dmg and edmg:
                need = (after["ehp"] + dmg - 1) // dmg
                print(f"[calc] dmg={dmg} edmg={edmg} need={need} turns "
                      f"-> 预计掉血 {need * edmg} / 当前 {after['php']}")
            if after["ehp"] <= 0:
                print("[+] 敌人已死")
                break
    s.c("mw show")
    s.c("inv list")


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    s = S()
    try:
        if what in ("all", "money"):
            hit = money_phase(s)
            print(f"[money hit] {hit}")
            if what == "money":
                return
        if what in ("all", "fight"):
            if what == "all":
                buy_and_equip(s)
            goto(s, "castle")
            fight(s)
    finally:
        s.close()


if __name__ == "__main__":
    main()
