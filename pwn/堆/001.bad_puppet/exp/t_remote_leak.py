from lib import *
import sys, time

HOST, PORT = "127.0.0.1", 30809

class RGame(Game):
    def __init__(self):
        context.log_level = "error"
        for attempt in range(8):
            try:
                self.io = remote(HOST, PORT, timeout=12)
                self.dead = False
                self.buf = b""
                time.sleep(0.6)
                d = self.drain(1.2)
                if b"help" in d or b"Hero starts" in d:
                    return
                self.io.close()
            except Exception as e:
                pass
            time.sleep(1.0)
        raise RuntimeError("connect failed")

g = RGame()
print("connected")
g.game_setup()
print("setup ok, rings:", sum(1 for it in g.inv() if it["type"] == "Ring"))
n = g.dup_n(8)
print("dups:", n)
items = g.inv()
NR = sum(1 for it in items if it["type"] == "Ring")
print("rings:", NR)
for k in range(NR):
    g.equip_sell()
eqs, _ = g.world()
print("dest entries:", len(eqs))
for e in eqs:
    print("  [%d] addr=%s head=%s key=%s" % (e["idx"], hex(e["addr"]), hex(e["head"]), hex(e["key"])))
g.cmd("quit", 0.2)
