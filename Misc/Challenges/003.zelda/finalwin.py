#!/usr/bin/env python3
import socket, time, re, sys
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
ALL=b""
def rx(s,pats,timeout=2.0):
    global ALL
    if isinstance(pats,str): pats=[pats]
    end=time.time()+timeout; out=b""
    while time.time()<end:
        s.settimeout(max(0.05,end-time.time()))
        try: d=s.recv(65536)
        except Exception: break
        if not d: out+=b"<EOF>"; break
        out+=d
        if any(p in out.decode('utf-8','replace') for p in pats): break
    ALL+=out
    return out.decode('utf-8','replace')
def cmd(s,c,pats,t=2.0):
    s.sendall(c.encode()+b"\n"); time.sleep(0.03); return rx(s,pats,t)
s,b=connect(); ALL+=b
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
cmd(s,"mw show",["Drops:"])
cmd(s,"inv list",["Inventory"])
# hidden probes
for c in ["help","map status","map travel castle","mw status","status","inv status",
          "shop status","battle status","map travel secret","map teleport flag","flag","cat /flag"]:
    cmd(s,c,["<EOF>","unknown","invalid","Commands","==="],1.0)
cmd(s,"quit",["bye","<EOF>"],1.0)
time.sleep(2)
s.settimeout(2); t=b""
try:
    while True:
        d=s.recv(65536)
        if not d: break
        t+=d
except Exception: pass
ALL+=t
txt=ALL.decode('utf-8','replace')
print("=== FLAG-LIKE ===")
for m in re.findall(r'[A-Za-z0-9_]*flag[A-Za-z0-9_]*\{[^}]*\}|\{[^}]{4,80}\}', txt, re.I):
    print(m)
print("=== TAIL ===")
print(txt[-600:])
s.close()
