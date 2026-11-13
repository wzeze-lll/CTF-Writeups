import time, select, os
from ws import connect, send_frame, recv_frame
def t(desc, data, op=1):
    s,resp=connect(); s.setblocking(False)
    out=[]; end=time.time()+0.8
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s))
            except Exception: out.append("EOF"); break
    send_frame(s,data,op)
    end=time.time()+2.5
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try:
                f=recv_frame(s); out.append(f)
                if f[0]==8: break
            except Exception: out.append("EOF"); break
    print(desc,out); s.close()
t("invalid utf8", b"\xff\xfe\x00\x01", 1)
t("huge", b"A"*3000, 1)
t("close frame", b"\x03\xe8", 8)
t("ping", b"x", 9)
