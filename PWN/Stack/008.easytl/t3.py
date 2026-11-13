import socket,ssl,struct,hashlib,time
def conn():
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    return ctx.wrap_socket(socket.create_connection(("host.docker.internal",1443),timeout=5))
s=conn()
s.sendall(struct.pack("<I",0x89954D3E)+b"\x00"*16)   # GET with bogus hash
time.sleep(0.3)
try: print("resp:", s.recv(100))
except Exception as e: print("err:", type(e).__name__)
