import time, select
from ws import connect, recv_frame, send_frame
def trial(label, payload, n, gap=1.0, cap=40):
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time()
        while time.time()-t0<0.5:
            r,_,_=select.select([s],[],[],0.05)
            if r:
                try: recv_frame(s)
                except Exception: break
        sent=0; closed=None
        nextsend=t0+0.2
        while time.time()-t0<cap:
            if sent<n and time.time()>=nextsend:
                send_frame(s,payload); sent+=1; nextsend=time.time()+gap
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try:
                    o,d=recv_frame(s)
                    if o==8: closed=time.time()-t0; break
                except Exception:
                    closed=time.time()-t0; break
        print(f"{label:44s} n={n} closed={round(closed,1) if closed else '>40'}",flush=True)
        s.close()
    except Exception as e:
        print(label,n,"EXC",str(e)[:50],flush=True)
for n in [3,4,6]:
    trial("hello", b"hello", n)
for n in [3,4]:
    trial("json-sub", b'{"cmd":"subscribe","feed":"rates"}', n)
for n in [3,4]:
    trial("json-identify", b'{"type":"identify","id":"guest"}', n)
