set pagination off
set confirm off
set follow-fork-mode child
break *0x40304d
commands
silent
printf "CANARY=%#lx\n", *(unsigned long*)($fs_base+0x28)
continue
end
run
