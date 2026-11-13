import requests
base="http://127.0.0.1:24606"
paths=["/","/docs","/api","/api/","/api/proxy","/api/rates","/api/settlement","/api/ledger","/api/feeds",
"/health","/healthz","/status","/metrics","/robots.txt","/openapi.json","/swagger","/api-docs",
"/admin","/console","/login","/partner","/partners","/v1","/v1/rates","/internal","/.git/config",
"/flag","/debug","/api/ws","/ws","/api/proxy/","/api/config","/api/partners","/api/session","/api/whoami"]
for p in paths:
    try:
        r=requests.get(base+p,timeout=6)
        t=r.text.replace("\n"," ")
        print(r.status_code,p,len(r.text),t[:100])
    except Exception as e: print("ERR",p,e)
