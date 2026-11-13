import time, select, struct
from ws import connect, recv_frame
def trial(label, mode, n=5, gap=0.7):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); closed=None
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: recv_frame(s)
            except Exception: break
    sent=0; nxt=t0+0.2
    while time.time()-t0<8:
        if sent<n and time.time()>=nxt:
            if mode=="raw": s.sendall(b"hello\n")
            elif mode=="rawjson": s.sendall(b'{"cmd":"subscribe","feed":"rates"}\n')
            elif mode=="frame":
                p=b"hello"; s.sendall(b"\x81"+bytes([0x80|len(p)])+b"\x11\x22\x33\x44"+bytes(x^[0x11,0x22,0x33,0x44][i%4] for i,x in enumerate(p)))
            sent+=1; nxt=time.time()+gap
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try:
                o,d=recv_frame(s)
                if o==8: closed=time.time()-t0; break
            except Exception: closed=time.time()-t0; break
    print(f"{label:26s} sent={sent} closed={round(closed,1) if closed else '>8'}",flush=True)
    s.close()
trial("frames x5","frame")
trial("raw lines x5","raw")
trial("raw json lines x5","rawjson")
