import socket, base64, os, struct, sys, json, time

GW=("127.0.0.1",24606)
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081/ws"

def mask(data):
    k=os.urandom(4)
    return k, bytes(b^k[i%4] for i,b in enumerate(data))

def send_frame(s, data, op=0x1):
    if isinstance(data,str): data=data.encode()
    k,m=mask(data)
    ln=len(data)
    h=bytes([0x80|op])
    if ln<126: h+=bytes([0x80|ln])
    elif ln<65536: h+=bytes([0x80|126])+struct.pack(">H",ln)
    else: h+=bytes([0x80|127])+struct.pack(">Q",ln)
    s.sendall(h+k+m)

def recv_exact(s,n):
    b=b""
    while len(b)<n:
        c=s.recv(n-len(b))
        if not c: raise EOFError
        b+=c
    return b

def recv_frame(s):
    b1,b2=recv_exact(s,2)
    op=b1&0xf; ln=b2&0x7f
    if ln==126: ln=struct.unpack(">H",recv_exact(s,2))[0]
    elif ln==127: ln=struct.unpack(">Q",recv_exact(s,8))[0]
    if b2&0x80: mk=recv_exact(s,4); data=bytes(x^mk[i%4] for i,x in enumerate(recv_exact(s,ln)))
    else: data=recv_exact(s,ln)
    return op,data

def connect(extra_headers=None, inner=None):
    inner = inner or INNER
    s=socket.create_connection(GW, timeout=10)
    req=(f"GET /api/proxy?url={inner} HTTP/1.1\r\nHost: 127.0.0.1:24606\r\n"
         "Upgrade: websocket\r\nConnection: Upgrade\r\n"
         f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
         "Sec-WebSocket-Version: 13\r\n")
    if extra_headers:
        for k,v in extra_headers.items(): req+=f"{k}: {v}\r\n"
    req+="\r\n"
    s.sendall(req.encode())
    resp=b""
    while b"\r\n\r\n" not in resp:
        c=s.recv(1)
        if not c: break
        resp+=c
    return s, resp.decode(errors="replace")

if __name__=="__main__":
    s,resp=connect()
    print(resp)
    for _ in range(3):
        try:
            op,d=recv_frame(s); print(op,d)
        except Exception as e:
            print("ERR",e); break
    for msg in sys.argv[1:]:
        print(">>",msg); send_frame(s,msg)
        try:
            op,d=recv_frame(s); print(op,d)
        except Exception as e:
            print("ERR",e); break
