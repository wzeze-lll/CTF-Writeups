import time, select
from ws import connect, recv_frame
cases=[
 ("X-Forwarded-Client-Cert","CN=ops"),
 ("X-Forwarded-Client-Cert","By=spiffe://vaultlink/ns/internal/sa/ops;Subject=\"CN=ops\""),
 ("X-SSL-Client-S-DN","CN=ops"),
 ("X-Client-Cert","CN=ops"),
 ("X-Client-DN","CN=ops"),
 ("X-Forwarded-Tls-Client-Cert","CN=ops"),
 ("X-Client-Subject","CN=ops"),
 ("X-Forwarded-Client-Subject","CN=ops"),
 ("X-Authenticated-User","ops"),
 ("X-Authenticated-Userid","ops"),
 ("X-Auth-Request-User","ops"),
 ("X-Auth-Request-Email","ops@vaultlink.internal"),
 ("Remote-User","ops"),
 ("X-Webauth-User","ops"),
]
for k,v in cases:
    try:
        s,resp=connect(extra_headers={k:v}); s.setblocking(False)
        out=[]; end=time.time()+0.8
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.08)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        rdy=[x for x in out if isinstance(x,bytes) and x.startswith(b"READY")]
        print(f"{k:32s} {v[:30]:32s} {rdy}",flush=True)
    except Exception as e: print(k,"EXC",str(e)[:40])
