#!/usr/bin/env python3
# backlog + 解耦：[Ring,Bomb] -> drop bomb(slot1) + sort -> v59=slot1=Ring, v151[0]=Bomb
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
def connect(tries=60):
    for i in range(tries):
        s=socket.socket(); s.settimeout(4)
        try: s.connect((HOST,PORT))
        except Exception: time.sleep(3); continue
        s.settimeout(2); b=b""
        try:
            while True:
                d=s.recv(4096)
                if not d: break
                b+=d
                if b"Great Plateau" in b: return s,b
        except Exception: pass
        s.close(); time.sleep(4)
    return None,None
def rx(s,pats,timeout=2.0):
    if isinstance(pats,str): pats=[pats]
    end=time.time()+timeout; out=b""
    while time.time()<end:
        s.settimeout(max(0.05,end-time.time()))
        try: d=s.recv(65536)
        except Exception: break
        if not d: out+=b"<EOF>"; break
        out+=d
        if any(p in out.decode('utf-8','replace') for p in pats): break
    return out.decode('utf-8','replace')
def cmd(s,c,pats,t=2.0):
    s.sendall(c.encode()+b"\n"); time.sleep(0.03); return rx(s,pats,t)
def drain(s,t=0.6):
    time.sleep(t); s.settimeout(1.2); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
    except Exception: pass
    return o.decode('utf-8','replace')
def inv(s):
    s.sendall(b"inv list\n"); time.sleep(0.25); s.settimeout(1.2); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
            if o.count(b"type=")>=1 and o.count(b"\n")>=3: break
    except Exception: pass
    return o.decode('utf-8','replace')
s,b=connect()
if s is None: print("NO BANNER"); sys.exit(1)
for i in range(5):
    cmd(s,"shop buy 1 1",["tx: item added","not enough"])
    cmd(s,"inv equip 1",["tx: main world equipped","invalid"])
    cmd(s,"shop sell 1",["shop sold","invalid"])
    cmd(s,"mw throw 0",["throws equipped item","invalid"])
    cmd(s,"mw pickup 0",["tx: item added","invalid"])
    cmd(s,"shop sell 1",["shop sold","invalid"])
    time.sleep(0.2)
cmd(s,"shop buy 3 34",["tx:","not enough"],3)
cmd(s,"map teleport castle",["Encounter"])
cmd(s,"battle",["player turn"])
cmd(s,"use item",["Enter inventory idx"])
cmd(s,"1",["Enter quantity"])
cmd(s,"34",["Battle won"],4)
cmd(s,"mw pickup 0",["tx: item added","invalid"])
cmd(s,"inv equip 1",["tx: main world equipped","invalid"])
print("[inv win] "+" || ".join(l.strip() for l in inv(s).splitlines() if "type=" in l)[:260],flush=True)
# drop Tree Branch slot0 (ring moves to 0)
cmd(s,"inv drop 0",["inventory queued drop","invalid"])
time.sleep(0.4)
print("[inv after drop branch] "+" || ".join(l.strip() for l in inv(s).splitlines() if "type=" in l)[:260],flush=True)
# buy bomb
cmd(s,"shop buy 3 1",["tx:","not enough"],2)
time.sleep(0.3)
print("[inv after bomb] "+" || ".join(l.strip() for l in inv(s).splitlines() if "type=" in l)[:260],flush=True)
# decouple: drop bomb (last slot) + sort
print("[decouple fire]",flush=True)
s.sendall(b"inv drop 1\ninv sort\n")
print("[out] "+repr(drain(s,1.2)[-300:]),flush=True)
print("[inv after] "+" || ".join(l.strip() for l in inv(s).splitlines() if "type=" in l)[:300],flush=True)
s.close()
