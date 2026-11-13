import time, select, os, struct
from ws import connect, send_frame, recv_frame

def trial(desc, headers=None, frames=()):
    try:
        s,resp=connect(extra_headers=headers); s.setblocking(False)
        out=[]
        def drain(t):
            end=time.time()+t
            while time.time()<end:
                r,_,_=select.select([s],[],[],0.1)
                if r:
                    try: out.append(recv_frame(s))
                    except Exception: out.append(("EOF",b"")); return False
            return True
        drain(0.8); send_frame(s,b"ping",0x9); drain(0.8)
        for f in frames:
            send_frame(s,f); drain(0.6)
        print(desc,"->",out)
        s.close()
    except Exception as e:
        print(desc,"EXC",e)

trial("ping only")
trial("xpartner-admin", {"X-Partner":"admin"})
trial("xpartnerid-admin", {"X-Partner-Id":"admin"})
trial("x-vaultlink-partner", {"X-VaultLink-Partner":"admin"})
trial("x-forwarded-user", {"X-Forwarded-User":"admin"})
trial("binary-json", frames=[b'{"cmd":"identify","id":"guest"}'])
