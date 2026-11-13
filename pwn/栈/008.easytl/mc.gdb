set pagination off
set confirm off
set follow-fork-mode child
break *0x403097
commands
silent
printf "MEMCPY dst=%p src=%p len=%ld\n", $rdi, $rsi, $rdx
printf "canary_slot(rbp-8)=%#lx  src+0x58=%#lx\n", *(unsigned long*)($rbp-0x8), *(unsigned long*)($rsi+0x58)
x/8bx $rsi+0x50
continue
end
run
