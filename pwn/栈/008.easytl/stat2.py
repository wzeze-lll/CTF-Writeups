import socket,ssl,sys
host="127.0.0.1"; port=2443
def one(sni):
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    try:
        s=ctx.wrap_socket(socket.create_connection((host,port),timeout=5), server_hostname=sni)
        s.close(); return True
    except Exception:
        return False
tests=["a","ab","abc","abcd","a.com","abcde","abcdef","abcdefg","x.com","aa.com","ab.com","a.c","b","c","com","localhost","a.b","0","aa"]
for t in tests:
    print(f"{t!r:14} {'OK' if one(t) else 'FAIL'}")
