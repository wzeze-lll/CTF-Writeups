import asyncio, sys, time
HOST="127.0.0.1"
async def probe(p, sem, out):
    async with sem:
        try:
            r,w = await asyncio.wait_for(asyncio.open_connection(HOST,p), timeout=2.5)
        except Exception:
            return
        try:
            data = await asyncio.wait_for(r.read(128), timeout=0.9)
        except Exception:
            data = b""
        try: w.close()
        except Exception: pass
        if data:
            out.append((p,data))
async def main(lo,hi,conc):
    sem=asyncio.Semaphore(conc); out=[]; t0=time.time()
    await asyncio.gather(*[probe(p,sem,out) for p in range(lo,hi)])
    print("scan",lo,hi,"secs",round(time.time()-t0,1),"hits",len(out), flush=True)
    for p,d in sorted(out): print(p, repr(d[:100]), flush=True)
asyncio.run(main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])))
