import time, select, threading
from ws import connect, recv_frame
feeds=["rates","settlement","ledger"]
def run(feed):
    inner=f"http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws?feed={feed}"
    try:
        s,resp=connect(inner=inner); s.setblocking(False)
        out=[]; t0=time.time()
        while time.time()-t0<60:
            r,_,_=select.select([s],[],[],0.5)
            if r:
                try:
                    op,d=recv_frame(s); out.append((round(time.time()-t0,1),op,d[:60]))
                    if op==8: break
                except Exception: out.append("EOF"); break
        print(feed, resp.split("\r\n")[0], out, flush=True)
        s.close()
    except Exception as e:
        print(feed,"EXC",e, flush=True)
ths=[threading.Thread(target=run,args=(f,)) for f in feeds]
[t.start() for t in ths]; [t.join() for t in ths]
