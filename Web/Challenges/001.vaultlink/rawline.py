import time, select
from ws import connect
payloads=[b"hello\n", b"IDENTIFY guest\n", b"SUBSCRIBE rates\n", b'{"cmd":"subscribe","feed":"rates"}\n', b"AUTH\n"]
for p in payloads:
    s,resp=connect(); s.setblocking(False)
    out=[]; end=time.time()+0.6
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(("init",s.recv(4096)))
            except Exception: break
    s.sendall(p)
    end=time.time()+1.5
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try:
                d=s.recv(4096)
                if not d: out.append(("EOF",b"")); break
                out.append(("raw",d))
            except Exception as e: out.append(("exc",str(e))); break
    print(p, out)
    s.close()
