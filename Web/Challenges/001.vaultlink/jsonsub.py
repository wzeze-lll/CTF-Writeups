import time, select, json
from ws import connect, send_frame, recv_frame
msgs=[
 '{"subscribe":"rates"}', '{"feed":"rates"}', '{"channel":"rates"}', '{"topic":"rates"}',
 '{"type":"subscribe","name":"rates"}', '{"type":"sub","feed":"rates"}',
 '{"action":"subscribe","name":"rates"}', '{"cmd":"sub","feed":"rates"}',
 '{"op":"sub","feed":"rates"}', '{"subscribe":["rates"]}',
 'subscribe rates', 'rates', 'SUBSCRIBE:rates', 'SUB rates', 'sub:rates',
 '{"cmd":"subscribe","feed":"ledger"}', '{"type":"subscribe","feed":"ledger"}',
 '{"cmd":"subscribe","feed":"settlement"}',
]
for m in msgs:
    try:
        s,resp=connect(); s.setblocking(False)
        end=time.time()+0.5; init=[]
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: init.append(recv_frame(s)[1])
                except Exception: break
        send_frame(s,m)
        out=[]; end=time.time()+2.5
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.15)
            if r:
                try:
                    op,d=recv_frame(s)
                    if d not in (b"READY guest",) and not d.startswith(b"SESSION"):
                        out.append((op,d[:100]))
                except Exception: out.append("EOF"); break
        s.close()
        print(f"{m:52s}", out, flush=True)
    except Exception as e: print(m,"EXC",str(e)[:60])
    time.sleep(0.4)
