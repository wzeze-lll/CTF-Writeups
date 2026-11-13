import asyncio, sys, time

HOST = "127.0.0.1"

async def probe(port, sem, hits):
    async with sem:
        try:
            r, w = await asyncio.wait_for(asyncio.open_connection(HOST, port), timeout=3)
        except Exception:
            return
        data = b""
        try:
            data = await asyncio.wait_for(r.read(256), timeout=0.6)
        except Exception:
            pass
        w.close()
        if data:
            hits.append((port, data[:120]))

async def main(lo, hi, conc):
    sem = asyncio.Semaphore(conc)
    hits = []
    t0 = time.time()
    tasks = [probe(p, sem, hits) for p in range(lo, hi)]
    await asyncio.gather(*tasks)
    print("done", hi-lo, "ports in", round(time.time()-t0,1), "s; hits:", len(hits))
    for p, d in sorted(hits):
        print(p, repr(d))

if __name__ == "__main__":
    lo, hi, conc = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    asyncio.run(main(lo, hi, conc))
