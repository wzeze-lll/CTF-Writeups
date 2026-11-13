import time, select
from ws import connect, recv_frame
paths=["/ws/rates","/ws/settlement","/ws/ledger","/ws/admin","/ws/internal","/ws/v2",
       "/ws?feed=rates","/ws?subscribe=rates","/ws?channel=rates","/ws?topic=rates",
       "/ws/rates/","/ws/1","/ws/0"]
for p in paths:
    inner=f"http://rates.partner-forex.example.com\\@127.0.0.1:8081{p}"
    try:
        s,resp=connect(inner=inner); s.setblocking(False)
        out=[]; end=time.time()+4.0
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.2)
            if r:
                try:
                    op,d=recv_frame(s); out.append((op,d[:80]))
                    if op==8: break
                except Exception: out.append("EOF"); break
        s.close()
        print(f"{p:26s}", resp.split("\r\n")[0], out)
    except Exception as e: print(p,"EXC",e)
