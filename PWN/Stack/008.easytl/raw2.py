import socket, struct, time
host="127.0.0.1"; port=1443
s=socket.create_connection((host,port),timeout=6); s.settimeout(2)
data=b"hello"; key=b"A"*16; iv=b"B"*16
import hashlib
s.sendall(struct.pack("<I",0x38432A87)+key+iv+struct.pack("<I",len(data))+data)
time.sleep(0.3)
s.sendall(struct.pack("<I",0x89954D3E)+hashlib.md5(data).digest())
time.sleep(0.3)
try: print("resp:", s.recv(200))
except Exception as e: print("err", type(e).__name__)
