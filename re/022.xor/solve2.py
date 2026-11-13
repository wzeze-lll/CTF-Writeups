c = bytes.fromhex(
    "660a6b0c77264f2e4011780d5a3b55117019461f76224d23440e6706680f47324f"
)
p = bytes([c[0]]) + bytes(c[i] ^ c[i - 1] for i in range(1, len(c)))
print(p.decode())
