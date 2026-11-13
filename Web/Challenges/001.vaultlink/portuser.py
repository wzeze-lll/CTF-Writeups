import time, select
from ws import connect, recv_frame
variants=[
 "http://rates.partner-forex.example.com:8081\\@127.0.0.1:8081/ws",
 "http://rates.partner-forex.example.com:80\\@127.0.0.1:8081/ws",
 "http://rates.partner-forex.example.com:0\\@127.0.0.1:8081/ws",
 "http://rates.partner-forex.example.com:31337\\@127.0.0.1:8081/ws",
]
for v in variants:
    try:
        s,resp=connect(inner=v); s.setblocking(False)
        out=[]; end=time.time()+1.0
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        print(v,"=>",resp.split("\r\n")[0],out)
    except Exception as e: print(v,"EXC",e)
