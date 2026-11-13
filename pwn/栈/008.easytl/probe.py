import socket, ssl, struct, hashlib, time, sys

ADD, ENC, DEC, GET, UPD, DEL = 0x38432A87, 0x6C5A5850, 0x363BBED5, 0x89954D3E, 0xDC375626, 0xD21FEF03

def conn(host="127.0.0.1", port=1443):
    c = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    c.minimum_version = ssl.TLSVersion.TLSv1_3
    c.maximum_version = ssl.TLSVersion.TLSv1_3
    return c.wrap_socket(socket.create_connection((host, port), timeout=6))

def cmd(s, c, payload=b"", wait=0.25, n=4096):
    s.sendall(struct.pack("<I", c) + payload)
    time.sleep(wait)
    s.settimeout(1.5)
    try:
        return s.recv(n)
    except Exception:
        return None

d = b"persist-test"
s = conn()
print("add:", cmd(s, ADD, b"A"*16 + b"B"*16 + struct.pack("<I", len(d)) + d))
print("get1:", cmd(s, GET, hashlib.md5(d).digest()))
s2 = conn()
print("get2:", cmd(s2, GET, hashlib.md5(d).digest()))
