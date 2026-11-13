import socket,ssl
host="127.0.0.1"; port=2443
def one(sni):
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    try:
        s=ctx.wrap_socket(socket.create_connection((host,port),timeout=5), server_hostname=sni)
        s.close(); return True
    except Exception as e:
        return False
tests=[
 "a"*60+".example.com",
 "a"*60+"."+"b"*60+".example.com",
 "a"*60+"."+"b"*60+"."+"c"*20+".example.com",
 "x"*100+".qiangwangbei.com",
 "a"*63+".example.com",
]
for t in tests:
    print(f"len={len(t):4d} {'OK' if one(t) else 'FAIL'}  ...{t[-20:]}")
