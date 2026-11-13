import time, select, threading
from ws import connect, recv_frame, send_frame
def trial(label, payload, op=1):
    try:
        s,resp=connect(); s.setblocking(False)
        t0=time.time()
        # drain init
        while time.time()-t0<0.6:
            r,_,_=select.select([s],[],[],0.05)
            if r:
                try: recv_frame(s)
                except Exception: break
        send_frame(s,payload,op)
        closed=None
        while time.time()-t0<70:
            r,_,_=select.select([s],[],[],0.2)
            if r:
                try:
                    o,d=recv_frame(s)
                    if o==8: closed=time.time()-t0; break
                except Exception:
                    closed=time.time()-t0; break
        print(f"{label:40s} closed after {round(closed,1) if closed else '>70'}",flush=True)
        s.close()
    except Exception as e:
        print(label,"EXC",e,flush=True)
trial("hello text", b"hello")
trial("IDENTIFY guest", b"IDENTIFY guest")
trial("SUBSCRIBE rates", b"SUBSCRIBE rates")
trial("json", b'{"cmd":"subscribe","feed":"rates"}')
trial("empty text", b"")
trial("binary hello", b"hello", 2)
