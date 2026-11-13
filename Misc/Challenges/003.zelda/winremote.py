#!/usr/bin/env python3
"""Win the Zelda game: money via double-sell, bombs, Ganon, Ring, whisper."""
import socket, time, sys, re, os

HOST = os.environ.get("EH", "127.0.0.1")
PORT = int(os.environ.get("EP", "31337"))

class G:
    def __init__(self, s):
        self.s = s
    def rx(self, pats, timeout=2.0):
        if isinstance(pats, str): pats=[pats]
        end=time.time()+timeout; out=b""
        while time.time()<end:
            self.s.settimeout(max(0.02,end-time.time()))
            try: d=self.s.recv(65536)
            except Exception: break
            if not d: out+=b"<EOF>"; break
            out+=d
            t=out.decode("utf-8","replace")
            if any(p in t for p in pats): break
        return out.decode("utf-8","replace")
    def cmd(self, c, pats, timeout=2.0):
        try: self.s.sendall(c.encode()+b"\n")
        except Exception as e: print("[send err]",e); raise
        time.sleep(0.03)
        out=self.rx(pats,timeout)
        print(">>> %s\n%s"%(c,out.rstrip()),flush=True)
        if "<EOF>" in out: raise RuntimeError("closed")
        return out

def main():
    s=None; banner=""
    for i in range(4):
        try:
            c=socket.socket(); c.settimeout(4); c.connect((HOST,PORT))
        except Exception as e:
            print("[connect %d] %s"%(i,e),flush=True); time.sleep(60); continue
        c.settimeout(2)
        banner=""
        t0=time.time()
        while time.time()-t0 < 6:
            try:
                d=c.recv(4096)
            except Exception:
                continue
            if not d: break
            banner += d.decode("utf-8","replace")
            if "Great Plateau" in banner: break
        if "Great Plateau" in banner:
            s=c; break
        print("[connect %d] no banner %r"%(i,banner[:40]),flush=True)
        c.close(); time.sleep(60)
    if s is None: raise SystemExit("no session")
    g=G(s)
    print(banner)
    cycles=5
    for i in range(cycles):
        g.cmd("shop buy 1 1", ["tx: item added","not enough"])
        g.cmd("inv equip 1", ["tx: main world equipped","invalid"])
        g.cmd("shop sell 1", ["shop sold","invalid"])
        g.cmd("mw throw 0", ["throws equipped item","invalid"])
        g.cmd("mw pickup 0", ["tx: item added","invalid"])
        g.cmd("shop sell 1", ["shop sold","invalid"])
        time.sleep(0.25)
    st=g.cmd("mw show", ["Drops:"])
    r=int(re.search(r"Rupees=(\d+)",st).group(1))
    print("[rupees]",r)
    n=min(999,(r-100)//64)
    g.cmd("shop buy 3 %d"%n, ["tx:","not enough"], 3)
    g.cmd("map teleport castle", ["Encounter"])
    g.cmd("battle", ["player turn","already"])
    g.cmd("use item", ["Enter inventory idx"])
    g.cmd("1", ["Enter quantity"])
    out=g.cmd("%d"%n, ["Battle won","damage"], 4)
    g.cmd("mw show", ["Drops:"])
    g.cmd("mw pickup 0", ["tx: item added","invalid"])
    g.cmd("inv list", ["Inventory"])
    g.cmd("inv equip 1", ["tx: main world equipped","invalid"])
    g.cmd("mw show", ["Drops:"])
    g.cmd("mw whisper 0 4142434445464748", ["whispered","only"])
    g.cmd("mw show", ["Drops:"])
    g.cmd("quit", ["bye"], 1.5)

if __name__=="__main__":
    main()
