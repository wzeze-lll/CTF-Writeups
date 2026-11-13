import time, select
from ws import connect, recv_frame
subs=["SUBSCRIBE rates","SUBSCRIBE reference-rates","SUBSCRIBE settlement-windows",
"SUBSCRIBE ledger-summaries","SUBSCRIBE ledger_summary","SUBSCRIBE all","SUBSCRIBE *",
"SUBSCRIBE internal","SUBSCRIBE admin",'{"subscribe":"rates"}',
'{"type":"subscribe","feed":"rates"}','{"cmd":"subscribe","feed":"rates"}',
"SUBSCRIBE v2 rates","SUBSCRIBE rates v2","SUB rates","SUBSCRIBE:rates"]
for s_ in subs:
    try:
        sock,resp=connect(); sock.setblocking(False)
        t0=time.time(); frames=[]
        while time.time()-t0<0.3:
            r,_,_=select.select([sock],[],[],0.05)
            if r:
                try: frames.append(recv_frame(sock)[1])
                except Exception: break
        sock.sendall((s_+"\n").encode())
        end=time.time()+7
        closed=None
        while time.time()<end:
            r,_,_=select.select([sock],[],[],0.2)
            if r:
                try:
                    o,d=recv_frame(sock); frames.append((o,d[:100]))
                    if o==8: closed="close"; break
                except Exception: closed="EOF"; break
        extra=[f for f in frames if f!=b'READY guest' and not (isinstance(f,bytes) and f.startswith(b'SESSION'))]
        print(f"{s_:38s} closed={closed} extra={extra}",flush=True)
        sock.close()
    except Exception as e: print(s_,"EXC",str(e)[:40])
