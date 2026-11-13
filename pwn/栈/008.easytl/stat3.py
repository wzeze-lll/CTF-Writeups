import socket,ssl
host="127.0.0.1"; port=2443
def one(sni):
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    try:
        s=ctx.wrap_socket(socket.create_connection((host,port),timeout=5), server_hostname=sni)
        s.close(); return True
    except Exception:
        return False
tests=[("a"*63+".com"), ("a"*60+".example.com"), ("example.com"), ("qiangwangbei.com"),
       ("a"*4+".com"), ("a"*10+".com"), ("a"*20+".com"), ("a"*40+".com"), ("a"*80+".com"), ("a"*200)]
for t in tests:
    print(f"len={len(t):4d} {'OK' if one(t) else 'FAIL'}  {t[:30]}...")
