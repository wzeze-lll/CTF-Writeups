import time, select, socket
from ws import connect, recv_frame, GW
# conn A: partial frame claiming huge length
sA,resp=connect(); sA.setblocking(False)
time.sleep(0.5)
try:
    while True:
        r,_,_=select.select([sA],[],[],0.2)
        if not r: break
        recv_frame(sA)
except Exception: pass
sA.sendall(b"\x81\xfe\xff\xff\x00\x00\x00\x00short")
print("sent partial frame on A")
time.sleep(0.5)
# conn B: does it still get SESSION/READY quickly?
t0=time.time()
try:
    sB,respB=connect()
    print("B handshake in %.2fs"%(time.time()-t0), respB.split("\r\n")[0])
    sB.setblocking(False)
    out=[]; end=time.time()+2
    while time.time()<end:
        r,_,_=select.select([sB],[],[],0.1)
        if r:
            try: out.append(recv_frame(sB)[1])
            except Exception: out.append(b"EOF"); break
    print("B frames",out)
except Exception as e:
    print("B failed after %.2fs"%(time.time()-t0), e)
sA.close()
