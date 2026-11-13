import time, select, threading
from ws import connect, recv_frame, send_frame
def monitor(send_interval, label, dur=90):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); closed=None; last=time.time()
    while time.time()-t0<dur:
        r,_,_=select.select([s],[],[],0.2)
        if r:
            try:
                op,d=recv_frame(s)
                if op==8: closed=time.time()-t0; break
            except Exception:
                closed=time.time()-t0; break
        if send_interval and time.time()-last>send_interval:
            try: send_frame(s,b"keepalive")
            except Exception: closed=closed or time.time()-t0; break
            last=time.time()
    print(label,"closed after", round(closed,1) if closed else ">90s", flush=True)
    try: s.close()
    except: pass
ths=[threading.Thread(target=monitor,args=(None,"idle")),
     threading.Thread(target=monitor,args=(8,"send every 8s"))]
[t.start() for t in ths]; [t.join() for t in ths]
