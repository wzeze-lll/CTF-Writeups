import time, select
from ws import connect, recv_frame
cases=[("X-Forwarded-For","127.0.0.1"),("X-Forwarded-For","127.0.0.1, 127.0.0.1"),
("X-Real-IP","127.0.0.1"),("Forwarded","for=127.0.0.1"),("X-Client-IP","127.0.0.1"),
("X-Originating-IP","127.0.0.1"),("True-Client-IP","127.0.0.1"),("CF-Connecting-IP","127.0.0.1"),
("X-Forwarded-Host","relay.internal"),("X-Forwarded-Server","relay"),("X-Host","relay"),
("X-Forwarded-Proto","internal"),("X-Env","production"),("X-Namespace","internal"),
("X-Scope","admin"),("X-Scope","ops"),("X-Permissions","admin"),("X-Permission","admin"),
("X-Groups","ops"),("X-Group","ops"),("X-Team","ops"),("X-Department","ops")]
for k,v in cases:
    try:
        s,resp=connect(extra_headers={k:v}); s.setblocking(False)
        out=[]; end=time.time()+0.8
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        rdy=[x for x in out if isinstance(x,bytes) and x.startswith(b"READY")]
        print(f"{k}: {v:24s}", rdy if rdy else out)
    except Exception as e: print(k,"EXC",str(e)[:40])
