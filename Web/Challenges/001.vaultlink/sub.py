import time, select
from ws import connect, recv_frame
cases=[]
for sp in ["admin","ops","vaultlink.admin","v2.admin","vaultlink.v2.admin","vaultlink","feed","rates","v1"]:
    cases.append((f"sub:{sp}", {"Sec-WebSocket-Protocol":sp}))
for org in ["http://127.0.0.1","http://localhost","https://relay.internal","http://vaultlink.internal"]:
    cases.append((f"origin:{org}", {"Origin":org}))
for name,h in cases:
    try:
        s,resp=connect(extra_headers=h); s.setblocking(False)
        out=[]; end=time.time()+0.8
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        print(f"{name:36s}", out)
    except Exception as e: print(name,"EXC",e)
