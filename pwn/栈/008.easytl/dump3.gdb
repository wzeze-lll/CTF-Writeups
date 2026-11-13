set pagination off
set confirm off
set follow-fork-mode child
break *0x40320a
commands
silent
printf "SNI_CB called ssl=%p\n", $rdi
continue
end
break *0x40317f
commands
silent
printf "MEMCPY_PATH type=0x%x actuallen=%d\n", *(int*)($rbp-0x1c), *(int*)0x970f68
continue
end
break *0x4030d5
commands
silent
printf "INFO type=0x%x sni=%p snilen=%d psklen=%d curlen=%d\n", $esi, *(void**)0x970f50, *(int*)0x970f58, *(int*)0x970f48, *(int*)0x970f68
continue
end
run
