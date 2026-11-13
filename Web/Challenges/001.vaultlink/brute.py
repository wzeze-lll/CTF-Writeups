import time, select
from ws import connect, send_frame, recv_frame
msgs=["IDENTIFY guest","identify guest","IDENTIFY","identify",
'{"cmd":"identify","id":"guest"}','{"type":"identify","id":"guest"}',
'{"op":"identify","partner":"guest"}','{"action":"identify"}',
"SUBSCRIBE rates","subscribe rates",'{"cmd":"subscribe","feed":"rates"}',
"HELP","help","STATUS","FEEDS","LIST",'{"cmd":"list"}',
"AUTH admin","AUTH","auth admin",'{"cmd":"auth","user":"admin"}']
for m in msgs:
    try:
        s,resp=connect(); s.setblocking(False)
        init=[]
        end=time.time()+0.7
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: init.append(recv_frame(s)[1])
                except Exception: break
        send_frame(s,m)
        out=[]; end=time.time()+1.2
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try:
                    op,d=recv_frame(s); out.append(d)
                except Exception as e: out.append(b"EOF"); break
        print(repr(m),"init",init,"->",out)
        s.close()
    except Exception as e:
        print(repr(m),"EXC",e)
