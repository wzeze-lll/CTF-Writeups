import time, select
from ws import connect, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
qs=["identify=guest&subscribe=rates","identify=ops&subscribe=ledger","identify=guest&subscribe=ledger",
f"identify={TOK}&subscribe=ledger","identify=admin&subscribe=ledger","identify=guest&subscribe=all",
"identify=rates&subscribe=rates","subscribe=rates&identify=guest"]
for q in qs:
    inner=f"http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws?{q}"
    try:
        s,resp=connect(inner=inner); s.setblocking(False)
        t0=time.time(); frames=[]; closed=None
        while time.time()-t0<6:
            r,_,_=select.select([s],[],[],0.2)
            if r:
                try:
                    o,d=recv_frame(s); frames.append((o,d[:100]))
                    if o==8: closed="close"; break
                except Exception: closed="EOF"; break
        extra=[f for f in frames if f[1]!=b'READY guest' and not f[1].startswith(b'SESSION')]
        print(f"{q[:44]:46s} closed={closed} extra={extra}",flush=True)
        s.close()
    except Exception as e: print(q,"EXC",str(e)[:40])
