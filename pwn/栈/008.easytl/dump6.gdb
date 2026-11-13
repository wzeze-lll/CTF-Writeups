set pagination off
set confirm off
set follow-fork-mode child
break *0x402dbb
commands
silent
printf "PSKCB enter id_len=%ld id=%.32s\n", $rdx, $rsi
continue
end
break *0x402e88
commands
silent
printf "PSKCB set len=32 pskbuf=%p\n", $rax
continue
end
break *0x403011
commands
silent
printf "PSKCB FAILRET0\n"
continue
end
break *0x403018
commands
silent
printf "PSKCB SUCCESS sess=%p\n", *(void**)$rax
continue
end
run
