import time, select
from ws import connect, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
base="http://rates.partner-forex.example.com"
variants=[
 f"{base}\\ops@127.0.0.1:8081/ws",
 f"{base}\\ops:x@127.0.0.1:8081/ws",
 f"{base}\\admin@127.0.0.1:8081/ws",
 f"{base}\\admin:{TOK}@127.0.0.1:8081/ws",
 f"{base}\\ops:ops@127.0.0.1:8081/ws",
 f"{base}\\\\ops@127.0.0.1:8081/ws",
 f"{base}\\@ops@127.0.0.1:8081/ws",
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
