import time, select
from ws import connect, recv_frame, send_frame
def trial(label, seq, cap=8, gap=0.7):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]; i=0; closed=None; nxt=t0+0.2
    while time.time()-t0<cap:
        if i<len(seq) and time.time()>=nxt:
            p,op=seq[i]; send_frame(s,p,op); i+=1; nxt=time.time()+gap
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:40]))
                if o==8: closed=time.time()-t0; break
            except Exception: closed=time.time()-t0; break
    extra=[f for f in frames if f[1]!=b'READY guest' and not f[1].startswith(b'SESSION')]
    print(f"{label:40s} sent={i} closed={round(closed,1) if closed else '>8'} extra={extra}",flush=True)
    s.close()
trial("3 pings", [(b"a",9),(b"b",9),(b"c",9)])
trial("5 pings", [(b"a",9)]*5)
trial("2 text + ping", [(b"hello",1),(b"hello",1),(b"p",9)])
trial("ping + 3 text", [(b"p",9),(b"hello",1),(b"hello",1),(b"hello",1)])
