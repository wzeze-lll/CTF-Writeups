import socket, sys, concurrent.futures as cf
HOST=sys.argv[1]
ports=[22,80,443,1080,1883,1884,2375,2376,3000,3306,5000,5432,6379,8000,8001,8080,8081,
       8443,8888,9000,9090,9200,10000,11211,1337,1883,27017,2883,2884,50000,50070,61616,
       18083,18082,28083,38883,18830,28830,8883,18803,18080,3128,5900,22,21,23,25,110,143]
ports=sorted(set(ports))
def chk(p):
    try:
        s=socket.create_connection((HOST,p),2); s.settimeout(1)
        try:
            s.send(b'\r\n'); b=s.recv(64)
        except Exception: b=b''
        s.close(); return (p, 'OPEN', b[:40])
    except Exception: return None
with cf.ThreadPoolExecutor(40) as ex:
    for r in ex.map(chk, ports):
        if r: print('port %-6d OPEN  %r'%(r[0], r[2]))
print('scan done', len(ports), 'ports')
