import socket, ssl, struct, hashlib, time, sys

CMD_ADD, CMD_ENC, CMD_DEC, CMD_GET, CMD_UPD, CMD_DEL = (
    0x38432A87, 0x6C5A5850, 0x363BBED5, 0x89954D3E, 0xDC375626, 0xD21FEF03)

M1 = bytes.fromhex("66558c3de56c1d3eddb3e8c3ec59e6d1")
M2 = bytes.fromhex("66448c3de56c4d3e11b3e8c4ec59e6d1")

def conn(host, port, timeout=8):
    c = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    c.minimum_version = ssl.TLSVersion.TLSv1_3
    c.maximum_version = ssl.TLSVersion.TLSv1_3
    s = socket.create_connection((host, port), timeout=timeout)
    return c.wrap_socket(s)

def recvall(s, n, t=2.0):
    s.settimeout(t)
    out = b""
    try:
        while len(out) < n:
            b = s.recv(n - len(out))
            if not b:
                break
            out += b
    except Exception:
        pass
    return out

def probe(host, port):
    try:
        s = conn(host, port)
    except Exception as e:
        return f"connect fail: {type(e).__name__}: {e}"
    info = f"{s.version()} {s.cipher()[0]}"
    r = []
    for name, key in (("M1", M1), ("M2", M2), ("zero", b"\x00"*16)):
        try:
            s.sendall(struct.pack("<I", CMD_GET) + key)
            r.append(f"{name}={recvall(s, 256, 1.5)!r}")
        except Exception as e:
            r.append(f"{name}=ERR {type(e).__name__}")
            break
    return info + " | " + " ".join(r)

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    ports = [int(x) for x in sys.argv[2:]] or [1443, 2443, 3443, 4443, 5443]
    for p in ports:
        print(p, probe(host, p))
