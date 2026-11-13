import hashlib, sys
V="cf8303ef7e9fc6f51baf27b6e2c8763bd199a0a24c5294bcdaca3ddef6e47864"
N=int(sys.argv[1]); start=int(sys.argv[2]); step=int(sys.argv[3])
h=lambda s: hashlib.sha256(s.encode()).hexdigest()
found=[]
for a in range(start,N,step):
    sa=str(a)
    for b in range(N):
        sab=sa+";"+str(b)
        for c in range(N):
            body=h(sab+";"+str(c))[:32]
            if h("ns::"+body)==V:
                print("HIT",a,b,c,flush=True); found.append((a,b,c))
print("done",start,found,flush=True)
