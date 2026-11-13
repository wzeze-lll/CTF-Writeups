import time, select
from ws import connect, recv_frame
def trial(label, payload, cap=5):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.3:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    s.sendall(payload)
    closed=None
    while time.time()<t0+cap:
        r,_,_=select.select([s],[],[],0.15)
        if r:
            try:
                o,d=recv_frame(s); frames.append((o,d[:150]))
                if o==8: closed="close"; break
            except Exception: closed="EOF"; break
    extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
    print(f"{label:30s} closed={closed} extra={extra}",flush=True)
    s.close()
trial("http get /", b"GET / HTTP/1.1\r\nHost: 127.0.0.1:8081\r\n\r\n")
trial("http get /flag", b"GET /flag HTTP/1.1\r\nHost: x\r\n\r\n")
trial("http post", b"POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 3\r\n\r\nabc")
trial("bad utf8 frame one write", b"\x81\x82\x00\x00\x00\x00\xff\xfe")
