import time, select
from ws import connect, recv_frame
def trial(label, lines, cap=12):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    for ln in lines:
        s.sendall(ln+b"\n")
        time.sleep(0.35)
        while True:
            r,_,_=select.select([s],[],[],0.05)
            if not r: break
            try:
                o,d=recv_frame(s); frames.append((o,d[:100]))
            except Exception: frames.append("EOF"); break
    closed=None
    while time.time()-t0<cap:
        r,_,_=select.select([s],[],[],0.2)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:100]))
                if o==8: closed=time.time()-t0; break
            except Exception: closed=time.time()-t0; break
    extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
    print(f"{label:34s} closed={round(closed,1) if closed else '>12'} extra={extra}",flush=True)
    s.close()
tests=[
 ("ident/sub", [b"IDENTIFY guest", b"SUBSCRIBE rates"]),
 ("lower", [b"identify guest", b"subscribe rates"]),
 ("rates partner", [b"IDENTIFY rates.partner-forex.example.com", b"SUBSCRIBE rates"]),
 ("hello/sub", [b"HELLO guest", b"SUBSCRIBE rates"]),
 ("sub only", [b"SUBSCRIBE rates"]),
 ("ident only", [b"IDENTIFY guest"]),
]
for l,ls in tests: trial(l,ls)
