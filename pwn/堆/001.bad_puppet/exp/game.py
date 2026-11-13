from pwn import *
import time, re, sys

class Game:
    def __init__(self, mode="socket", env=None, host=None, port=None, retries=45):
        context.log_level = "error"
        self.proc = None
        self.remote_mode = host is not None
        e = {"MALLOC_ARENA_MAX": "1"}
        if env: e.update(env)
        if self.remote_mode:
            for _ in range(retries):
                try:
                    self.io = remote(host, port, timeout=12)
                    self.dead = False; self.buf = b""
                    time.sleep(0.5)
                    d = self.drain(1.5)
                    if b"help" in d or b"Hero starts" in d:
                        return
                    self.io.close()
                except Exception:
                    pass
                time.sleep(1.0)
            raise RuntimeError("connect failed")
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
            self.dead = True; return b""
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

    def game_setup(self):
        self.cmd("shop buy 3 4227858432", 0.5)
        self.cmd("map teleport castle", 0.35)
        self.cmd("battle", 0.35)
        self.cmd("use item", 0.35)
        self.cmd("1", 0.35)
        self.cmd("32", 0.5)
        for _ in range(8):
            if any(i["type"] == "Ring" for i in self.inv()):
                break
            eqs, drops = self.world()
            ridx = [d["idx"] for d in drops if d["is_ring"]]
            if ridx:
                self.cmd("mw pickup %d" % ridx[0], 0.5)
                if any(i["type"] == "Ring" for i in self.inv()):
                    break
        it = self.inv()
        bomb = [i for i in it if i["type"] == "Bomb Flower"]
        if bomb:
            self.cmd("shop sell %d" % bomb[0]["idx"], 0.5)
        self.cmd("shop buy 0 10", 0.7)
        self.cmd("shop buy 1 10", 0.7)


    def stale_drop(self, slot, t=0.8):
        self.buf = b""
        self.raw(("inv drop %d\ninv sort\n" % slot).encode(), t)
        txt = self.text()
        if "stale drop slot" not in txt:
            return (False, None, None)
        m = re.search(r"resolved to #(\d+) ([^|]*)\| type=([\w ]+)", txt)
        if not m:
            return (True, None, None)
        return (True, int(m.group(1)), m.group(3).strip())

    def dup_ring(self):
        for attempt in range(4):
            items = self.inv(); n = len(items)
            ringidx = {it["idx"] for it in items if it["type"] == "Ring"}
            cand = None
            for it in items:
                i = it["idx"]
                if it["type"] == "Ring": continue
                if (n - 1 - i) in ringidx: cand = i
            if cand is None:
                if attempt == 3: return None
                if attempt % 2 == 0: self.cmd("inv sort", 0.3)
                else: self.cmd("shop buy 1 1", 0.5)
                continue
            if not self.stale_drop(cand)[0]: continue
            eqs, drops = self.world()
            ridx = [d["idx"] for d in drops if d["is_ring"]]
            if not ridx: continue
            self.cmd("mw pickup %d" % ridx[0], 0.45)
            return cand
        return None

    def equip_sell(self):
        items = self.inv()
        rings = [it for it in items if it["type"] == "Ring"]
        if not rings: return None
        r0 = rings[0]
        self.cmd("inv equip %d" % r0["idx"], 0.28)
        self.cmd("shop sell %d" % r0["idx"], 0.28)
        return r0

    def equip(self, idx, wait_tx=True):
        """equip and wait for the tx thread to push into dest (so mw show is fresh)."""
        self.buf = b""
        self.cmd("inv equip %d" % idx, 0.2)
        if wait_tx:
            for _ in range(8):
                if b"main world equipped" in self.buf:
                    break
                self.drain(0.2)
        return self.buf

    # -------- solve inventory layout for a stale drop --------
    def solve(self, drop_kind, mirror_kind, mirror_id=None, tries=3):
        """drop_kind/mirror_kind in {'ring','nonring'}
        want: v_pre[s] matches drop_kind, v_pre[n-1-s] matches mirror_kind."""
        for t in range(tries):
            items = self.inv(); n = len(items)
            for it in items:
                s = it["idx"]; mir = n - 1 - s
                if mir < 0: continue
                m = items[mir]
                if drop_kind == "ring" and it["type"] != "Ring": continue
                if drop_kind == "nonring" and it["type"] == "Ring": continue
                if mirror_kind == "ring" and m["type"] != "Ring": continue
                if mirror_kind == "nonring" and m["type"] == "Ring": continue
                if mirror_id is not None and m["id"] != mirror_id: continue
                return s
            self.cmd("inv sort", 0.3)
        return None
