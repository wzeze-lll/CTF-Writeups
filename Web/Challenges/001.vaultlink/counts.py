import time, select, struct
from ws import connect, recv_frame
def frame(p):
    return b"\x81"+bytes([0x80|len(p)])+b"\x01\x02\x03\x04"+bytes(x^[1,2,3,4][i%4] for i,x in enumerate(p))
def trial(label, payload, cap=8):
    s,resp=connect(); s.setblocking(False)
    t0=time.time()
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: recv_frame(s)
            except Exception: break
    s.sendall(payload)
    closed=None
    while time.time()-t0<cap:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try:
                o,d=recv_frame(s)
                if o==8: closed=time.time()-t0; break
            except Exception: closed=time.time()-t0; break
    print(f"{label:34s} closed={round(closed,1) if closed else '>8'}",flush=True)
    s.close()
trial("3 lines one write", b"hello\nhello\nhello\n")
trial("5 lines one write", b"hello\n"*5)
trial("3 frames one write", frame(b"hello")*3)
trial("3 frames separate writes (0.05s)", None) if False else None
# separate writes
s,resp=connect(); s.setblocking(False); t0=time.time(); closed=None
while time.time()-t0<0.3:
    r,_,_=select.select([s],[],[],0.05)
    if r:
        try: recv_frame(s)
        except Exception: break
for i in range(3):
    s.sendall(frame(b"hello")); time.sleep(0.05)
while time.time()-t0<8:
    r,_,_=select.select([s],[],[],0.1)
    if r:
        try:
            o,d=recv_frame(s)
            if o==8: closed=time.time()-t0; break
        except Exception: closed=time.time()-t0; break
print(f"{'3 frames 3 writes':34s} closed={round(closed,1) if closed else '>8'}",flush=True)
s.close()
