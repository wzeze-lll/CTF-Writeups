set pagination off
set confirm off
set follow-fork-mode child
break *0x4030d5
commands
silent
printf "INFO type=0x%x psk=%p psklen=%d sni=%p snilen=%d curlen=%d\n", $esi, *(void**)0x970f40, *(int*)0x970f48, *(void**)0x970f50, *(int*)0x970f58, *(int*)0x970f68
continue
end
break *0x40304d
commands
silent
printf "MEMCPY len=%d src=%p\n", *(int*)0x970f68, *(void**)0x970f60
continue
end
run
