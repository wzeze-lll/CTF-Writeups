#!/usr/bin/env python3
"""Adaptive in-game agent: recon locations, find ring/drops, money, fight."""
import os, sys, time, socket, re
os.environ.setdefault("ZH", "127.0.0.1")
os.environ.setdefault("ZP", "36943")
os.environ.setdefault("ZLOG", "agent.log")
import win

LOCS = ["zora", "rito", "goron", "gerudo", "castle", "plateau"]

class A:
    def __init__(self, s, b):
        self.s = win.Sess(s, b)
        self.inv = []
        self.slot = 0
    def c(self, cmd, q=0.35):
        return self.s.cmd(cmd, quiet=q)
    def parse_inv(self, txt):
        items = []
        for line in txt.splitlines():
            m = re.match(r"\[\*\]\s+\[(\d+)\]\s+#(\d+)\s+(.*?)\s+\|\s+type=(\w+)\s+\|\s+equipped=(\d)", line)
            if m:
                items.append(dict(idx=int(m.group(1)), id=int(m.group(2)), name=m.group(3), type=m.group(4)))
        return items
    def parse_rupees(self, txt):
        m = re.search(r"Rupees=(-?\d+)", txt)
        return int(m.group(1)) if m else None
    def parse_drops(self, txt):
        m = re.search(r"Drops:\s*(.*)", txt)
        return m.group(1).strip() if m else ""
    def equip_named(self, name):
        inv = self.parse_inv(self.c("inv list"))
        for it in inv:
            if name.lower() in it["name"].lower():
                out = self.c("inv equip %d" % it["idx"])
                self.c("mw show")
                return it
        return None
    def pickup_all(self):
        for i in range(3):
            out = self.c("mw pickup %d" % i)
            if "invalid" in out.lower() or "empty" in out.lower():
                break
            self.c("inv list")

def run(a):
    a.c("help")
    st = a.c("mw show"); r = a.parse_rupees(st)
    win.log("[start rupees] %s" % r)

    ring = False
    for loc in LOCS:
        if a.s.dead: return
        a.c("map teleport %s" % loc)
        st = a.c("mw show")
        drops = a.parse_drops(st)
        win.log("[%s drops] %s" % (loc, drops))
        if drops and "empty" not in drops.lower():
            a.pickup_all()
        sh = a.c("shop list")
        if "ring" in sh.lower():
            win.log("[RING IN SHOP at %s]" % loc)
            ring = True
        inv = a.parse_inv(a.c("inv list"))
        if any("ring" in it["name"].lower() for it in inv):
            win.log("[RING IN INVENTORY]")
            ring = True

    if ring:
        it = a.equip_named("ring")
        win.log("[ring equip] %s" % it)
        a.c("mw whisper %d 41424344" % a.slot)
        a.c("mw show")
        a.c("mw whisper %d 00" % a.slot)
        a.c("mw show")

    # money attempts
    st = a.c("mw show"); r = a.parse_rupees(st)
    for payload in ["shop buy 3 0", "shop buy 2 0", "shop buy 3 67108864", "shop buy 2 -1"]:
        if a.s.dead: return
        a.c(payload)
        st = a.c("mw show"); r2 = a.parse_rupees(st)
        win.log("[money %s] -> %s" % (payload, r2))
        if r2 is not None and r2 != r:
            r = r2
            if r >= 10000: break

    # fight bokoblin for drops
    a.c("map teleport plateau")
    a.c("shop buy 1 1")
    a.equip_named("Broadsword")
    a.c("battle")
    for i in range(20):
        if a.s.dead: break
        out = a.c("attack")
        if "defeated" in out.lower() or "victory" in out.lower() or "EnemyDefeated=yes" in out:
            break
        if "player_hp=0" in out: break
    st = a.c("mw show"); win.log("[after fight drops] %s" % a.parse_drops(st))
    a.pickup_all()
    inv = a.c("inv list"); win.log(inv)
    if "ring" in inv.lower():
        a.equip_named("ring")

    # castle attempt
    st = a.c("mw show"); r = a.parse_rupees(st)
    if r is not None and r >= 10000:
        a.c("shop buy 2 1")
        a.equip_named("Master Sword")
    a.c("map teleport castle")
    a.c("battle")
    for i in range(60):
        if a.s.dead: break
        out = a.c("attack")
        if re.search(r"flag\{", out, re.I):
            win.log("[FLAG] " + out)
            break
        if "player_hp=0" in out or "lost" in out:
            break
    a.c("quit")

def main():
    delay = float(sys.argv[1]) if len(sys.argv) > 1 else 0
    if delay: time.sleep(delay)
    s = socket.socket(); s.settimeout(5)
    try:
        s.connect((win.HOST, win.PORT))
    except Exception as e:
        win.log("connect err %s" % e); return
    s.settimeout(1.2)
    b = b""
    try:
        while True:
            d = s.recv(8192)
            if not d: break
            b += d
            if b"Plateau" in b: break
    except Exception:
        pass
    if b"Plateau" not in b:
        win.log("no banner"); s.close(); return
    a = A(s, b)
    try:
        run(a)
    except Exception as e:
        win.log("[agent err] %s" % e)
    try: s.close()
    except Exception: pass

if __name__ == "__main__":
    main()
