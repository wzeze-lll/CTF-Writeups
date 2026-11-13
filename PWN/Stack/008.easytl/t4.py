import socket,ssl,struct,hashlib,time
def conn():
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    return ctx.wrap_socket(socket.create_connection(("host.docker.internal",1443),timeout=5))
s=conn()
data=b"hello world"; key=b"A"*16; iv=b"B"*16
s.sendall(struct.pack("<I",0x38432A87)+key+iv+struct.pack("<I",len(data))+data)
time.sleep(0.3)
h=hashlib.md5(data).digest()
s.sendall(struct.pack("<I",0x89954D3E)+h)
time.sleep(0.3)
s.settimeout(3)
try: print("get:", s.recv(200))
except Exception as e: print("err", type(e).__name__)
# second get to test survival
try:
    s.sendall(struct.pack("<I",0x89954D3E)+h); time.sleep(0.3); print("get2:", s.recv(200))
except Exception as e: print("err2", type(e).__name__, e)
