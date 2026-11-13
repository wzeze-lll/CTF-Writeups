#!/usr/bin/env python3
import socket, time, re, sys
HOST="127.0.0.1"; PORT=31337
class G:
    def __init__(self,s): self.s=s
    def rx(self,pats,timeout=2.0):
        if isinstance(pats,str): pats=[pats]
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
    def cmd(self,c,pats,timeout=2.0):
        self.s.sendall(c.encode()+b"\n"); time.sleep(0.02)
        out=self.rx(pats,timeout)
        if "<EOF>" in out: raise RuntimeError("closed")
        return out
def main():
    s=socket.socket(); s.settimeout(3); s.connect((HOST,PORT)); g=G(s)
    print(g.rx("Great Plateau",3),flush=True)
    for i in range(5):
        g.cmd("shop buy 1 1", ["tx: item added","not enough"])
        g.cmd("inv equip 1", ["tx: main world equipped","invalid"])
        g.cmd("shop sell 1", ["shop sold","invalid"])
        g.cmd("mw throw 0", ["throws equipped item","invalid"])
        g.cmd("mw pickup 0", ["tx: item added","invalid"])
        g.cmd("shop sell 1", ["shop sold","invalid"])
        time.sleep(0.2)
    st=g.cmd("mw show", ["Drops:"])
    r=int(re.search(r"Rupees=(\d+)",st).group(1))
    n=min(999,(r-100)//64)
    g.cmd("shop buy 3 %d"%n, ["tx:","not enough"],3)
    g.cmd("map teleport castle", ["Encounter"])
    g.cmd("battle", ["player turn"])
    g.cmd("use item", ["Enter inventory idx"])
    g.cmd("1", ["Enter quantity"])
    g.cmd("%d"%n, ["Battle won"],4)
    g.cmd("mw pickup 0", ["tx: item added","invalid"])
    g.cmd("inv equip 1", ["tx: main world equipped","invalid"])
    st=g.cmd("mw show", ["Drops:"])
    m=re.search(r"description_addr=0x([0-9a-f]+)", st)
    print("BASE="+m.group(1) if m else "NOBASE",flush=True)
    print("HOLDING",flush=True)
    time.sleep(600)
    g.cmd("quit", ["bye"],1)
if __name__=="__main__":
    main()
