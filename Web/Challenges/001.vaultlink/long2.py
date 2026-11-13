import time, select, threading
from ws import connect, recv_frame
def run(feed):
    s,resp=connect(); s.setblocking(False)
    t0=time.time(); frames=[]
    while time.time()-t0<0.4:
        r,_,_=select.select([s],[],[],0.05)
        if r:
            try: frames.append(recv_frame(s)[1])
            except Exception: break
    s.sendall(f"IDENTIFY guest\nSUBSCRIBE {feed}\n".encode())
    closed=None
    while time.time()-t0<75:
        r,_,_=select.select([s],[],[],0.3)
        if r:
            try:
                o,d=recv_frame(s); frames.append((round(time.time()-t0,1),o,d[:150]))
                if o==8: closed="close"; break
            except Exception: closed=time.time()-t0; break
    print(feed,"closed",closed,"frames",[f for f in frames if not (isinstance(f[0],int) and f[0] in (1,)) or True][:5],len(frames),flush=True)
    s.close()
ts=[threading.Thread(target=run,args=(f,)) for f in ["rates","ledger","settlement"]]
[t.start() for t in ts]; [t.join() for t in ts]
