import hashlib
from Crypto.Cipher import AES
B=open('model_B.bin','rb').read()
target=B[:4]; want=b'PK\x03\x04'
ks=(int.from_bytes(target,'big')^int.from_bytes(want,'big')).to_bytes(4,'big')
print('needed keystream[0:4] =',ks.hex(),flush=True)
hits=[]
N=1<<24
for mode in ('raw4be','raw4le','sha4'):
    for k in range(N):
        if mode=='raw4be': key=k.to_bytes(16,'big')
        elif mode=='raw4le': key=k.to_bytes(16,'little')
        else: key=hashlib.sha256(k.to_bytes(4,'little')).digest()[:16]
        blk=AES.new(key,AES.MODE_ECB).encrypt(b'\x00'*16)
        if blk[:4]==ks:
            print('HIT',mode,k,flush=True); hits.append((mode,k))
    print('done',mode,flush=True)
print('hits',hits,flush=True)
