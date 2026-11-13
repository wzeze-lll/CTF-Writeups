import socket, ssl, sys, time
host=sys.argv[1]; port=int(sys.argv[2]); sni=sys.argv[3]
ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
ctx.minimum_version=ssl.TLSVersion.TLSv1_3; ctx.maximum_version=ssl.TLSVersion.TLSv1_3
raw=socket.create_connection((host,port),timeout=8)
try:
    s=ctx.wrap_socket(raw, server_hostname=sni)
except Exception as e:
    print("hs err", e); sys.exit()
print("[*] hs ok")
# send close_notify alert (client -> server) = read alert event
raw.sendall(bytes([0x15,0x03,0x03,0x00,0x02,0x01,0x00]))
time.sleep(0.5)
raw.settimeout(2)
out=b""
try:
    while True:
        b=raw.recv(4096)
        if not b: break
        out+=b
except Exception: pass
print("[*] raw after alert:", out)
