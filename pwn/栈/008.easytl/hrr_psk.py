import socket, struct, os, sys, time

MAGIC_ID = b"1401518dc5d7641ccd41593a5d812410"   # 服务端硬编码 PSK identity


def ext(t, data):
    return struct.pack("!HH", t, len(data)) + data


def client_hello(sni, key_share_pub=None, session_id=b"\x00" * 32, cookie=None, with_psk=False):
    exts = b""
    name = sni.encode()
    sn = b"\x00" + struct.pack("!H", len(name)) + name
    exts += ext(0, struct.pack("!H", len(sn)) + sn)                  # server_name
    exts += ext(10, struct.pack("!H", 2) + struct.pack("!H", 0x001D))  # supported_groups
    sigs = struct.pack("!H", 10) + b"".join(struct.pack("!H", x) for x in (0x0804, 0x0403, 0x0503, 0x0401, 0x0201))
    exts += ext(13, sigs)  # sig algs
    exts += ext(43, b"\x02\x03\x04")                                   # supported_versions 1.3
    if cookie is not None:
        exts += ext(44, struct.pack("!H", len(cookie)) + cookie)       # cookie
    if key_share_pub is None:
        exts += ext(51, b"\x00\x00")                                   # empty key_share -> HRR
    else:
        entry = struct.pack("!H", 0x001D) + struct.pack("!H", len(key_share_pub)) + key_share_pub
        exts += ext(51, struct.pack("!H", len(entry)) + entry)
    if with_psk:
        exts += ext(45, b"\x01\x01")                                   # psk_key_exchange_modes: psk_dhe_ke
        ident = struct.pack("!H", len(MAGIC_ID)) + MAGIC_ID + struct.pack("!I", 0)
        binders = b"\x30" + b"\x00" * 48
        psk = struct.pack("!H", len(ident)) + ident + struct.pack("!H", len(binders)) + binders
        exts += ext(41, psk)
    body = (b"\x03\x03" + os.urandom(32) + bytes([len(session_id)]) + session_id +
            b"\x00\x02\x13\x02" + b"\x01\x00" + struct.pack("!H", len(exts)) + exts)
    return b"\x01" + struct.pack("!I", len(body))[1:] + body


def send_hs(sock, hs):
    sock.sendall(b"\x16\x03\x01" + struct.pack("!H", len(hs)) + hs)


def read_records(sock, timeout=2.0):
    sock.settimeout(timeout)
    out = b""
    try:
        while True:
            b = sock.recv(4096)
            if not b:
                break
            out += b
            if len(b) < 4096:
                break
    except Exception:
        pass
    return out


def parse_server_hello(rec):
    """returns (is_hrr, cookie, group) or None"""
    if len(rec) < 5 or rec[0] != 0x16:
        return None
    p = 5
    if rec[p] != 0x02:
        return None
    ln = int.from_bytes(rec[p + 1:p + 4], "big")
    hs = rec[p + 4:p + 4 + ln]
    legacy_ver = hs[0:2]
    random = hs[2:34]
    sid_len = hs[34]
    q = 35 + sid_len
    cipher = hs[q:q + 2]
    q += 2
    q += 1  # compression
    elen = int.from_bytes(hs[q:q + 2], "big")
    q += 2
    exts = hs[q:q + elen]
    HRR_RANDOM = bytes.fromhex("cf21ad74e59a6111be1d8c021e65b891c2a211167abb8c5e079e09e2c8a8339c")
    is_hrr = (random == HRR_RANDOM)
    cookie = None
    group = None
    i = 0
    while i + 4 <= len(exts):
        et = int.from_bytes(exts[i:i + 2], "big")
        el = int.from_bytes(exts[i + 2:i + 4], "big")
        data = exts[i + 4:i + 4 + el]
        if et == 44:
            cookie = data[2:]
        if et == 51 and len(data) >= 2:
            group = int.from_bytes(data[2:4], "big")
        i += 4 + el
    return is_hrr, cookie, group


def run(host, port, sni):
    s = socket.create_connection((host, port), timeout=8)
    send_hs(s, client_hello(sni))
    rec = read_records(s)
    print(f"[*] after CH1: {len(rec)} bytes: {rec[:16].hex()}")
    info = parse_server_hello(rec)
    if not info:
        print("[!] no server hello"); return
    is_hrr, cookie, group = info
    print(f"[*] HRR={is_hrr} cookie={cookie.hex() if cookie else None} group={group}")
    if not is_hrr:
        print("[!] no HRR; abort"); return
    # CH2 with key share + PSK
    send_hs(s, client_hello(sni, key_share_pub=bytes(range(32)), cookie=cookie, with_psk=True))
    rec2 = read_records(s, 2.0)
    print(f"[*] after CH2: {len(rec2)} bytes: {rec2.hex()}")
    # send alert (close_notify) to provoke read-alert callback
    try:
        s.sendall(bytes([0x15, 0x03, 0x03, 0x00, 0x02, 0x01, 0x00]))
    except Exception as e:
        print("[!] send alert failed:", e)
    rec3 = read_records(s, 2.0)
    print(f"[*] after alert: {len(rec3)} bytes: {rec3.hex()}")


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1443
    sni = sys.argv[3] if len(sys.argv) > 3 else ("a" * 60 + "." + "b" * 60 + ".example.com")
    run(host, port, sni)
