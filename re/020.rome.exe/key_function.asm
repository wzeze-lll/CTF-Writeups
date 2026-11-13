<_func>:
  401340: 55                           	pushl	%ebp
  401341: 89 e5                        	movl	%esp, %ebp
  401343: 83 ec 58                     	subl	$0x58, %esp
  401346: c6 45 e3 51                  	movb	$0x51, -0x1d(%ebp)
  40134a: c6 45 e4 73                  	movb	$0x73, -0x1c(%ebp)
  40134e: c6 45 e5 77                  	movb	$0x77, -0x1b(%ebp)
  401352: c6 45 e6 33                  	movb	$0x33, -0x1a(%ebp)
  401356: c6 45 e7 73                  	movb	$0x73, -0x19(%ebp)
  40135a: c6 45 e8 6a                  	movb	$0x6a, -0x18(%ebp)
  40135e: c6 45 e9 5f                  	movb	$0x5f, -0x17(%ebp)
  401362: c6 45 ea 6c                  	movb	$0x6c, -0x16(%ebp)
  401366: c6 45 eb 7a                  	movb	$0x7a, -0x15(%ebp)
  40136a: c6 45 ec 34                  	movb	$0x34, -0x14(%ebp)
  40136e: c6 45 ed 5f                  	movb	$0x5f, -0x13(%ebp)
  401372: c6 45 ee 55                  	movb	$0x55, -0x12(%ebp)
  401376: c6 45 ef 6a                  	movb	$0x6a, -0x11(%ebp)
  40137a: c6 45 f0 77                  	movb	$0x77, -0x10(%ebp)
  40137e: c6 45 f1 40                  	movb	$0x40, -0xf(%ebp)
  401382: c6 45 f2 6c                  	movb	$0x6c, -0xe(%ebp)
  401386: c6 45 f3 00                  	movb	$0x0, -0xd(%ebp)
  40138a: c7 04 24 24 30 40 00         	movl	$0x403024, (%esp)       # imm = 0x403024
  401391: e8 ba 09 00 00               	calll	0x401d50 <_printf>
  401396: 8d 45 cc                     	leal	-0x34(%ebp), %eax
  401399: 89 44 24 04                  	movl	%eax, 0x4(%esp)
  40139d: c7 04 24 32 30 40 00         	movl	$0x403032, (%esp)       # imm = 0x403032
  4013a4: e8 af 09 00 00               	calll	0x401d58 <_scanf>
  4013a9: 0f b6 45 cc                  	movzbl	-0x34(%ebp), %eax
  4013ad: 3c 41                        	cmpb	$0x41, %al
  4013af: 75 20                        	jne	0x4013d1 <_func+0x91>
  4013b1: 0f b6 45 cd                  	movzbl	-0x33(%ebp), %eax
  4013b5: 3c 43                        	cmpb	$0x43, %al
  4013b7: 75 18                        	jne	0x4013d1 <_func+0x91>
  4013b9: 0f b6 45 ce                  	movzbl	-0x32(%ebp), %eax
  4013bd: 3c 54                        	cmpb	$0x54, %al
  4013bf: 75 10                        	jne	0x4013d1 <_func+0x91>
  4013c1: 0f b6 45 cf                  	movzbl	-0x31(%ebp), %eax
  4013c5: 3c 46                        	cmpb	$0x46, %al
  4013c7: 75 08                        	jne	0x4013d1 <_func+0x91>
  4013c9: 0f b6 45 d0                  	movzbl	-0x30(%ebp), %eax
  4013cd: 3c 7b                        	cmpb	$0x7b, %al
  4013cf: 74 05                        	je	0x4013d6 <_func+0x96>
  4013d1: e9 34 01 00 00               	jmp	0x40150a <_func+0x1ca>
  4013d6: 0f b6 45 e1                  	movzbl	-0x1f(%ebp), %eax
  4013da: 3c 7d                        	cmpb	$0x7d, %al
  4013dc: 74 05                        	je	0x4013e3 <_func+0xa3>
  4013de: e9 27 01 00 00               	jmp	0x40150a <_func+0x1ca>
  4013e3: 8d 45 cc                     	leal	-0x34(%ebp), %eax
  4013e6: 83 c0 05                     	addl	$0x5, %eax
  4013e9: 8b 10                        	movl	(%eax), %edx
  4013eb: 89 55 bc                     	movl	%edx, -0x44(%ebp)
  4013ee: 8b 50 04                     	movl	0x4(%eax), %edx
  4013f1: 89 55 c0                     	movl	%edx, -0x40(%ebp)
  4013f4: 8b 50 08                     	movl	0x8(%eax), %edx
  4013f7: 89 55 c4                     	movl	%edx, -0x3c(%ebp)
  4013fa: 8b 40 0c                     	movl	0xc(%eax), %eax
  4013fd: 89 45 c8                     	movl	%eax, -0x38(%ebp)
  401400: c7 45 f4 00 00 00 00         	movl	$0x0, -0xc(%ebp)
  401407: e9 b8 00 00 00               	jmp	0x4014c4 <_func+0x184>
  40140c: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  40140f: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  401412: 01 d0                        	addl	%edx, %eax
  401414: 0f b6 00                     	movzbl	(%eax), %eax
  401417: 3c 40                        	cmpb	$0x40, %al
  401419: 7e 4b                        	jle	0x401466 <_func+0x126>
  40141b: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  40141e: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  401421: 01 d0                        	addl	%edx, %eax
  401423: 0f b6 00                     	movzbl	(%eax), %eax
  401426: 3c 5a                        	cmpb	$0x5a, %al
  401428: 7f 3c                        	jg	0x401466 <_func+0x126>
  40142a: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  40142d: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  401430: 01 d0                        	addl	%edx, %eax
  401432: 0f b6 00                     	movzbl	(%eax), %eax
  401435: 0f be c0                     	movsbl	%al, %eax
  401438: 8d 48 cd                     	leal	-0x33(%eax), %ecx
  40143b: ba 4f ec c4 4e               	movl	$0x4ec4ec4f, %edx       # imm = 0x4EC4EC4F
  401440: 89 c8                        	movl	%ecx, %eax
  401442: f7 ea                        	imull	%edx
  401444: c1 fa 03                     	sarl	$0x3, %edx
  401447: 89 c8                        	movl	%ecx, %eax
  401449: c1 f8 1f                     	sarl	$0x1f, %eax
  40144c: 29 c2                        	subl	%eax, %edx
  40144e: 89 d0                        	movl	%edx, %eax
  401450: 6b c0 1a                     	imull	$0x1a, %eax, %eax
  401453: 29 c1                        	subl	%eax, %ecx
  401455: 89 c8                        	movl	%ecx, %eax
  401457: 83 c0 41                     	addl	$0x41, %eax
  40145a: 89 c1                        	movl	%eax, %ecx
  40145c: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  40145f: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  401462: 01 d0                        	addl	%edx, %eax
  401464: 88 08                        	movb	%cl, (%eax)
  401466: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  401469: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  40146c: 01 d0                        	addl	%edx, %eax
  40146e: 0f b6 00                     	movzbl	(%eax), %eax
  401471: 3c 60                        	cmpb	$0x60, %al
  401473: 7e 4b                        	jle	0x4014c0 <_func+0x180>
  401475: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  401478: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  40147b: 01 d0                        	addl	%edx, %eax
  40147d: 0f b6 00                     	movzbl	(%eax), %eax
  401480: 3c 7a                        	cmpb	$0x7a, %al
  401482: 7f 3c                        	jg	0x4014c0 <_func+0x180>
  401484: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  401487: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  40148a: 01 d0                        	addl	%edx, %eax
  40148c: 0f b6 00                     	movzbl	(%eax), %eax
  40148f: 0f be c0                     	movsbl	%al, %eax
  401492: 8d 48 b1                     	leal	-0x4f(%eax), %ecx
  401495: ba 4f ec c4 4e               	movl	$0x4ec4ec4f, %edx       # imm = 0x4EC4EC4F
  40149a: 89 c8                        	movl	%ecx, %eax
  40149c: f7 ea                        	imull	%edx
  40149e: c1 fa 03                     	sarl	$0x3, %edx
  4014a1: 89 c8                        	movl	%ecx, %eax
  4014a3: c1 f8 1f                     	sarl	$0x1f, %eax
  4014a6: 29 c2                        	subl	%eax, %edx
  4014a8: 89 d0                        	movl	%edx, %eax
  4014aa: 6b c0 1a                     	imull	$0x1a, %eax, %eax
  4014ad: 29 c1                        	subl	%eax, %ecx
  4014af: 89 c8                        	movl	%ecx, %eax
  4014b1: 83 c0 61                     	addl	$0x61, %eax
  4014b4: 89 c1                        	movl	%eax, %ecx
  4014b6: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  4014b9: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  4014bc: 01 d0                        	addl	%edx, %eax
  4014be: 88 08                        	movb	%cl, (%eax)
  4014c0: 83 45 f4 01                  	addl	$0x1, -0xc(%ebp)
  4014c4: 83 7d f4 0f                  	cmpl	$0xf, -0xc(%ebp)
  4014c8: 0f 8e 3e ff ff ff            	jle	0x40140c <_func+0xcc>
  4014ce: c7 45 f4 00 00 00 00         	movl	$0x0, -0xc(%ebp)
  4014d5: eb 20                        	jmp	0x4014f7 <_func+0x1b7>
  4014d7: 8d 55 bc                     	leal	-0x44(%ebp), %edx
  4014da: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  4014dd: 01 d0                        	addl	%edx, %eax
  4014df: 0f b6 10                     	movzbl	(%eax), %edx
  4014e2: 8d 4d e3                     	leal	-0x1d(%ebp), %ecx
  4014e5: 8b 45 f4                     	movl	-0xc(%ebp), %eax
  4014e8: 01 c8                        	addl	%ecx, %eax
  4014ea: 0f b6 00                     	movzbl	(%eax), %eax
  4014ed: 38 c2                        	cmpb	%al, %dl
  4014ef: 74 02                        	je	0x4014f3 <_func+0x1b3>
  4014f1: eb 17                        	jmp	0x40150a <_func+0x1ca>
  4014f3: 83 45 f4 01                  	addl	$0x1, -0xc(%ebp)
  4014f7: 83 7d f4 0f                  	cmpl	$0xf, -0xc(%ebp)
  4014fb: 7e da                        	jle	0x4014d7 <_func+0x197>
  4014fd: c7 04 24 35 30 40 00         	movl	$0x403035, (%esp)       # imm = 0x403035
  401504: e8 47 08 00 00               	calll	0x401d50 <_printf>
  401509: 90                           	nop
  40150a: c9                           	leave
  40150b: c3                           	retl
