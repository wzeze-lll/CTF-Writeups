import socket, struct, time, sys
host="127.0.0.1"
for port in (1443,):
    s=socket.create_connection((host,port),timeout=6); s.settimeout(3)
    print(port,"connected")
    try:
        print("banner:", s.recv(64))
    except Exception as e:
        print("no banner", type(e).__name__)
    try:
        s.sendall(b"GET / HTTP/1.0\r\n\r\n")
        time.sleep(0.3)
        print("http:", s.recv(256))
    except Exception as e:
        print("send err", type(e).__name__)
    try:
        s.sendall(struct.pack("<I",0x38432A87)+b"A"*16+b"B"*16+struct.pack("<I",5)+b"hello")
        time.sleep(0.4)
        print("cmd:", s.recv(256))
    except Exception as e:
        print("cmd err", type(e).__name__, e)
