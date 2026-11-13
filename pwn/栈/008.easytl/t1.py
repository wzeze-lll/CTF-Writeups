import socket,ssl,struct,hashlib,time
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
s=ctx.wrap_socket(socket.create_connection(("host.docker.internal",1443),timeout=5))
data=b"hello world"; key=b"A"*16; iv=b"B"*16
s.sendall(struct.pack("<I",0x38432A87)+key+iv+struct.pack("<I",len(data))+data)
time.sleep(0.3)
print("sent add")
s.sendall(struct.pack("<I",0x89954D3E)+hashlib.sha256(data).digest()[:16])
time.sleep(0.3)
try:
    print("recv:",s.recv(100))
except Exception as e:
    print("err",e)
