import socket,ssl,struct,hashlib,time
def conn():
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    return ctx.wrap_socket(socket.create_connection(("host.docker.internal",1443),timeout=5))
s=conn(); print("hs ok"); time.sleep(1)
s.settimeout(3)
try:
    print("idle recv:", s.recv(10))
except Exception as e: print("idle err:", type(e).__name__, e)
try:
    s.sendall(b"\x87\x2a\x43\x38" + b"A"*16+b"B"*16+struct.pack("<I",11)+b"hello world")
    print("sent add")
except Exception as e: print("send err", e)
time.sleep(0.5)
try: print("recv2:", s.recv(100))
except Exception as e: print("recv2 err:", type(e).__name__, e)
try:
    s2=conn(); print("second conn ok")
except Exception as e: print("second conn err", type(e).__name__, e)
