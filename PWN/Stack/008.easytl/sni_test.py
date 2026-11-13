import socket, ssl, sys

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 1443
sni_len = int(sys.argv[3]) if len(sys.argv) > 3 else 200

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.maximum_version = ssl.TLSVersion.TLSv1_3

sni = ("a" * (sni_len - 4)) + ".com"
raw = socket.create_connection((host, port), timeout=8)
try:
    s = ctx.wrap_socket(raw, server_hostname=sni)
    print("[*] handshake ok", s.version(), s.cipher()[0])
    s.close()
except Exception as e:
    print("[!] handshake err:", type(e).__name__, e)
    try:
        raw.close()
    except Exception:
        pass
