<get_flag>:
  4007cb: 55                           	pushq	%rbp
  4007cc: 48 89 e5                     	movq	%rsp, %rbp
  4007cf: 48 83 ec 40                  	subq	$0x40, %rsp
  4007d3: 64 48 8b 04 25 28 00 00 00   	movq	%fs:0x28, %rax
  4007dc: 48 89 45 f8                  	movq	%rax, -0x8(%rbp)
  4007e0: 31 c0                        	xorl	%eax, %eax
  4007e2: bf 00 00 00 00               	movl	$0x0, %edi
  4007e7: e8 74 fe ff ff               	callq	0x400660 <time@plt>
  4007ec: 89 c7                        	movl	%eax, %edi
  4007ee: e8 5d fe ff ff               	callq	0x400650 <srand@plt>
  4007f3: c7 45 c4 00 00 00 00         	movl	$0x0, -0x3c(%rbp)
  4007fa: e9 7a 01 00 00               	jmp	0x400979 <get_flag+0x1ae>
  4007ff: e8 8c fe ff ff               	callq	0x400690 <rand@plt>
  400804: 89 c1                        	movl	%eax, %ecx
  400806: ba 1f 85 eb 51               	movl	$0x51eb851f, %edx       # imm = 0x51EB851F
  40080b: 89 c8                        	movl	%ecx, %eax
  40080d: f7 ea                        	imull	%edx
  40080f: c1 fa 06                     	sarl	$0x6, %edx
  400812: 89 c8                        	movl	%ecx, %eax
  400814: c1 f8 1f                     	sarl	$0x1f, %eax
  400817: 29 c2                        	subl	%eax, %edx
  400819: 89 d0                        	movl	%edx, %eax
  40081b: 89 45 cc                     	movl	%eax, -0x34(%rbp)
  40081e: 8b 45 cc                     	movl	-0x34(%rbp), %eax
  400821: 69 c0 c8 00 00 00            	imull	$0xc8, %eax, %eax
  400827: 29 c1                        	subl	%eax, %ecx
  400829: 89 c8                        	movl	%ecx, %eax
  40082b: 89 45 cc                     	movl	%eax, -0x34(%rbp)
  40082e: 83 7d cc 05                  	cmpl	$0x5, -0x34(%rbp)
  400832: 0f 87 33 01 00 00            	ja	0x40096b <get_flag+0x1a0>
  400838: 8b 45 cc                     	movl	-0x34(%rbp), %eax
  40083b: 48 8b 04 c5 c0 0b 40 00      	movq	0x400bc0(,%rax,8), %rax
  400843: ff e0                        	jmpq	*%rax
  400845: bf 5e 0b 40 00               	movl	$0x400b5e, %edi         # imm = 0x400B5E
  40084a: e8 b1 fd ff ff               	callq	0x400600 <puts@plt>
  40084f: 48 8d 45 d0                  	leaq	-0x30(%rbp), %rax
  400853: ba 28 00 00 00               	movl	$0x28, %edx
  400858: be 00 00 00 00               	movl	$0x0, %esi
  40085d: 48 89 c7                     	movq	%rax, %rdi
  400860: e8 cb fd ff ff               	callq	0x400630 <memset@plt>
  400865: 48 8d 45 d0                  	leaq	-0x30(%rbp), %rax
  400869: be 78 10 60 00               	movl	$0x601078, %esi         # imm = 0x601078
  40086e: 48 89 c7                     	movq	%rax, %rdi
  400871: e8 0a fe ff ff               	callq	0x400680 <strcat@plt>
  400876: 48 8d 45 d0                  	leaq	-0x30(%rbp), %rax
  40087a: be 90 10 60 00               	movl	$0x601090, %esi         # imm = 0x601090
  40087f: 48 89 c7                     	movq	%rax, %rdi
  400882: e8 f9 fd ff ff               	callq	0x400680 <strcat@plt>
  400887: 48 8d 45 d0                  	leaq	-0x30(%rbp), %rax
  40088b: 48 89 c6                     	movq	%rax, %rsi
  40088e: bf 6d 0b 40 00               	movl	$0x400b6d, %edi         # imm = 0x400B6D
  400893: b8 00 00 00 00               	movl	$0x0, %eax
  400898: e8 83 fd ff ff               	callq	0x400620 <printf@plt>
  40089d: e9 d3 00 00 00               	jmp	0x400975 <get_flag+0x1aa>
  4008a2: bf 70 0b 40 00               	movl	$0x400b70, %edi         # imm = 0x400B70
  4008a7: b8 00 00 00 00               	movl	$0x0, %eax
  4008ac: e8 6f fd ff ff               	callq	0x400620 <printf@plt>
  4008b1: e9 bf 00 00 00               	jmp	0x400975 <get_flag+0x1aa>
  4008b6: bf 83 0b 40 00               	movl	$0x400b83, %edi         # imm = 0x400B83
  4008bb: b8 00 00 00 00               	movl	$0x0, %eax
  4008c0: e8 5b fd ff ff               	callq	0x400620 <printf@plt>
  4008c5: e9 ab 00 00 00               	jmp	0x400975 <get_flag+0x1aa>
  4008ca: 48 c7 45 d0 00 00 00 00      	movq	$0x0, -0x30(%rbp)
  4008d2: c6 45 d8 00                  	movb	$0x0, -0x28(%rbp)
  4008d6: c6 45 d0 69                  	movb	$0x69, -0x30(%rbp)
  4008da: c6 45 d1 63                  	movb	$0x63, -0x2f(%rbp)
  4008de: c6 45 d2 75                  	movb	$0x75, -0x2e(%rbp)
  4008e2: c6 45 d3 67                  	movb	$0x67, -0x2d(%rbp)
  4008e6: c6 45 d4 60                  	movb	$0x60, -0x2c(%rbp)
  4008ea: c6 45 d5 6f                  	movb	$0x6f, -0x2b(%rbp)
  4008ee: c6 45 d6 66                  	movb	$0x66, -0x2a(%rbp)
  4008f2: c6 45 d7 7f                  	movb	$0x7f, -0x29(%rbp)
  4008f6: 48 8d 45 d0                  	leaq	-0x30(%rbp), %rax
  4008fa: 48 89 c6                     	movq	%rax, %rsi
  4008fd: bf 90 10 60 00               	movl	$0x601090, %edi         # imm = 0x601090
  400902: e8 79 fd ff ff               	callq	0x400680 <strcat@plt>
  400907: eb 6c                        	jmp	0x400975 <get_flag+0x1aa>
  400909: c7 45 c8 00 00 00 00         	movl	$0x0, -0x38(%rbp)
  400910: eb 51                        	jmp	0x400963 <get_flag+0x198>
  400912: 8b 45 c8                     	movl	-0x38(%rbp), %eax
  400915: 99                           	cltd
  400916: c1 ea 1f                     	shrl	$0x1f, %edx
  400919: 01 d0                        	addl	%edx, %eax
  40091b: 83 e0 01                     	andl	$0x1, %eax
  40091e: 29 d0                        	subl	%edx, %eax
  400920: 83 f8 01                     	cmpl	$0x1, %eax
  400923: 75 1e                        	jne	0x400943 <get_flag+0x178>
  400925: 8b 45 c8                     	movl	-0x38(%rbp), %eax
  400928: 48 98                        	cltq
  40092a: 0f b6 80 90 10 60 00         	movzbl	0x601090(%rax), %eax
  400931: 83 e8 02                     	subl	$0x2, %eax
  400934: 89 c2                        	movl	%eax, %edx
  400936: 8b 45 c8                     	movl	-0x38(%rbp), %eax
  400939: 48 98                        	cltq
  40093b: 88 90 90 10 60 00            	movb	%dl, 0x601090(%rax)
  400941: eb 1c                        	jmp	0x40095f <get_flag+0x194>
  400943: 8b 45 c8                     	movl	-0x38(%rbp), %eax
  400946: 48 98                        	cltq
  400948: 0f b6 80 90 10 60 00         	movzbl	0x601090(%rax), %eax
  40094f: 83 e8 01                     	subl	$0x1, %eax
  400952: 89 c2                        	movl	%eax, %edx
  400954: 8b 45 c8                     	movl	-0x38(%rbp), %eax
  400957: 48 98                        	cltq
  400959: 88 90 90 10 60 00            	movb	%dl, 0x601090(%rax)
  40095f: 83 45 c8 01                  	addl	$0x1, -0x38(%rbp)
  400963: 83 7d c8 07                  	cmpl	$0x7, -0x38(%rbp)
  400967: 7e a9                        	jle	0x400912 <get_flag+0x147>
  400969: eb 0a                        	jmp	0x400975 <get_flag+0x1aa>
  40096b: bf a0 0b 40 00               	movl	$0x400ba0, %edi         # imm = 0x400BA0
  400970: e8 8b fc ff ff               	callq	0x400600 <puts@plt>
  400975: 83 45 c4 01                  	addl	$0x1, -0x3c(%rbp)
  400979: 83 7d c4 04                  	cmpl	$0x4, -0x3c(%rbp)
  40097d: 0f 8e 7c fe ff ff            	jle	0x4007ff <get_flag+0x34>
  400983: 90                           	nop
  400984: 48 8b 45 f8                  	movq	-0x8(%rbp), %rax
  400988: 64 48 33 04 25 28 00 00 00   	xorq	%fs:0x28, %rax
  400991: 74 05                        	je	0x400998 <get_flag+0x1cd>
  400993: e8 78 fc ff ff               	callq	0x400610 <__stack_chk_fail@plt>
  400998: c9                           	leave
  400999: c3                           	retq
