import socket,ssl,sys
host="127.0.0.1"; port=int(sys.argv[1]) if len(sys.argv)>1 else 2443
def one(sni):
    ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
    try:
        s=ctx.wrap_socket(socket.create_connection((host,port),timeout=5), server_hostname=sni)
        s.close(); return True
    except Exception as e:
        return False
for sni in ("a.com","b","qiangwangbei.com",None):
    ok=sum(one(sni) for _ in range(8))
    print(f"sni={sni!r}: {ok}/8 ok")
