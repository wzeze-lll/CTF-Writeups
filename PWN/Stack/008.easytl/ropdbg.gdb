set pagination off
set confirm off
set follow-fork-mode child
break *0x403097
commands
silent
set *(unsigned long*)($rsi+0x58) = *(unsigned long*)($fs_base+0x28)
printf "canary patched, len=%ld\n", $rdx
continue
end
break *0x4251bd
commands
silent
printf "ROP pop_rdi hit target=%#lx\n", *(unsigned long*)$rsp
continue
end
break *0x4020c2
commands
silent
printf "SYSCALL rax=%ld rdi=%#lx rsi=%#lx rdx=%#lx\n", $rax, $rdi, $rsi, $rdx
continue
end
run
