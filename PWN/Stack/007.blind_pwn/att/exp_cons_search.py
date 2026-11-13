import os, time
import exp_cons as E
from pwn import *
context.log_level="error"
NV=int(os.environ.get("NV","5"))
def vote(idx,g,n=NV):
    t=f=0
    for _ in range(n):
        r=E.one(idx,g)
        if r is True: t+=1
        elif r is False: f+=1
    return t>f
def one_byte(idx):
    lo,hi=0,255
    while lo<hi:
        mid=(lo+hi)//2
        if vote(idx,mid): lo=mid+1
        else: hi=mid
    return lo
def good(idx,v):
    if not (0x20 <= v < 0x7f): return False
    if v>0 and not vote(idx,v-1): return False
    if vote(idx,v): return False
    return True
MAXLEN=int(os.environ.get("MAXLEN","45"))
STATE=os.environ.get("STATE","/tmp/flag_state.txt")
out=b""
if os.environ.get("RESUME") and os.path.exists(STATE):
    out=open(STATE,"rb").read().strip()
    print("resume from %r"%out, flush=True)""
for i in range(MAXLEN):
    if len(out)>i:            # resume: 已有该字节
        continue
    b=None
    for _ in range(5):
        v=one_byte(i)
        if good(i,v): b=v; break
    if b is None:
        print("idx %d FAILED"%i, flush=True); break
    out+=bytes([b]); print("[%02d] %r => %r"%(i,chr(b),out), flush=True)
    try: open(STATE,"wb").write(out)
    except Exception: pass
    if out.endswith(b"}"): break
print("FLAG = %s"%out.decode("latin1"), flush=True)
