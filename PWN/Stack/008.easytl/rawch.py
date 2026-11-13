import socket, struct, sys, binascii

def ch(sni):
    ext = b""
    # server_name
    name = sni.encode()
    sn = b"\x00" + struct.pack("!H", len(name)) + name
    ext += struct.pack("!HH", 0, len(sn)) + sn
    # supported_groups x25519
    ext += struct.pack("!HH", 10, 4) + struct.pack("!H", 2) + struct.pack("!H", 0x001d)
    # signature_algorithms
    sa = struct.pack("!H",2)+struct.pack("!H",0x0403)
    ext += struct.pack("!HH", 13, len(sa)) + sa
    # supported_versions
    ext += struct.pack("!HH", 43, 3) + b"\x02\x03\x04"
    # key_share x25519
    ks = struct.pack("!H", 0x001d) + struct.pack("!H", 32) + bytes(range(32))
    ext += struct.pack("!HH", 51, len(ks)+2) + struct.pack("!H", len(ks)) + ks
    body = b"\x03\x03" + bytes(32) + b"\x00" + b"\x00\x02\x13\x02" + b"\x01\x00" + struct.pack("!H", len(ext)) + ext
    hs = b"\x01" + struct.pack("!I", len(body))[1:] + body
    return b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs

for sni in ("a.com","b","example.com"):
    s=socket.create_connection(("127.0.0.1",2443),timeout=6); s.settimeout(4)
    s.sendall(ch(sni))
    out=b""
    try:
        while len(out)<4096:
            b=s.recv(4096)
            if not b: break
            out+=b
    except Exception: pass
    print(sni, "->", len(out), "bytes:", out[:80].hex())
    s.close()
