import time, select
from ws import connect, recv_frame
names=["X-Partner-Id","X-Partner","X-Identity","X-User","X-Role","X-Partner-Role",
"X-VaultLink-Partner","X-VaultLink-Identity","X-Vaultlink-Identity","X-Vaultlink-Session",
"X-Session-Id","X-Forwarded-User","X-Auth-User","X-Auth-Role","X-Admin","X-Ops","Partner-Id",
"Identity","Role","User","X-Partner-Name","X-Partner-Key","X-Api-Key","Api-Key","X-Token",
"X-Vault-Session","X-Session","X-Partner-Token","X-Client-Id"]
for n in names:
    try:
        s,resp=connect(extra_headers={n:"ops"}); s.setblocking(False)
        out=[]; end=time.time()+0.7
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: break
        s.close()
        flag = "CHANGED" if any(b"ops" in x for x in out) else ""
        print(f"{n:24s}", out, flag)
    except Exception as e: print(n,"ERR",e)
