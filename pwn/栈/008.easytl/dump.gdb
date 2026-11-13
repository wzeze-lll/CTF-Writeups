set pagination off
set confirm off
set follow-fork-mode child
break *0x40304d
commands
silent
printf "HIT40304d len=%ld src=%p psklen=%d snilen=%d\n", *(long*)0x970f68, *(void**)0x970f40, *(int*)0x970f48, *(int*)0x970f58
continue
end
run
