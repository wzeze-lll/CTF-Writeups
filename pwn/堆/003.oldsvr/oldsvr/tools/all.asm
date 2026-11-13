
server:     file format elf64-tradbigmips


Disassembly of section .init:

0000000000001418 <_init>:
    1418:	67bdffe0 	daddiu	sp,sp,-32
    141c:	ffbf0018 	sd	ra,24(sp)
    1420:	ffbc0010 	sd	gp,16(sp)
    1424:	3c010002 	lui	at,0x2
    1428:	24216c38 	addiu	at,at,27704
    142c:	0039e02d 	daddu	gp,at,t9
    1430:	04110001 	bal	1438 <_init+0x20>
    1434:	00000000 	nop
    1438:	03801025 	move	v0,gp
    143c:	3c1c0002 	lui	gp,0x2
    1440:	279c6c18 	addiu	gp,gp,27672
    1444:	039fe02d 	daddu	gp,gp,ra
    1448:	df998068 	ld	t9,-32664(gp)
    144c:	0320f809 	jalr	t9
    1450:	00000000 	nop
    1454:	04110001 	bal	145c <_init+0x44>
    1458:	00000000 	nop
    145c:	03801025 	move	v0,gp
    1460:	3c1c0002 	lui	gp,0x2
    1464:	279c6bf4 	addiu	gp,gp,27636
    1468:	039fe02d 	daddu	gp,gp,ra
    146c:	df9981b0 	ld	t9,-32336(gp)
    1470:	0320f809 	jalr	t9
    1474:	00000000 	nop
    1478:	dfbf0018 	ld	ra,24(sp)
    147c:	dfbc0010 	ld	gp,16(sp)
    1480:	03e00008 	jr	ra
    1484:	67bd0020 	daddiu	sp,sp,32

Disassembly of section .text:

0000000000001490 <main-0x240>:
    1490:	03e00025 	move	zero,ra
    1494:	04110001 	bal	149c <_init+0x84>
    1498:	00000000 	nop
    149c:	0380c825 	move	t9,gp
    14a0:	3c1c0002 	lui	gp,0x2
    14a4:	279c6bb4 	addiu	gp,gp,27572
    14a8:	039fe02d 	daddu	gp,gp,ra
    14ac:	0000f825 	move	ra,zero
    14b0:	df848020 	ld	a0,-32736(gp)
    14b4:	dfa50000 	ld	a1,0(sp)
    14b8:	67a60008 	daddiu	a2,sp,8
    14bc:	2401fff0 	li	at,-16
    14c0:	03a1e824 	and	sp,sp,at
    14c4:	df878028 	ld	a3,-32728(gp)
    14c8:	df888030 	ld	a4,-32720(gp)
    14cc:	00404825 	move	a5,v0
    14d0:	03a05025 	move	a6,sp
    14d4:	df998200 	ld	t9,-32256(gp)
    14d8:	0320f809 	jalr	t9
    14dc:	00000000 	nop
    14e0:	1000ffff 	b	14e0 <_init+0xc8>
    14e4:	00000000 	nop
	...
    14f0:	3c030002 	lui	v1,0x2
    14f4:	0079182d 	daddu	v1,v1,t9
    14f8:	64636b60 	daddiu	v1,v1,27488
    14fc:	dc648038 	ld	a0,-32712(v1)
    1500:	dc628040 	ld	v0,-32704(v1)
    1504:	64840058 	daddiu	a0,a0,88
    1508:	10440005 	beq	v0,a0,1520 <_init+0x108>
    150c:	dc798208 	ld	t9,-32248(v1)
    1510:	13200003 	beqz	t9,1520 <_init+0x108>
    1514:	00000000 	nop
    1518:	03200008 	jr	t9
    151c:	00000000 	nop
    1520:	03e00008 	jr	ra
    1524:	00000000 	nop
    1528:	3c030002 	lui	v1,0x2
    152c:	0079182d 	daddu	v1,v1,t9
    1530:	64636b28 	daddiu	v1,v1,27432
    1534:	dc648038 	ld	a0,-32712(v1)
    1538:	dc658040 	ld	a1,-32704(v1)
    153c:	64840058 	daddiu	a0,a0,88
    1540:	00a4282f 	dsubu	a1,a1,a0
    1544:	000510fb 	dsra	v0,a1,0x3
    1548:	00052ffe 	dsrl32	a1,a1,0x1f
    154c:	00a2282d 	daddu	a1,a1,v0
    1550:	0005287b 	dsra	a1,a1,0x1
    1554:	10a00005 	beqz	a1,156c <_init+0x154>
    1558:	dc798238 	ld	t9,-32200(v1)
    155c:	13200003 	beqz	t9,156c <_init+0x154>
    1560:	00000000 	nop
    1564:	03200008 	jr	t9
    1568:	00000000 	nop
    156c:	03e00008 	jr	ra
    1570:	00000000 	nop
    1574:	00000000 	nop
    1578:	67bdffd0 	daddiu	sp,sp,-48
    157c:	ffbc0020 	sd	gp,32(sp)
    1580:	3c1c0002 	lui	gp,0x2
    1584:	0399e02d 	daddu	gp,gp,t9
    1588:	679c6ad8 	daddiu	gp,gp,27352
    158c:	ffb30018 	sd	s3,24(sp)
    1590:	df938038 	ld	s3,-32712(gp)
    1594:	ffbf0028 	sd	ra,40(sp)
    1598:	926202f0 	lbu	v0,752(s3)
    159c:	ffb20010 	sd	s2,16(sp)
    15a0:	ffb10008 	sd	s1,8(sp)
    15a4:	1440002b 	bnez	v0,1654 <_init+0x23c>
    15a8:	ffb00000 	sd	s0,0(sp)
    15ac:	df828268 	ld	v0,-32152(gp)
    15b0:	10400004 	beqz	v0,15c4 <_init+0x1ac>
    15b4:	df828048 	ld	v0,-32696(gp)
    15b8:	df998268 	ld	t9,-32152(gp)
    15bc:	0320f809 	jalr	t9
    15c0:	dc440000 	ld	a0,0(v0)
    15c4:	df838038 	ld	v1,-32712(gp)
    15c8:	df918050 	ld	s1,-32688(gp)
    15cc:	6463fff0 	daddiu	v1,v1,-16
    15d0:	df908038 	ld	s0,-32712(gp)
    15d4:	0223882f 	dsubu	s1,s1,v1
    15d8:	de0202f8 	ld	v0,760(s0)
    15dc:	001188fb 	dsra	s1,s1,0x3
    15e0:	df848038 	ld	a0,-32712(gp)
    15e4:	6631ffff 	daddiu	s1,s1,-1
    15e8:	0051182b 	sltu	v1,v0,s1
    15ec:	6492fff0 	daddiu	s2,a0,-16
    15f0:	1060000d 	beqz	v1,1628 <_init+0x210>
    15f4:	df998058 	ld	t9,-32680(gp)
    15f8:	64420001 	daddiu	v0,v0,1
    15fc:	00000000 	nop
    1600:	000218f8 	dsll	v1,v0,0x3
    1604:	0243182d 	daddu	v1,s2,v1
    1608:	dc790000 	ld	t9,0(v1)
    160c:	0320f809 	jalr	t9
    1610:	fe0202f8 	sd	v0,760(s0)
    1614:	de0202f8 	ld	v0,760(s0)
    1618:	0051182b 	sltu	v1,v0,s1
    161c:	1460fff8 	bnez	v1,1600 <_init+0x1e8>
    1620:	64420001 	daddiu	v0,v0,1
    1624:	df998058 	ld	t9,-32680(gp)
    1628:	673914f0 	daddiu	t9,t9,5360
    162c:	0411ffb0 	bal	14f0 <_init+0xd8>
    1630:	00000000 	nop
    1634:	df828240 	ld	v0,-32192(gp)
    1638:	10400004 	beqz	v0,164c <_init+0x234>
    163c:	df998240 	ld	t9,-32192(gp)
    1640:	df848058 	ld	a0,-32680(gp)
    1644:	0320f809 	jalr	t9
    1648:	64846f50 	daddiu	a0,a0,28496
    164c:	24020001 	li	v0,1
    1650:	a26202f0 	sb	v0,752(s3)
    1654:	dfbf0028 	ld	ra,40(sp)
    1658:	dfbc0020 	ld	gp,32(sp)
    165c:	dfb30018 	ld	s3,24(sp)
    1660:	dfb20010 	ld	s2,16(sp)
    1664:	dfb10008 	ld	s1,8(sp)
    1668:	dfb00000 	ld	s0,0(sp)
    166c:	03e00008 	jr	ra
    1670:	67bd0030 	daddiu	sp,sp,48
    1674:	00000000 	nop
    1678:	67bdfff0 	daddiu	sp,sp,-16
    167c:	ffbc0000 	sd	gp,0(sp)
    1680:	3c1c0002 	lui	gp,0x2
    1684:	0399e02d 	daddu	gp,gp,t9
    1688:	679c69d8 	daddiu	gp,gp,27096
    168c:	df8281d8 	ld	v0,-32296(gp)
    1690:	10400007 	beqz	v0,16b0 <_init+0x298>
    1694:	ffbf0008 	sd	ra,8(sp)
    1698:	df858038 	ld	a1,-32712(gp)
    169c:	df848058 	ld	a0,-32680(gp)
    16a0:	df9981d8 	ld	t9,-32296(gp)
    16a4:	64a50300 	daddiu	a1,a1,768
    16a8:	0320f809 	jalr	t9
    16ac:	64846f50 	daddiu	a0,a0,28496
    16b0:	df998058 	ld	t9,-32680(gp)
    16b4:	dfbf0008 	ld	ra,8(sp)
    16b8:	dfbc0000 	ld	gp,0(sp)
    16bc:	67391528 	daddiu	t9,t9,5416
    16c0:	1000ff99 	b	1528 <_init+0x110>
    16c4:	67bd0010 	daddiu	sp,sp,16
	...

00000000000016d0 <main>:
    16d0:	67bdffe0 	daddiu	sp,sp,-32
    16d4:	ffbf0018 	sd	ra,24(sp)
    16d8:	ffbe0010 	sd	s8,16(sp)
    16dc:	ffbc0008 	sd	gp,8(sp)
    16e0:	03a0f025 	move	s8,sp
    16e4:	3c1c0002 	lui	gp,0x2
    16e8:	0399e02d 	daddu	gp,gp,t9
    16ec:	679c6980 	daddiu	gp,gp,27008
    16f0:	df828230 	ld	v0,-32208(gp)
    16f4:	dc420000 	ld	v0,0(v0)
    16f8:	00003825 	move	a3,zero
    16fc:	24060002 	li	a2,2
    1700:	00002825 	move	a1,zero
    1704:	00402025 	move	a0,v0
    1708:	df828278 	ld	v0,-32136(gp)
    170c:	0040c825 	move	t9,v0
    1710:	0320f809 	jalr	t9
    1714:	00000000 	nop
    1718:	df828290 	ld	v0,-32112(gp)
    171c:	dc420000 	ld	v0,0(v0)
    1720:	00003825 	move	a3,zero
    1724:	24060002 	li	a2,2
    1728:	00002825 	move	a1,zero
    172c:	00402025 	move	a0,v0
    1730:	df828278 	ld	v0,-32136(gp)
    1734:	0040c825 	move	t9,v0
    1738:	0320f809 	jalr	t9
    173c:	00000000 	nop
    1740:	df8281f0 	ld	v0,-32272(gp)
    1744:	dc420000 	ld	v0,0(v0)
    1748:	00003825 	move	a3,zero
    174c:	24060002 	li	a2,2
    1750:	00002825 	move	a1,zero
    1754:	00402025 	move	a0,v0
    1758:	df828278 	ld	v0,-32136(gp)
    175c:	0040c825 	move	t9,v0
    1760:	0320f809 	jalr	t9
    1764:	00000000 	nop
    1768:	24040050 	li	a0,80
    176c:	df828258 	ld	v0,-32168(gp)
    1770:	0040c825 	move	t9,v0
    1774:	0320f809 	jalr	t9
    1778:	00000000 	nop
    177c:	df828070 	ld	v0,-32656(gp)
    1780:	0040c825 	move	t9,v0
    1784:	04110c9d 	bal	49fc <main+0x332c>
    1788:	00000000 	nop
    178c:	00001025 	move	v0,zero
    1790:	03c0e825 	move	sp,s8
    1794:	dfbf0018 	ld	ra,24(sp)
    1798:	dfbe0010 	ld	s8,16(sp)
    179c:	dfbc0008 	ld	gp,8(sp)
    17a0:	67bd0020 	daddiu	sp,sp,32
    17a4:	03e00008 	jr	ra
    17a8:	00000000 	nop
    17ac:	00000000 	nop
    17b0:	67bdffd0 	daddiu	sp,sp,-48
    17b4:	ffbe0028 	sd	s8,40(sp)
    17b8:	03a0f025 	move	s8,sp
    17bc:	ffc40010 	sd	a0,16(s8)
    17c0:	24020001 	li	v0,1
    17c4:	a3c20000 	sb	v0,0(s8)
    17c8:	dfc20010 	ld	v0,16(s8)
    17cc:	64420001 	daddiu	v0,v0,1
    17d0:	90420000 	lbu	v0,0(v0)
    17d4:	0002163c 	dsll32	v0,v0,0x18
    17d8:	0002163f 	dsra32	v0,v0,0x18
    17dc:	04410018 	bgez	v0,1840 <main+0x170>
    17e0:	00000000 	nop
    17e4:	93c20000 	lbu	v0,0(s8)
    17e8:	24420001 	addiu	v0,v0,1
    17ec:	a3c20000 	sb	v0,0(s8)
    17f0:	dfc20010 	ld	v0,16(s8)
    17f4:	64420002 	daddiu	v0,v0,2
    17f8:	90420000 	lbu	v0,0(v0)
    17fc:	0002163c 	dsll32	v0,v0,0x18
    1800:	0002163f 	dsra32	v0,v0,0x18
    1804:	0441000e 	bgez	v0,1840 <main+0x170>
    1808:	00000000 	nop
    180c:	93c20000 	lbu	v0,0(s8)
    1810:	24420001 	addiu	v0,v0,1
    1814:	a3c20000 	sb	v0,0(s8)
    1818:	dfc20010 	ld	v0,16(s8)
    181c:	64420003 	daddiu	v0,v0,3
    1820:	90420000 	lbu	v0,0(v0)
    1824:	0002163c 	dsll32	v0,v0,0x18
    1828:	0002163f 	dsra32	v0,v0,0x18
    182c:	04410004 	bgez	v0,1840 <main+0x170>
    1830:	00000000 	nop
    1834:	93c20000 	lbu	v0,0(s8)
    1838:	24420001 	addiu	v0,v0,1
    183c:	a3c20000 	sb	v0,0(s8)
    1840:	93c20000 	lbu	v0,0(s8)
    1844:	03c0e825 	move	sp,s8
    1848:	dfbe0028 	ld	s8,40(sp)
    184c:	67bd0030 	daddiu	sp,sp,48
    1850:	03e00008 	jr	ra
    1854:	00000000 	nop
    1858:	67bdffd0 	daddiu	sp,sp,-48
    185c:	ffbe0028 	sd	s8,40(sp)
    1860:	03a0f025 	move	s8,sp
    1864:	ffc40010 	sd	a0,16(s8)
    1868:	24020001 	li	v0,1
    186c:	a7c20000 	sh	v0,0(s8)
    1870:	a7c00002 	sh	zero,2(s8)
    1874:	dfc20010 	ld	v0,16(s8)
    1878:	64420001 	daddiu	v0,v0,1
    187c:	ffc20010 	sd	v0,16(s8)
    1880:	dfc20010 	ld	v0,16(s8)
    1884:	90420000 	lbu	v0,0(v0)
    1888:	a3c20004 	sb	v0,4(s8)
    188c:	93c20004 	lbu	v0,4(s8)
    1890:	3042ffff 	andi	v0,v0,0xffff
    1894:	3042007f 	andi	v0,v0,0x7f
    1898:	3042ffff 	andi	v0,v0,0xffff
    189c:	97c30000 	lhu	v1,0(s8)
    18a0:	70621002 	mul	v0,v1,v0
    18a4:	3042ffff 	andi	v0,v0,0xffff
    18a8:	97c30002 	lhu	v1,2(s8)
    18ac:	00621021 	addu	v0,v1,v0
    18b0:	a7c20002 	sh	v0,2(s8)
    18b4:	97c20000 	lhu	v0,0(s8)
    18b8:	000211c0 	sll	v0,v0,0x7
    18bc:	a7c20000 	sh	v0,0(s8)
    18c0:	dfc20010 	ld	v0,16(s8)
    18c4:	64420001 	daddiu	v0,v0,1
    18c8:	ffc20010 	sd	v0,16(s8)
    18cc:	83c20004 	lb	v0,4(s8)
    18d0:	0440ffeb 	bltz	v0,1880 <main+0x1b0>
    18d4:	00000000 	nop
    18d8:	97c20002 	lhu	v0,2(s8)
    18dc:	03c0e825 	move	sp,s8
    18e0:	dfbe0028 	ld	s8,40(sp)
    18e4:	67bd0030 	daddiu	sp,sp,48
    18e8:	03e00008 	jr	ra
    18ec:	00000000 	nop
    18f0:	67bdffc0 	daddiu	sp,sp,-64
    18f4:	ffbf0038 	sd	ra,56(sp)
    18f8:	ffbe0030 	sd	s8,48(sp)
    18fc:	ffbc0028 	sd	gp,40(sp)
    1900:	03a0f025 	move	s8,sp
    1904:	3c1c0002 	lui	gp,0x2
    1908:	0399e02d 	daddu	gp,gp,t9
    190c:	679c6760 	daddiu	gp,gp,26464
    1910:	ffc40010 	sd	a0,16(s8)
    1914:	dfc20010 	ld	v0,16(s8)
    1918:	90420000 	lbu	v0,0(v0)
    191c:	304200f0 	andi	v0,v0,0xf0
    1920:	00401825 	move	v1,v0
    1924:	24020010 	li	v0,16
    1928:	14620054 	bne	v1,v0,1a7c <main+0x3ac>
    192c:	00000000 	nop
    1930:	dfc40010 	ld	a0,16(s8)
    1934:	df828078 	ld	v0,-32648(gp)
    1938:	0040c825 	move	t9,v0
    193c:	0411ff9c 	bal	17b0 <main+0xe0>
    1940:	00000000 	nop
    1944:	a3c20000 	sb	v0,0(s8)
    1948:	93c20000 	lbu	v0,0(s8)
    194c:	64420001 	daddiu	v0,v0,1
    1950:	dfc30010 	ld	v1,16(s8)
    1954:	0062102d 	daddu	v0,v1,v0
    1958:	90420000 	lbu	v0,0(v0)
    195c:	00021200 	sll	v0,v0,0x8
    1960:	a7c20002 	sh	v0,2(s8)
    1964:	93c20000 	lbu	v0,0(s8)
    1968:	64420002 	daddiu	v0,v0,2
    196c:	dfc30010 	ld	v1,16(s8)
    1970:	0062102d 	daddu	v0,v1,v0
    1974:	90420000 	lbu	v0,0(v0)
    1978:	00401825 	move	v1,v0
    197c:	97c20002 	lhu	v0,2(s8)
    1980:	00431025 	or	v0,v0,v1
    1984:	a7c20002 	sh	v0,2(s8)
    1988:	97c30002 	lhu	v1,2(s8)
    198c:	24020004 	li	v0,4
    1990:	1462003a 	bne	v1,v0,1a7c <main+0x3ac>
    1994:	00000000 	nop
    1998:	93c20000 	lbu	v0,0(s8)
    199c:	64420003 	daddiu	v0,v0,3
    19a0:	dfc30010 	ld	v1,16(s8)
    19a4:	0062182d 	daddu	v1,v1,v0
    19a8:	24060004 	li	a2,4
    19ac:	df828058 	ld	v0,-32680(gp)
    19b0:	64456e40 	daddiu	a1,v0,28224
    19b4:	00602025 	move	a0,v1
    19b8:	df828218 	ld	v0,-32232(gp)
    19bc:	0040c825 	move	t9,v0
    19c0:	0320f809 	jalr	t9
    19c4:	00000000 	nop
    19c8:	1440002c 	bnez	v0,1a7c <main+0x3ac>
    19cc:	00000000 	nop
    19d0:	93c20000 	lbu	v0,0(s8)
    19d4:	64420007 	daddiu	v0,v0,7
    19d8:	dfc30010 	ld	v1,16(s8)
    19dc:	0062102d 	daddu	v0,v1,v0
    19e0:	90420000 	lbu	v0,0(v0)
    19e4:	a3c20004 	sb	v0,4(s8)
    19e8:	93c30004 	lbu	v1,4(s8)
    19ec:	24020004 	li	v0,4
    19f0:	14620022 	bne	v1,v0,1a7c <main+0x3ac>
    19f4:	00000000 	nop
    19f8:	93c20000 	lbu	v0,0(s8)
    19fc:	64420008 	daddiu	v0,v0,8
    1a00:	dfc30010 	ld	v1,16(s8)
    1a04:	0062102d 	daddu	v0,v1,v0
    1a08:	90420000 	lbu	v0,0(v0)
    1a0c:	a3c20005 	sb	v0,5(s8)
    1a10:	93c30005 	lbu	v1,5(s8)
    1a14:	240200c2 	li	v0,194
    1a18:	14620018 	bne	v1,v0,1a7c <main+0x3ac>
    1a1c:	00000000 	nop
    1a20:	93c20000 	lbu	v0,0(s8)
    1a24:	64420009 	daddiu	v0,v0,9
    1a28:	dfc30010 	ld	v1,16(s8)
    1a2c:	0062102d 	daddu	v0,v1,v0
    1a30:	90420000 	lbu	v0,0(v0)
    1a34:	00021200 	sll	v0,v0,0x8
    1a38:	a7c20006 	sh	v0,6(s8)
    1a3c:	93c20000 	lbu	v0,0(s8)
    1a40:	6442000a 	daddiu	v0,v0,10
    1a44:	dfc30010 	ld	v1,16(s8)
    1a48:	0062102d 	daddu	v0,v1,v0
    1a4c:	90420000 	lbu	v0,0(v0)
    1a50:	00401825 	move	v1,v0
    1a54:	97c20006 	lhu	v0,6(s8)
    1a58:	00431025 	or	v0,v0,v1
    1a5c:	a7c20006 	sh	v0,6(s8)
    1a60:	97c30006 	lhu	v1,6(s8)
    1a64:	24024321 	li	v0,17185
    1a68:	14620004 	bne	v1,v0,1a7c <main+0x3ac>
    1a6c:	00000000 	nop
    1a70:	24020001 	li	v0,1
    1a74:	10000002 	b	1a80 <main+0x3b0>
    1a78:	00000000 	nop
    1a7c:	00001025 	move	v0,zero
    1a80:	03c0e825 	move	sp,s8
    1a84:	dfbf0038 	ld	ra,56(sp)
    1a88:	dfbe0030 	ld	s8,48(sp)
    1a8c:	dfbc0028 	ld	gp,40(sp)
    1a90:	67bd0040 	daddiu	sp,sp,64
    1a94:	03e00008 	jr	ra
    1a98:	00000000 	nop
    1a9c:	67bdffc0 	daddiu	sp,sp,-64
    1aa0:	ffbf0038 	sd	ra,56(sp)
    1aa4:	ffbe0030 	sd	s8,48(sp)
    1aa8:	ffbc0028 	sd	gp,40(sp)
    1aac:	03a0f025 	move	s8,sp
    1ab0:	3c1c0002 	lui	gp,0x2
    1ab4:	0399e02d 	daddu	gp,gp,t9
    1ab8:	679c65b4 	daddiu	gp,gp,26036
    1abc:	ffc40010 	sd	a0,16(s8)
    1ac0:	ffc50018 	sd	a1,24(s8)
    1ac4:	a7c00000 	sh	zero,0(s8)
    1ac8:	dfc20010 	ld	v0,16(s8)
    1acc:	90420000 	lbu	v0,0(v0)
    1ad0:	304200f0 	andi	v0,v0,0xf0
    1ad4:	00401825 	move	v1,v0
    1ad8:	24020010 	li	v0,16
    1adc:	14620023 	bne	v1,v0,1b6c <main+0x49c>
    1ae0:	00000000 	nop
    1ae4:	dfc40010 	ld	a0,16(s8)
    1ae8:	df828078 	ld	v0,-32648(gp)
    1aec:	0040c825 	move	t9,v0
    1af0:	0411ff2f 	bal	17b0 <main+0xe0>
    1af4:	00000000 	nop
    1af8:	a3c20002 	sb	v0,2(s8)
    1afc:	93c20002 	lbu	v0,2(s8)
    1b00:	2442000a 	addiu	v0,v0,10
    1b04:	a3c20002 	sb	v0,2(s8)
    1b08:	93c20002 	lbu	v0,2(s8)
    1b0c:	64420001 	daddiu	v0,v0,1
    1b10:	dfc30010 	ld	v1,16(s8)
    1b14:	0062102d 	daddu	v0,v1,v0
    1b18:	90420000 	lbu	v0,0(v0)
    1b1c:	00021200 	sll	v0,v0,0x8
    1b20:	a7c20000 	sh	v0,0(s8)
    1b24:	93c20002 	lbu	v0,2(s8)
    1b28:	64420002 	daddiu	v0,v0,2
    1b2c:	dfc30010 	ld	v1,16(s8)
    1b30:	0062102d 	daddu	v0,v1,v0
    1b34:	90420000 	lbu	v0,0(v0)
    1b38:	00401825 	move	v1,v0
    1b3c:	97c20000 	lhu	v0,0(s8)
    1b40:	00431025 	or	v0,v0,v1
    1b44:	a7c20000 	sh	v0,0(s8)
    1b48:	93c20002 	lbu	v0,2(s8)
    1b4c:	24420001 	addiu	v0,v0,1
    1b50:	64420002 	daddiu	v0,v0,2
    1b54:	dfc30010 	ld	v1,16(s8)
    1b58:	0062182d 	daddu	v1,v1,v0
    1b5c:	dfc20018 	ld	v0,24(s8)
    1b60:	fc430000 	sd	v1,0(v0)
    1b64:	10000003 	b	1b74 <main+0x4a4>
    1b68:	00000000 	nop
    1b6c:	dfc20018 	ld	v0,24(s8)
    1b70:	fc400000 	sd	zero,0(v0)
    1b74:	97c20000 	lhu	v0,0(s8)
    1b78:	03c0e825 	move	sp,s8
    1b7c:	dfbf0038 	ld	ra,56(sp)
    1b80:	dfbe0030 	ld	s8,48(sp)
    1b84:	dfbc0028 	ld	gp,40(sp)
    1b88:	67bd0040 	daddiu	sp,sp,64
    1b8c:	03e00008 	jr	ra
    1b90:	00000000 	nop
    1b94:	67bdffc0 	daddiu	sp,sp,-64
    1b98:	ffbf0038 	sd	ra,56(sp)
    1b9c:	ffbe0030 	sd	s8,48(sp)
    1ba0:	ffbc0028 	sd	gp,40(sp)
    1ba4:	03a0f025 	move	s8,sp
    1ba8:	3c1c0002 	lui	gp,0x2
    1bac:	0399e02d 	daddu	gp,gp,t9
    1bb0:	679c64bc 	daddiu	gp,gp,25788
    1bb4:	ffc40010 	sd	a0,16(s8)
    1bb8:	ffc50018 	sd	a1,24(s8)
    1bbc:	a7c00000 	sh	zero,0(s8)
    1bc0:	dfc20010 	ld	v0,16(s8)
    1bc4:	90420000 	lbu	v0,0(v0)
    1bc8:	304200f0 	andi	v0,v0,0xf0
    1bcc:	00401825 	move	v1,v0
    1bd0:	24020010 	li	v0,16
    1bd4:	1462003a 	bne	v1,v0,1cc0 <main+0x5f0>
    1bd8:	00000000 	nop
    1bdc:	dfc40010 	ld	a0,16(s8)
    1be0:	df828078 	ld	v0,-32648(gp)
    1be4:	0040c825 	move	t9,v0
    1be8:	0411fef1 	bal	17b0 <main+0xe0>
    1bec:	00000000 	nop
    1bf0:	a3c20002 	sb	v0,2(s8)
    1bf4:	93c20002 	lbu	v0,2(s8)
    1bf8:	2442000a 	addiu	v0,v0,10
    1bfc:	a3c20002 	sb	v0,2(s8)
    1c00:	93c20002 	lbu	v0,2(s8)
    1c04:	64420001 	daddiu	v0,v0,1
    1c08:	dfc30010 	ld	v1,16(s8)
    1c0c:	0062102d 	daddu	v0,v1,v0
    1c10:	90420000 	lbu	v0,0(v0)
    1c14:	00021200 	sll	v0,v0,0x8
    1c18:	a7c20000 	sh	v0,0(s8)
    1c1c:	93c20002 	lbu	v0,2(s8)
    1c20:	64420002 	daddiu	v0,v0,2
    1c24:	dfc30010 	ld	v1,16(s8)
    1c28:	0062102d 	daddu	v0,v1,v0
    1c2c:	90420000 	lbu	v0,0(v0)
    1c30:	00401825 	move	v1,v0
    1c34:	97c20000 	lhu	v0,0(s8)
    1c38:	00431025 	or	v0,v0,v1
    1c3c:	a7c20000 	sh	v0,0(s8)
    1c40:	97c20000 	lhu	v0,0(s8)
    1c44:	304200ff 	andi	v0,v0,0xff
    1c48:	93c30002 	lbu	v1,2(s8)
    1c4c:	00621021 	addu	v0,v1,v0
    1c50:	304200ff 	andi	v0,v0,0xff
    1c54:	24420002 	addiu	v0,v0,2
    1c58:	a3c20002 	sb	v0,2(s8)
    1c5c:	93c20002 	lbu	v0,2(s8)
    1c60:	64420001 	daddiu	v0,v0,1
    1c64:	dfc30010 	ld	v1,16(s8)
    1c68:	0062102d 	daddu	v0,v1,v0
    1c6c:	90420000 	lbu	v0,0(v0)
    1c70:	00021200 	sll	v0,v0,0x8
    1c74:	a7c20000 	sh	v0,0(s8)
    1c78:	93c20002 	lbu	v0,2(s8)
    1c7c:	64420002 	daddiu	v0,v0,2
    1c80:	dfc30010 	ld	v1,16(s8)
    1c84:	0062102d 	daddu	v0,v1,v0
    1c88:	90420000 	lbu	v0,0(v0)
    1c8c:	00401825 	move	v1,v0
    1c90:	97c20000 	lhu	v0,0(s8)
    1c94:	00431025 	or	v0,v0,v1
    1c98:	a7c20000 	sh	v0,0(s8)
    1c9c:	93c20002 	lbu	v0,2(s8)
    1ca0:	24420001 	addiu	v0,v0,1
    1ca4:	64420002 	daddiu	v0,v0,2
    1ca8:	dfc30010 	ld	v1,16(s8)
    1cac:	0062182d 	daddu	v1,v1,v0
    1cb0:	dfc20018 	ld	v0,24(s8)
    1cb4:	fc430000 	sd	v1,0(v0)
    1cb8:	10000003 	b	1cc8 <main+0x5f8>
    1cbc:	00000000 	nop
    1cc0:	dfc20018 	ld	v0,24(s8)
    1cc4:	fc400000 	sd	zero,0(v0)
    1cc8:	97c20000 	lhu	v0,0(s8)
    1ccc:	03c0e825 	move	sp,s8
    1cd0:	dfbf0038 	ld	ra,56(sp)
    1cd4:	dfbe0030 	ld	s8,48(sp)
    1cd8:	dfbc0028 	ld	gp,40(sp)
    1cdc:	67bd0040 	daddiu	sp,sp,64
    1ce0:	03e00008 	jr	ra
    1ce4:	00000000 	nop
    1ce8:	67bdffc0 	daddiu	sp,sp,-64
    1cec:	ffbf0038 	sd	ra,56(sp)
    1cf0:	ffbe0030 	sd	s8,48(sp)
    1cf4:	ffbc0028 	sd	gp,40(sp)
    1cf8:	03a0f025 	move	s8,sp
    1cfc:	3c1c0002 	lui	gp,0x2
    1d00:	0399e02d 	daddu	gp,gp,t9
    1d04:	679c6368 	daddiu	gp,gp,25448
    1d08:	ffc40010 	sd	a0,16(s8)
    1d0c:	ffc50018 	sd	a1,24(s8)
    1d10:	a7c00000 	sh	zero,0(s8)
    1d14:	dfc20010 	ld	v0,16(s8)
    1d18:	90420000 	lbu	v0,0(v0)
    1d1c:	304200f0 	andi	v0,v0,0xf0
    1d20:	00401825 	move	v1,v0
    1d24:	24020010 	li	v0,16
    1d28:	14620051 	bne	v1,v0,1e70 <main+0x7a0>
    1d2c:	00000000 	nop
    1d30:	dfc40010 	ld	a0,16(s8)
    1d34:	df828078 	ld	v0,-32648(gp)
    1d38:	0040c825 	move	t9,v0
    1d3c:	0411fe9c 	bal	17b0 <main+0xe0>
    1d40:	00000000 	nop
    1d44:	a3c20002 	sb	v0,2(s8)
    1d48:	93c20002 	lbu	v0,2(s8)
    1d4c:	2442000a 	addiu	v0,v0,10
    1d50:	a3c20002 	sb	v0,2(s8)
    1d54:	93c20002 	lbu	v0,2(s8)
    1d58:	64420001 	daddiu	v0,v0,1
    1d5c:	dfc30010 	ld	v1,16(s8)
    1d60:	0062102d 	daddu	v0,v1,v0
    1d64:	90420000 	lbu	v0,0(v0)
    1d68:	00021200 	sll	v0,v0,0x8
    1d6c:	a7c20000 	sh	v0,0(s8)
    1d70:	93c20002 	lbu	v0,2(s8)
    1d74:	64420002 	daddiu	v0,v0,2
    1d78:	dfc30010 	ld	v1,16(s8)
    1d7c:	0062102d 	daddu	v0,v1,v0
    1d80:	90420000 	lbu	v0,0(v0)
    1d84:	00401825 	move	v1,v0
    1d88:	97c20000 	lhu	v0,0(s8)
    1d8c:	00431025 	or	v0,v0,v1
    1d90:	a7c20000 	sh	v0,0(s8)
    1d94:	97c20000 	lhu	v0,0(s8)
    1d98:	304200ff 	andi	v0,v0,0xff
    1d9c:	93c30002 	lbu	v1,2(s8)
    1da0:	00621021 	addu	v0,v1,v0
    1da4:	304200ff 	andi	v0,v0,0xff
    1da8:	24420002 	addiu	v0,v0,2
    1dac:	a3c20002 	sb	v0,2(s8)
    1db0:	93c20002 	lbu	v0,2(s8)
    1db4:	64420001 	daddiu	v0,v0,1
    1db8:	dfc30010 	ld	v1,16(s8)
    1dbc:	0062102d 	daddu	v0,v1,v0
    1dc0:	90420000 	lbu	v0,0(v0)
    1dc4:	00021200 	sll	v0,v0,0x8
    1dc8:	a7c20000 	sh	v0,0(s8)
    1dcc:	93c20002 	lbu	v0,2(s8)
    1dd0:	64420002 	daddiu	v0,v0,2
    1dd4:	dfc30010 	ld	v1,16(s8)
    1dd8:	0062102d 	daddu	v0,v1,v0
    1ddc:	90420000 	lbu	v0,0(v0)
    1de0:	00401825 	move	v1,v0
    1de4:	97c20000 	lhu	v0,0(s8)
    1de8:	00431025 	or	v0,v0,v1
    1dec:	a7c20000 	sh	v0,0(s8)
    1df0:	97c20000 	lhu	v0,0(s8)
    1df4:	304200ff 	andi	v0,v0,0xff
    1df8:	93c30002 	lbu	v1,2(s8)
    1dfc:	00621021 	addu	v0,v1,v0
    1e00:	304200ff 	andi	v0,v0,0xff
    1e04:	24420002 	addiu	v0,v0,2
    1e08:	a3c20002 	sb	v0,2(s8)
    1e0c:	93c20002 	lbu	v0,2(s8)
    1e10:	64420001 	daddiu	v0,v0,1
    1e14:	dfc30010 	ld	v1,16(s8)
    1e18:	0062102d 	daddu	v0,v1,v0
    1e1c:	90420000 	lbu	v0,0(v0)
    1e20:	00021200 	sll	v0,v0,0x8
    1e24:	a7c20000 	sh	v0,0(s8)
    1e28:	93c20002 	lbu	v0,2(s8)
    1e2c:	64420002 	daddiu	v0,v0,2
    1e30:	dfc30010 	ld	v1,16(s8)
    1e34:	0062102d 	daddu	v0,v1,v0
    1e38:	90420000 	lbu	v0,0(v0)
    1e3c:	00401825 	move	v1,v0
    1e40:	97c20000 	lhu	v0,0(s8)
    1e44:	00431025 	or	v0,v0,v1
    1e48:	a7c20000 	sh	v0,0(s8)
    1e4c:	93c20002 	lbu	v0,2(s8)
    1e50:	24420001 	addiu	v0,v0,1
    1e54:	64420002 	daddiu	v0,v0,2
    1e58:	dfc30010 	ld	v1,16(s8)
    1e5c:	0062182d 	daddu	v1,v1,v0
    1e60:	dfc20018 	ld	v0,24(s8)
    1e64:	fc430000 	sd	v1,0(v0)
    1e68:	10000003 	b	1e78 <main+0x7a8>
    1e6c:	00000000 	nop
    1e70:	dfc20018 	ld	v0,24(s8)
    1e74:	fc400000 	sd	zero,0(v0)
    1e78:	97c20000 	lhu	v0,0(s8)
    1e7c:	03c0e825 	move	sp,s8
    1e80:	dfbf0038 	ld	ra,56(sp)
    1e84:	dfbe0030 	ld	s8,48(sp)
    1e88:	dfbc0028 	ld	gp,40(sp)
    1e8c:	67bd0040 	daddiu	sp,sp,64
    1e90:	03e00008 	jr	ra
    1e94:	00000000 	nop
    1e98:	67bdffc0 	daddiu	sp,sp,-64
    1e9c:	ffbf0038 	sd	ra,56(sp)
    1ea0:	ffbe0030 	sd	s8,48(sp)
    1ea4:	ffbc0028 	sd	gp,40(sp)
    1ea8:	03a0f025 	move	s8,sp
    1eac:	3c1c0002 	lui	gp,0x2
    1eb0:	0399e02d 	daddu	gp,gp,t9
    1eb4:	679c61b8 	daddiu	gp,gp,25016
    1eb8:	ffc40010 	sd	a0,16(s8)
    1ebc:	dfc20010 	ld	v0,16(s8)
    1ec0:	90430000 	lbu	v1,0(v0)
    1ec4:	2402fff0 	li	v0,-16
    1ec8:	00621024 	and	v0,v1,v0
    1ecc:	a3c20002 	sb	v0,2(s8)
    1ed0:	dfc20010 	ld	v0,16(s8)
    1ed4:	90420000 	lbu	v0,0(v0)
    1ed8:	00021043 	sra	v0,v0,0x1
    1edc:	304200ff 	andi	v0,v0,0xff
    1ee0:	30420003 	andi	v0,v0,0x3
    1ee4:	a3c20003 	sb	v0,3(s8)
    1ee8:	a7c00000 	sh	zero,0(s8)
    1eec:	93c20002 	lbu	v0,2(s8)
    1ef0:	2c420030 	sltiu	v0,v0,48
    1ef4:	14400048 	bnez	v0,2018 <main+0x948>
    1ef8:	00000000 	nop
    1efc:	93c20002 	lbu	v0,2(s8)
    1f00:	2c4200b1 	sltiu	v0,v0,177
    1f04:	10400044 	beqz	v0,2018 <main+0x948>
    1f08:	00000000 	nop
    1f0c:	93c30002 	lbu	v1,2(s8)
    1f10:	24020030 	li	v0,48
    1f14:	1462002a 	bne	v1,v0,1fc0 <main+0x8f0>
    1f18:	00000000 	nop
    1f1c:	93c20003 	lbu	v0,3(s8)
    1f20:	1040003d 	beqz	v0,2018 <main+0x948>
    1f24:	00000000 	nop
    1f28:	dfc40010 	ld	a0,16(s8)
    1f2c:	df828078 	ld	v0,-32648(gp)
    1f30:	0040c825 	move	t9,v0
    1f34:	0411fe1e 	bal	17b0 <main+0xe0>
    1f38:	00000000 	nop
    1f3c:	a3c20005 	sb	v0,5(s8)
    1f40:	a3c00006 	sb	zero,6(s8)
    1f44:	93c20005 	lbu	v0,5(s8)
    1f48:	64420002 	daddiu	v0,v0,2
    1f4c:	dfc30010 	ld	v1,16(s8)
    1f50:	0062102d 	daddu	v0,v1,v0
    1f54:	90420000 	lbu	v0,0(v0)
    1f58:	93c30006 	lbu	v1,6(s8)
    1f5c:	00621025 	or	v0,v1,v0
    1f60:	a3c20006 	sb	v0,6(s8)
    1f64:	93c30005 	lbu	v1,5(s8)
    1f68:	93c20006 	lbu	v0,6(s8)
    1f6c:	00621021 	addu	v0,v1,v0
    1f70:	304200ff 	andi	v0,v0,0xff
    1f74:	24420003 	addiu	v0,v0,3
    1f78:	a3c20006 	sb	v0,6(s8)
    1f7c:	93c20006 	lbu	v0,6(s8)
    1f80:	dfc30010 	ld	v1,16(s8)
    1f84:	0062102d 	daddu	v0,v1,v0
    1f88:	90420000 	lbu	v0,0(v0)
    1f8c:	00021200 	sll	v0,v0,0x8
    1f90:	a7c20000 	sh	v0,0(s8)
    1f94:	93c20006 	lbu	v0,6(s8)
    1f98:	64420001 	daddiu	v0,v0,1
    1f9c:	dfc30010 	ld	v1,16(s8)
    1fa0:	0062102d 	daddu	v0,v1,v0
    1fa4:	90420000 	lbu	v0,0(v0)
    1fa8:	00401825 	move	v1,v0
    1fac:	97c20000 	lhu	v0,0(s8)
    1fb0:	00431025 	or	v0,v0,v1
    1fb4:	a7c20000 	sh	v0,0(s8)
    1fb8:	10000017 	b	2018 <main+0x948>
    1fbc:	00000000 	nop
    1fc0:	dfc40010 	ld	a0,16(s8)
    1fc4:	df828078 	ld	v0,-32648(gp)
    1fc8:	0040c825 	move	t9,v0
    1fcc:	0411fdf8 	bal	17b0 <main+0xe0>
    1fd0:	00000000 	nop
    1fd4:	a3c20004 	sb	v0,4(s8)
    1fd8:	93c20004 	lbu	v0,4(s8)
    1fdc:	64420001 	daddiu	v0,v0,1
    1fe0:	dfc30010 	ld	v1,16(s8)
    1fe4:	0062102d 	daddu	v0,v1,v0
    1fe8:	90420000 	lbu	v0,0(v0)
    1fec:	00021200 	sll	v0,v0,0x8
    1ff0:	a7c20000 	sh	v0,0(s8)
    1ff4:	93c20004 	lbu	v0,4(s8)
    1ff8:	64420002 	daddiu	v0,v0,2
    1ffc:	dfc30010 	ld	v1,16(s8)
    2000:	0062102d 	daddu	v0,v1,v0
    2004:	90420000 	lbu	v0,0(v0)
    2008:	00401825 	move	v1,v0
    200c:	97c20000 	lhu	v0,0(s8)
    2010:	00431025 	or	v0,v0,v1
    2014:	a7c20000 	sh	v0,0(s8)
    2018:	97c20000 	lhu	v0,0(s8)
    201c:	03c0e825 	move	sp,s8
    2020:	dfbf0038 	ld	ra,56(sp)
    2024:	dfbe0030 	ld	s8,48(sp)
    2028:	dfbc0028 	ld	gp,40(sp)
    202c:	67bd0040 	daddiu	sp,sp,64
    2030:	03e00008 	jr	ra
    2034:	00000000 	nop
    2038:	67bdffc0 	daddiu	sp,sp,-64
    203c:	ffbf0038 	sd	ra,56(sp)
    2040:	ffbe0030 	sd	s8,48(sp)
    2044:	ffbc0028 	sd	gp,40(sp)
    2048:	03a0f025 	move	s8,sp
    204c:	3c1c0002 	lui	gp,0x2
    2050:	0399e02d 	daddu	gp,gp,t9
    2054:	679c6018 	daddiu	gp,gp,24600
    2058:	ffc40010 	sd	a0,16(s8)
    205c:	ffc50018 	sd	a1,24(s8)
    2060:	67c20008 	daddiu	v0,s8,8
    2064:	00402825 	move	a1,v0
    2068:	dfc40010 	ld	a0,16(s8)
    206c:	df828080 	ld	v0,-32640(gp)
    2070:	0040c825 	move	t9,v0
    2074:	04110019 	bal	20dc <main+0xa0c>
    2078:	00000000 	nop
    207c:	a7c20000 	sh	v0,0(s8)
    2080:	97c20000 	lhu	v0,0(s8)
    2084:	1040000d 	beqz	v0,20bc <main+0x9ec>
    2088:	00000000 	nop
    208c:	dfc20008 	ld	v0,8(s8)
    2090:	1040000a 	beqz	v0,20bc <main+0x9ec>
    2094:	00000000 	nop
    2098:	dfc20008 	ld	v0,8(s8)
    209c:	97c30000 	lhu	v1,0(s8)
    20a0:	00603025 	move	a2,v1
    20a4:	00402825 	move	a1,v0
    20a8:	dfc40018 	ld	a0,24(s8)
    20ac:	df828280 	ld	v0,-32128(gp)
    20b0:	0040c825 	move	t9,v0
    20b4:	0320f809 	jalr	t9
    20b8:	00000000 	nop
    20bc:	97c20000 	lhu	v0,0(s8)
    20c0:	03c0e825 	move	sp,s8
    20c4:	dfbf0038 	ld	ra,56(sp)
    20c8:	dfbe0030 	ld	s8,48(sp)
    20cc:	dfbc0028 	ld	gp,40(sp)
    20d0:	67bd0040 	daddiu	sp,sp,64
    20d4:	03e00008 	jr	ra
    20d8:	00000000 	nop
    20dc:	67bdffc0 	daddiu	sp,sp,-64
    20e0:	ffbf0038 	sd	ra,56(sp)
    20e4:	ffbe0030 	sd	s8,48(sp)
    20e8:	ffbc0028 	sd	gp,40(sp)
    20ec:	03a0f025 	move	s8,sp
    20f0:	3c1c0002 	lui	gp,0x2
    20f4:	0399e02d 	daddu	gp,gp,t9
    20f8:	679c5f74 	daddiu	gp,gp,24436
    20fc:	ffc40010 	sd	a0,16(s8)
    2100:	ffc50018 	sd	a1,24(s8)
    2104:	a7c00000 	sh	zero,0(s8)
    2108:	dfc20010 	ld	v0,16(s8)
    210c:	90420000 	lbu	v0,0(v0)
    2110:	304200f0 	andi	v0,v0,0xf0
    2114:	00401825 	move	v1,v0
    2118:	24020030 	li	v0,48
    211c:	14620020 	bne	v1,v0,21a0 <main+0xad0>
    2120:	00000000 	nop
    2124:	dfc40010 	ld	a0,16(s8)
    2128:	df828078 	ld	v0,-32648(gp)
    212c:	0040c825 	move	t9,v0
    2130:	0411fd9f 	bal	17b0 <main+0xe0>
    2134:	00000000 	nop
    2138:	a3c20002 	sb	v0,2(s8)
    213c:	93c20002 	lbu	v0,2(s8)
    2140:	64420001 	daddiu	v0,v0,1
    2144:	dfc30010 	ld	v1,16(s8)
    2148:	0062102d 	daddu	v0,v1,v0
    214c:	90420000 	lbu	v0,0(v0)
    2150:	00021200 	sll	v0,v0,0x8
    2154:	a7c20000 	sh	v0,0(s8)
    2158:	93c20002 	lbu	v0,2(s8)
    215c:	64420002 	daddiu	v0,v0,2
    2160:	dfc30010 	ld	v1,16(s8)
    2164:	0062102d 	daddu	v0,v1,v0
    2168:	90420000 	lbu	v0,0(v0)
    216c:	00401825 	move	v1,v0
    2170:	97c20000 	lhu	v0,0(s8)
    2174:	00431025 	or	v0,v0,v1
    2178:	a7c20000 	sh	v0,0(s8)
    217c:	93c20002 	lbu	v0,2(s8)
    2180:	24420001 	addiu	v0,v0,1
    2184:	64420002 	daddiu	v0,v0,2
    2188:	dfc30010 	ld	v1,16(s8)
    218c:	0062182d 	daddu	v1,v1,v0
    2190:	dfc20018 	ld	v0,24(s8)
    2194:	fc430000 	sd	v1,0(v0)
    2198:	10000003 	b	21a8 <main+0xad8>
    219c:	00000000 	nop
    21a0:	dfc20018 	ld	v0,24(s8)
    21a4:	fc400000 	sd	zero,0(v0)
    21a8:	97c20000 	lhu	v0,0(s8)
    21ac:	03c0e825 	move	sp,s8
    21b0:	dfbf0038 	ld	ra,56(sp)
    21b4:	dfbe0030 	ld	s8,48(sp)
    21b8:	dfbc0028 	ld	gp,40(sp)
    21bc:	67bd0040 	daddiu	sp,sp,64
    21c0:	03e00008 	jr	ra
    21c4:	00000000 	nop
    21c8:	67bdffc0 	daddiu	sp,sp,-64
    21cc:	ffbf0038 	sd	ra,56(sp)
    21d0:	ffbe0030 	sd	s8,48(sp)
    21d4:	ffbc0028 	sd	gp,40(sp)
    21d8:	03a0f025 	move	s8,sp
    21dc:	3c1c0002 	lui	gp,0x2
    21e0:	0399e02d 	daddu	gp,gp,t9
    21e4:	679c5e88 	daddiu	gp,gp,24200
    21e8:	ffc40010 	sd	a0,16(s8)
    21ec:	ffc50018 	sd	a1,24(s8)
    21f0:	67c20008 	daddiu	v0,s8,8
    21f4:	00402825 	move	a1,v0
    21f8:	dfc40010 	ld	a0,16(s8)
    21fc:	df828088 	ld	v0,-32632(gp)
    2200:	0040c825 	move	t9,v0
    2204:	04110019 	bal	226c <main+0xb9c>
    2208:	00000000 	nop
    220c:	a7c20000 	sh	v0,0(s8)
    2210:	97c20000 	lhu	v0,0(s8)
    2214:	1040000d 	beqz	v0,224c <main+0xb7c>
    2218:	00000000 	nop
    221c:	dfc20008 	ld	v0,8(s8)
    2220:	1040000a 	beqz	v0,224c <main+0xb7c>
    2224:	00000000 	nop
    2228:	dfc20008 	ld	v0,8(s8)
    222c:	97c30000 	lhu	v1,0(s8)
    2230:	00603025 	move	a2,v1
    2234:	00402825 	move	a1,v0
    2238:	dfc40018 	ld	a0,24(s8)
    223c:	df828280 	ld	v0,-32128(gp)
    2240:	0040c825 	move	t9,v0
    2244:	0320f809 	jalr	t9
    2248:	00000000 	nop
    224c:	97c20000 	lhu	v0,0(s8)
    2250:	03c0e825 	move	sp,s8
    2254:	dfbf0038 	ld	ra,56(sp)
    2258:	dfbe0030 	ld	s8,48(sp)
    225c:	dfbc0028 	ld	gp,40(sp)
    2260:	67bd0040 	daddiu	sp,sp,64
    2264:	03e00008 	jr	ra
    2268:	00000000 	nop
    226c:	67bdffc0 	daddiu	sp,sp,-64
    2270:	ffbf0038 	sd	ra,56(sp)
    2274:	ffbe0030 	sd	s8,48(sp)
    2278:	ffbc0028 	sd	gp,40(sp)
    227c:	03a0f025 	move	s8,sp
    2280:	3c1c0002 	lui	gp,0x2
    2284:	0399e02d 	daddu	gp,gp,t9
    2288:	679c5de4 	daddiu	gp,gp,24036
    228c:	ffc40010 	sd	a0,16(s8)
    2290:	ffc50018 	sd	a1,24(s8)
    2294:	a7c00000 	sh	zero,0(s8)
    2298:	dfc20010 	ld	v0,16(s8)
    229c:	90420000 	lbu	v0,0(v0)
    22a0:	304200f0 	andi	v0,v0,0xf0
    22a4:	00401825 	move	v1,v0
    22a8:	24020030 	li	v0,48
    22ac:	14620035 	bne	v1,v0,2384 <main+0xcb4>
    22b0:	00000000 	nop
    22b4:	dfc40010 	ld	a0,16(s8)
    22b8:	df828078 	ld	v0,-32648(gp)
    22bc:	0040c825 	move	t9,v0
    22c0:	0411fd3b 	bal	17b0 <main+0xe0>
    22c4:	00000000 	nop
    22c8:	a3c20003 	sb	v0,3(s8)
    22cc:	a3c00002 	sb	zero,2(s8)
    22d0:	93c20003 	lbu	v0,3(s8)
    22d4:	64420002 	daddiu	v0,v0,2
    22d8:	dfc30010 	ld	v1,16(s8)
    22dc:	0062102d 	daddu	v0,v1,v0
    22e0:	90420000 	lbu	v0,0(v0)
    22e4:	93c30002 	lbu	v1,2(s8)
    22e8:	00621025 	or	v0,v1,v0
    22ec:	a3c20002 	sb	v0,2(s8)
    22f0:	93c30003 	lbu	v1,3(s8)
    22f4:	93c20002 	lbu	v0,2(s8)
    22f8:	00621021 	addu	v0,v1,v0
    22fc:	304200ff 	andi	v0,v0,0xff
    2300:	24420003 	addiu	v0,v0,3
    2304:	a3c20002 	sb	v0,2(s8)
    2308:	dfc20010 	ld	v0,16(s8)
    230c:	90420000 	lbu	v0,0(v0)
    2310:	30420006 	andi	v0,v0,0x6
    2314:	10400004 	beqz	v0,2328 <main+0xc58>
    2318:	00000000 	nop
    231c:	93c20002 	lbu	v0,2(s8)
    2320:	24420002 	addiu	v0,v0,2
    2324:	a3c20002 	sb	v0,2(s8)
    2328:	93c20002 	lbu	v0,2(s8)
    232c:	dfc30010 	ld	v1,16(s8)
    2330:	0062182d 	daddu	v1,v1,v0
    2334:	dfc20018 	ld	v0,24(s8)
    2338:	fc430000 	sd	v1,0(v0)
    233c:	dfc40010 	ld	a0,16(s8)
    2340:	df828090 	ld	v0,-32624(gp)
    2344:	0040c825 	move	t9,v0
    2348:	0411fd43 	bal	1858 <main+0x188>
    234c:	00000000 	nop
    2350:	00402025 	move	a0,v0
    2354:	93c20003 	lbu	v0,3(s8)
    2358:	3043ffff 	andi	v1,v0,0xffff
    235c:	93c20002 	lbu	v0,2(s8)
    2360:	3042ffff 	andi	v0,v0,0xffff
    2364:	00621023 	subu	v0,v1,v0
    2368:	3042ffff 	andi	v0,v0,0xffff
    236c:	00821021 	addu	v0,a0,v0
    2370:	3042ffff 	andi	v0,v0,0xffff
    2374:	24420001 	addiu	v0,v0,1
    2378:	a7c20000 	sh	v0,0(s8)
    237c:	10000003 	b	238c <main+0xcbc>
    2380:	00000000 	nop
    2384:	dfc20018 	ld	v0,24(s8)
    2388:	fc400000 	sd	zero,0(v0)
    238c:	97c20000 	lhu	v0,0(s8)
    2390:	03c0e825 	move	sp,s8
    2394:	dfbf0038 	ld	ra,56(sp)
    2398:	dfbe0030 	ld	s8,48(sp)
    239c:	dfbc0028 	ld	gp,40(sp)
    23a0:	67bd0040 	daddiu	sp,sp,64
    23a4:	03e00008 	jr	ra
    23a8:	00000000 	nop
    23ac:	67bdffc0 	daddiu	sp,sp,-64
    23b0:	ffbf0038 	sd	ra,56(sp)
    23b4:	ffbe0030 	sd	s8,48(sp)
    23b8:	ffbc0028 	sd	gp,40(sp)
    23bc:	03a0f025 	move	s8,sp
    23c0:	3c1c0002 	lui	gp,0x2
    23c4:	0399e02d 	daddu	gp,gp,t9
    23c8:	679c5ca4 	daddiu	gp,gp,23716
    23cc:	ffc40010 	sd	a0,16(s8)
    23d0:	ffc50018 	sd	a1,24(s8)
    23d4:	a7c00000 	sh	zero,0(s8)
    23d8:	dfc20010 	ld	v0,16(s8)
    23dc:	90420000 	lbu	v0,0(v0)
    23e0:	304200f0 	andi	v0,v0,0xf0
    23e4:	00401825 	move	v1,v0
    23e8:	24020080 	li	v0,128
    23ec:	14620020 	bne	v1,v0,2470 <main+0xda0>
    23f0:	00000000 	nop
    23f4:	dfc40010 	ld	a0,16(s8)
    23f8:	df828078 	ld	v0,-32648(gp)
    23fc:	0040c825 	move	t9,v0
    2400:	0411fceb 	bal	17b0 <main+0xe0>
    2404:	00000000 	nop
    2408:	a3c20002 	sb	v0,2(s8)
    240c:	93c20002 	lbu	v0,2(s8)
    2410:	64420003 	daddiu	v0,v0,3
    2414:	dfc30010 	ld	v1,16(s8)
    2418:	0062102d 	daddu	v0,v1,v0
    241c:	90420000 	lbu	v0,0(v0)
    2420:	00021200 	sll	v0,v0,0x8
    2424:	a7c20000 	sh	v0,0(s8)
    2428:	93c20002 	lbu	v0,2(s8)
    242c:	64420004 	daddiu	v0,v0,4
    2430:	dfc30010 	ld	v1,16(s8)
    2434:	0062102d 	daddu	v0,v1,v0
    2438:	90420000 	lbu	v0,0(v0)
    243c:	00401825 	move	v1,v0
    2440:	97c20000 	lhu	v0,0(s8)
    2444:	00431025 	or	v0,v0,v1
    2448:	a7c20000 	sh	v0,0(s8)
    244c:	93c20002 	lbu	v0,2(s8)
    2450:	24420003 	addiu	v0,v0,3
    2454:	64420002 	daddiu	v0,v0,2
    2458:	dfc30010 	ld	v1,16(s8)
    245c:	0062182d 	daddu	v1,v1,v0
    2460:	dfc20018 	ld	v0,24(s8)
    2464:	fc430000 	sd	v1,0(v0)
    2468:	10000003 	b	2478 <main+0xda8>
    246c:	00000000 	nop
    2470:	dfc20018 	ld	v0,24(s8)
    2474:	fc400000 	sd	zero,0(v0)
    2478:	97c20000 	lhu	v0,0(s8)
    247c:	03c0e825 	move	sp,s8
    2480:	dfbf0038 	ld	ra,56(sp)
    2484:	dfbe0030 	ld	s8,48(sp)
    2488:	dfbc0028 	ld	gp,40(sp)
    248c:	67bd0040 	daddiu	sp,sp,64
    2490:	03e00008 	jr	ra
    2494:	00000000 	nop
    2498:	67bdffc0 	daddiu	sp,sp,-64
    249c:	ffbf0038 	sd	ra,56(sp)
    24a0:	ffbe0030 	sd	s8,48(sp)
    24a4:	ffbc0028 	sd	gp,40(sp)
    24a8:	03a0f025 	move	s8,sp
    24ac:	3c1c0002 	lui	gp,0x2
    24b0:	0399e02d 	daddu	gp,gp,t9
    24b4:	679c5bb8 	daddiu	gp,gp,23480
    24b8:	ffc40010 	sd	a0,16(s8)
    24bc:	ffc50018 	sd	a1,24(s8)
    24c0:	a7c00000 	sh	zero,0(s8)
    24c4:	dfc20010 	ld	v0,16(s8)
    24c8:	90420000 	lbu	v0,0(v0)
    24cc:	304200f0 	andi	v0,v0,0xf0
    24d0:	00401825 	move	v1,v0
    24d4:	240200a0 	li	v0,160
    24d8:	14620020 	bne	v1,v0,255c <main+0xe8c>
    24dc:	00000000 	nop
    24e0:	dfc40010 	ld	a0,16(s8)
    24e4:	df828078 	ld	v0,-32648(gp)
    24e8:	0040c825 	move	t9,v0
    24ec:	0411fcb0 	bal	17b0 <main+0xe0>
    24f0:	00000000 	nop
    24f4:	a3c20002 	sb	v0,2(s8)
    24f8:	93c20002 	lbu	v0,2(s8)
    24fc:	64420003 	daddiu	v0,v0,3
    2500:	dfc30010 	ld	v1,16(s8)
    2504:	0062102d 	daddu	v0,v1,v0
    2508:	90420000 	lbu	v0,0(v0)
    250c:	00021200 	sll	v0,v0,0x8
    2510:	a7c20000 	sh	v0,0(s8)
    2514:	93c20002 	lbu	v0,2(s8)
    2518:	64420004 	daddiu	v0,v0,4
    251c:	dfc30010 	ld	v1,16(s8)
    2520:	0062102d 	daddu	v0,v1,v0
    2524:	90420000 	lbu	v0,0(v0)
    2528:	00401825 	move	v1,v0
    252c:	97c20000 	lhu	v0,0(s8)
    2530:	00431025 	or	v0,v0,v1
    2534:	a7c20000 	sh	v0,0(s8)
    2538:	93c20002 	lbu	v0,2(s8)
    253c:	24420003 	addiu	v0,v0,3
    2540:	64420002 	daddiu	v0,v0,2
    2544:	dfc30010 	ld	v1,16(s8)
    2548:	0062182d 	daddu	v1,v1,v0
    254c:	dfc20018 	ld	v0,24(s8)
    2550:	fc430000 	sd	v1,0(v0)
    2554:	10000003 	b	2564 <main+0xe94>
    2558:	00000000 	nop
    255c:	dfc20018 	ld	v0,24(s8)
    2560:	fc400000 	sd	zero,0(v0)
    2564:	97c20000 	lhu	v0,0(s8)
    2568:	03c0e825 	move	sp,s8
    256c:	dfbf0038 	ld	ra,56(sp)
    2570:	dfbe0030 	ld	s8,48(sp)
    2574:	dfbc0028 	ld	gp,40(sp)
    2578:	67bd0040 	daddiu	sp,sp,64
    257c:	03e00008 	jr	ra
    2580:	00000000 	nop
    2584:	67bdffc0 	daddiu	sp,sp,-64
    2588:	ffbf0038 	sd	ra,56(sp)
    258c:	ffbe0030 	sd	s8,48(sp)
    2590:	ffbc0028 	sd	gp,40(sp)
    2594:	03a0f025 	move	s8,sp
    2598:	3c1c0002 	lui	gp,0x2
    259c:	0399e02d 	daddu	gp,gp,t9
    25a0:	679c5acc 	daddiu	gp,gp,23244
    25a4:	ffc40000 	sd	a0,0(s8)
    25a8:	ffc50008 	sd	a1,8(s8)
    25ac:	00c01825 	move	v1,a2
    25b0:	00e01025 	move	v0,a3
    25b4:	00031800 	sll	v1,v1,0x0
    25b8:	a7c30010 	sh	v1,16(s8)
    25bc:	00021000 	sll	v0,v0,0x0
    25c0:	a3c20012 	sb	v0,18(s8)
    25c4:	93c30012 	lbu	v1,18(s8)
    25c8:	97c20010 	lhu	v0,16(s8)
    25cc:	00004825 	move	a5,zero
    25d0:	24080002 	li	a4,2
    25d4:	00603825 	move	a3,v1
    25d8:	00403025 	move	a2,v0
    25dc:	dfc50008 	ld	a1,8(s8)
    25e0:	dfc40000 	ld	a0,0(s8)
    25e4:	df828098 	ld	v0,-32616(gp)
    25e8:	0040c825 	move	t9,v0
    25ec:	04110008 	bal	2610 <main+0xf40>
    25f0:	00000000 	nop
    25f4:	03c0e825 	move	sp,s8
    25f8:	dfbf0038 	ld	ra,56(sp)
    25fc:	dfbe0030 	ld	s8,48(sp)
    2600:	dfbc0028 	ld	gp,40(sp)
    2604:	67bd0040 	daddiu	sp,sp,64
    2608:	03e00008 	jr	ra
    260c:	00000000 	nop
    2610:	67bdff80 	daddiu	sp,sp,-128
    2614:	ffbf0078 	sd	ra,120(sp)
    2618:	ffbe0070 	sd	s8,112(sp)
    261c:	ffbc0068 	sd	gp,104(sp)
    2620:	03a0f025 	move	s8,sp
    2624:	3c1c0002 	lui	gp,0x2
    2628:	0399e02d 	daddu	gp,gp,t9
    262c:	679c5a40 	daddiu	gp,gp,23104
    2630:	ffc40040 	sd	a0,64(s8)
    2634:	ffc50048 	sd	a1,72(s8)
    2638:	00c02025 	move	a0,a2
    263c:	00e01825 	move	v1,a3
    2640:	01001025 	move	v0,a4
    2644:	ffc90058 	sd	a5,88(s8)
    2648:	00042000 	sll	a0,a0,0x0
    264c:	a7c40050 	sh	a0,80(s8)
    2650:	00031800 	sll	v1,v1,0x0
    2654:	a3c30052 	sb	v1,82(s8)
    2658:	00021000 	sll	v0,v0,0x0
    265c:	a3c20053 	sb	v0,83(s8)
    2660:	df8280a0 	ld	v0,-32608(gp)
    2664:	0040c825 	move	t9,v0
    2668:	0411028a 	bal	3094 <main+0x19c4>
    266c:	00000000 	nop
    2670:	ffc20008 	sd	v0,8(s8)
    2674:	dfc20008 	ld	v0,8(s8)
    2678:	14400004 	bnez	v0,268c <main+0xfbc>
    267c:	00000000 	nop
    2680:	2402ffff 	li	v0,-1
    2684:	10000110 	b	2ac8 <main+0x13f8>
    2688:	00000000 	nop
    268c:	dfc40040 	ld	a0,64(s8)
    2690:	df8281e0 	ld	v0,-32288(gp)
    2694:	0040c825 	move	t9,v0
    2698:	0320f809 	jalr	t9
    269c:	00000000 	nop
    26a0:	a7c20010 	sh	v0,16(s8)
    26a4:	97c20050 	lhu	v0,80(s8)
    26a8:	a7c20012 	sh	v0,18(s8)
    26ac:	ffc00018 	sd	zero,24(s8)
    26b0:	ffc00020 	sd	zero,32(s8)
    26b4:	a3c00000 	sb	zero,0(s8)
    26b8:	a3c00028 	sb	zero,40(s8)
    26bc:	a7c0002a 	sh	zero,42(s8)
    26c0:	ffc00030 	sd	zero,48(s8)
    26c4:	a7c00038 	sh	zero,56(s8)
    26c8:	a3c00001 	sb	zero,1(s8)
    26cc:	a3c00002 	sb	zero,2(s8)
    26d0:	93c30053 	lbu	v1,83(s8)
    26d4:	24020001 	li	v0,1
    26d8:	14620007 	bne	v1,v0,26f8 <main+0x1028>
    26dc:	00000000 	nop
    26e0:	24020002 	li	v0,2
    26e4:	a3c20002 	sb	v0,2(s8)
    26e8:	24020002 	li	v0,2
    26ec:	a3c20001 	sb	v0,1(s8)
    26f0:	10000009 	b	2718 <main+0x1048>
    26f4:	00000000 	nop
    26f8:	93c30053 	lbu	v1,83(s8)
    26fc:	24020002 	li	v0,2
    2700:	14620005 	bne	v1,v0,2718 <main+0x1048>
    2704:	00000000 	nop
    2708:	24020002 	li	v0,2
    270c:	a3c20002 	sb	v0,2(s8)
    2710:	24020004 	li	v0,4
    2714:	a3c20001 	sb	v0,1(s8)
    2718:	97c20010 	lhu	v0,16(s8)
    271c:	304200ff 	andi	v0,v0,0xff
    2720:	93c30002 	lbu	v1,2(s8)
    2724:	00621021 	addu	v0,v1,v0
    2728:	304200ff 	andi	v0,v0,0xff
    272c:	24420002 	addiu	v0,v0,2
    2730:	a3c20028 	sb	v0,40(s8)
    2734:	93c20028 	lbu	v0,40(s8)
    2738:	00402025 	move	a0,v0
    273c:	df828260 	ld	v0,-32160(gp)
    2740:	0040c825 	move	t9,v0
    2744:	0320f809 	jalr	t9
    2748:	00000000 	nop
    274c:	ffc20018 	sd	v0,24(s8)
    2750:	93c20028 	lbu	v0,40(s8)
    2754:	00403025 	move	a2,v0
    2758:	00002825 	move	a1,zero
    275c:	dfc40018 	ld	a0,24(s8)
    2760:	df8281f8 	ld	v0,-32264(gp)
    2764:	0040c825 	move	t9,v0
    2768:	0320f809 	jalr	t9
    276c:	00000000 	nop
    2770:	97c20010 	lhu	v0,16(s8)
    2774:	00021202 	srl	v0,v0,0x8
    2778:	3042ffff 	andi	v0,v0,0xffff
    277c:	304300ff 	andi	v1,v0,0xff
    2780:	dfc20018 	ld	v0,24(s8)
    2784:	a0430000 	sb	v1,0(v0)
    2788:	dfc20018 	ld	v0,24(s8)
    278c:	64420001 	daddiu	v0,v0,1
    2790:	97c30010 	lhu	v1,16(s8)
    2794:	306300ff 	andi	v1,v1,0xff
    2798:	a0430000 	sb	v1,0(v0)
    279c:	dfc20018 	ld	v0,24(s8)
    27a0:	64420002 	daddiu	v0,v0,2
    27a4:	97c30010 	lhu	v1,16(s8)
    27a8:	00603025 	move	a2,v1
    27ac:	dfc50040 	ld	a1,64(s8)
    27b0:	00402025 	move	a0,v0
    27b4:	df828280 	ld	v0,-32128(gp)
    27b8:	0040c825 	move	t9,v0
    27bc:	0320f809 	jalr	t9
    27c0:	00000000 	nop
    27c4:	93c20002 	lbu	v0,2(s8)
    27c8:	1040002a 	beqz	v0,2874 <main+0x11a4>
    27cc:	00000000 	nop
    27d0:	dfc20008 	ld	v0,8(s8)
    27d4:	8c42000c 	lw	v0,12(v0)
    27d8:	24420001 	addiu	v0,v0,1
    27dc:	00401825 	move	v1,v0
    27e0:	dfc20008 	ld	v0,8(s8)
    27e4:	ac43000c 	sw	v1,12(v0)
    27e8:	dfc20008 	ld	v0,8(s8)
    27ec:	8c42000c 	lw	v0,12(v0)
    27f0:	14400004 	bnez	v0,2804 <main+0x1134>
    27f4:	00000000 	nop
    27f8:	dfc20008 	ld	v0,8(s8)
    27fc:	24030001 	li	v1,1
    2800:	ac43000c 	sw	v1,12(v0)
    2804:	dfc20008 	ld	v0,8(s8)
    2808:	8c42000c 	lw	v0,12(v0)
    280c:	00021202 	srl	v0,v0,0x8
    2810:	00402025 	move	a0,v0
    2814:	97c20010 	lhu	v0,16(s8)
    2818:	64420002 	daddiu	v0,v0,2
    281c:	dfc30018 	ld	v1,24(s8)
    2820:	0062102d 	daddu	v0,v1,v0
    2824:	00801825 	move	v1,a0
    2828:	306300ff 	andi	v1,v1,0xff
    282c:	a0430000 	sb	v1,0(v0)
    2830:	dfc20008 	ld	v0,8(s8)
    2834:	8c44000c 	lw	a0,12(v0)
    2838:	97c20010 	lhu	v0,16(s8)
    283c:	64420003 	daddiu	v0,v0,3
    2840:	dfc30018 	ld	v1,24(s8)
    2844:	0062102d 	daddu	v0,v1,v0
    2848:	00801825 	move	v1,a0
    284c:	306300ff 	andi	v1,v1,0xff
    2850:	a0430000 	sb	v1,0(v0)
    2854:	dfc20058 	ld	v0,88(s8)
    2858:	10400006 	beqz	v0,2874 <main+0x11a4>
    285c:	00000000 	nop
    2860:	dfc20008 	ld	v0,8(s8)
    2864:	8c42000c 	lw	v0,12(v0)
    2868:	3043ffff 	andi	v1,v0,0xffff
    286c:	dfc20058 	ld	v0,88(s8)
    2870:	a4430000 	sh	v1,0(v0)
    2874:	24020002 	li	v0,2
    2878:	a3c20000 	sb	v0,0(s8)
    287c:	93c20028 	lbu	v0,40(s8)
    2880:	3042ffff 	andi	v0,v0,0xffff
    2884:	97c30012 	lhu	v1,18(s8)
    2888:	00621021 	addu	v0,v1,v0
    288c:	a7c2002a 	sh	v0,42(s8)
    2890:	97c2002a 	lhu	v0,42(s8)
    2894:	2c420080 	sltiu	v0,v0,128
    2898:	14400004 	bnez	v0,28ac <main+0x11dc>
    289c:	00000000 	nop
    28a0:	93c20000 	lbu	v0,0(s8)
    28a4:	24420001 	addiu	v0,v0,1
    28a8:	a3c20000 	sb	v0,0(s8)
    28ac:	93c20000 	lbu	v0,0(s8)
    28b0:	00402025 	move	a0,v0
    28b4:	df828260 	ld	v0,-32160(gp)
    28b8:	0040c825 	move	t9,v0
    28bc:	0320f809 	jalr	t9
    28c0:	00000000 	nop
    28c4:	ffc20020 	sd	v0,32(s8)
    28c8:	93c20001 	lbu	v0,1(s8)
    28cc:	34420030 	ori	v0,v0,0x30
    28d0:	304300ff 	andi	v1,v0,0xff
    28d4:	dfc20020 	ld	v0,32(s8)
    28d8:	a0430000 	sb	v1,0(v0)
    28dc:	93c20052 	lbu	v0,82(s8)
    28e0:	10400007 	beqz	v0,2900 <main+0x1230>
    28e4:	00000000 	nop
    28e8:	dfc20020 	ld	v0,32(s8)
    28ec:	90420000 	lbu	v0,0(v0)
    28f0:	34420001 	ori	v0,v0,0x1
    28f4:	304300ff 	andi	v1,v0,0xff
    28f8:	dfc20020 	ld	v0,32(s8)
    28fc:	a0430000 	sb	v1,0(v0)
    2900:	97c2002a 	lhu	v0,42(s8)
    2904:	2c420080 	sltiu	v0,v0,128
    2908:	10400008 	beqz	v0,292c <main+0x125c>
    290c:	00000000 	nop
    2910:	dfc20020 	ld	v0,32(s8)
    2914:	64420001 	daddiu	v0,v0,1
    2918:	97c3002a 	lhu	v1,42(s8)
    291c:	306300ff 	andi	v1,v1,0xff
    2920:	a0430000 	sb	v1,0(v0)
    2924:	10000018 	b	2988 <main+0x12b8>
    2928:	00000000 	nop
    292c:	97c2002a 	lhu	v0,42(s8)
    2930:	304300ff 	andi	v1,v0,0xff
    2934:	dfc20020 	ld	v0,32(s8)
    2938:	64420001 	daddiu	v0,v0,1
    293c:	3063007f 	andi	v1,v1,0x7f
    2940:	306300ff 	andi	v1,v1,0xff
    2944:	a0430000 	sb	v1,0(v0)
    2948:	dfc20020 	ld	v0,32(s8)
    294c:	64420001 	daddiu	v0,v0,1
    2950:	90440000 	lbu	a0,0(v0)
    2954:	dfc20020 	ld	v0,32(s8)
    2958:	64420001 	daddiu	v0,v0,1
    295c:	2403ff80 	li	v1,-128
    2960:	00831825 	or	v1,a0,v1
    2964:	306300ff 	andi	v1,v1,0xff
    2968:	a0430000 	sb	v1,0(v0)
    296c:	97c2002a 	lhu	v0,42(s8)
    2970:	000211c2 	srl	v0,v0,0x7
    2974:	3043ffff 	andi	v1,v0,0xffff
    2978:	dfc20020 	ld	v0,32(s8)
    297c:	64420002 	daddiu	v0,v0,2
    2980:	306300ff 	andi	v1,v1,0xff
    2984:	a0430000 	sb	v1,0(v0)
    2988:	93c20000 	lbu	v0,0(s8)
    298c:	3043ffff 	andi	v1,v0,0xffff
    2990:	93c20028 	lbu	v0,40(s8)
    2994:	3042ffff 	andi	v0,v0,0xffff
    2998:	00621021 	addu	v0,v1,v0
    299c:	3042ffff 	andi	v0,v0,0xffff
    29a0:	97c30012 	lhu	v1,18(s8)
    29a4:	00621021 	addu	v0,v1,v0
    29a8:	a7c20038 	sh	v0,56(s8)
    29ac:	97c20038 	lhu	v0,56(s8)
    29b0:	00402025 	move	a0,v0
    29b4:	df828260 	ld	v0,-32160(gp)
    29b8:	0040c825 	move	t9,v0
    29bc:	0320f809 	jalr	t9
    29c0:	00000000 	nop
    29c4:	ffc20030 	sd	v0,48(s8)
    29c8:	97c20038 	lhu	v0,56(s8)
    29cc:	00403025 	move	a2,v0
    29d0:	00002825 	move	a1,zero
    29d4:	dfc40030 	ld	a0,48(s8)
    29d8:	df8281f8 	ld	v0,-32264(gp)
    29dc:	0040c825 	move	t9,v0
    29e0:	0320f809 	jalr	t9
    29e4:	00000000 	nop
    29e8:	93c20000 	lbu	v0,0(s8)
    29ec:	00403025 	move	a2,v0
    29f0:	dfc50020 	ld	a1,32(s8)
    29f4:	dfc40030 	ld	a0,48(s8)
    29f8:	df828280 	ld	v0,-32128(gp)
    29fc:	0040c825 	move	t9,v0
    2a00:	0320f809 	jalr	t9
    2a04:	00000000 	nop
    2a08:	93c20000 	lbu	v0,0(s8)
    2a0c:	dfc30030 	ld	v1,48(s8)
    2a10:	0062102d 	daddu	v0,v1,v0
    2a14:	93c30028 	lbu	v1,40(s8)
    2a18:	00603025 	move	a2,v1
    2a1c:	dfc50018 	ld	a1,24(s8)
    2a20:	00402025 	move	a0,v0
    2a24:	df828280 	ld	v0,-32128(gp)
    2a28:	0040c825 	move	t9,v0
    2a2c:	0320f809 	jalr	t9
    2a30:	00000000 	nop
    2a34:	93c30000 	lbu	v1,0(s8)
    2a38:	93c20028 	lbu	v0,40(s8)
    2a3c:	0062102d 	daddu	v0,v1,v0
    2a40:	dfc30030 	ld	v1,48(s8)
    2a44:	0062102d 	daddu	v0,v1,v0
    2a48:	97c30012 	lhu	v1,18(s8)
    2a4c:	00603025 	move	a2,v1
    2a50:	dfc50048 	ld	a1,72(s8)
    2a54:	00402025 	move	a0,v0
    2a58:	df828280 	ld	v0,-32128(gp)
    2a5c:	0040c825 	move	t9,v0
    2a60:	0320f809 	jalr	t9
    2a64:	00000000 	nop
    2a68:	dfc40018 	ld	a0,24(s8)
    2a6c:	df8281d0 	ld	v0,-32304(gp)
    2a70:	0040c825 	move	t9,v0
    2a74:	0320f809 	jalr	t9
    2a78:	00000000 	nop
    2a7c:	dfc40020 	ld	a0,32(s8)
    2a80:	df8281d0 	ld	v0,-32304(gp)
    2a84:	0040c825 	move	t9,v0
    2a88:	0320f809 	jalr	t9
    2a8c:	00000000 	nop
    2a90:	97c20038 	lhu	v0,56(s8)
    2a94:	00403025 	move	a2,v0
    2a98:	dfc50030 	ld	a1,48(s8)
    2a9c:	24040001 	li	a0,1
    2aa0:	df8280a8 	ld	v0,-32600(gp)
    2aa4:	0040c825 	move	t9,v0
    2aa8:	04110187 	bal	30c8 <main+0x19f8>
    2aac:	00000000 	nop
    2ab0:	dfc40030 	ld	a0,48(s8)
    2ab4:	df8281d0 	ld	v0,-32304(gp)
    2ab8:	0040c825 	move	t9,v0
    2abc:	0320f809 	jalr	t9
    2ac0:	00000000 	nop
    2ac4:	24020001 	li	v0,1
    2ac8:	03c0e825 	move	sp,s8
    2acc:	dfbf0078 	ld	ra,120(sp)
    2ad0:	dfbe0070 	ld	s8,112(sp)
    2ad4:	dfbc0068 	ld	gp,104(sp)
    2ad8:	67bd0080 	daddiu	sp,sp,128
    2adc:	03e00008 	jr	ra
    2ae0:	00000000 	nop
    2ae4:	67bdff90 	daddiu	sp,sp,-112
    2ae8:	ffbf0068 	sd	ra,104(sp)
    2aec:	ffbe0060 	sd	s8,96(sp)
    2af0:	ffbc0058 	sd	gp,88(sp)
    2af4:	03a0f025 	move	s8,sp
    2af8:	3c1c0002 	lui	gp,0x2
    2afc:	0399e02d 	daddu	gp,gp,t9
    2b00:	679c556c 	daddiu	gp,gp,21868
    2b04:	00801025 	move	v0,a0
    2b08:	00021000 	sll	v0,v0,0x0
    2b0c:	a3c20040 	sb	v0,64(s8)
    2b10:	df8280a0 	ld	v0,-32608(gp)
    2b14:	0040c825 	move	t9,v0
    2b18:	0411015e 	bal	3094 <main+0x19c4>
    2b1c:	00000000 	nop
    2b20:	ffc20000 	sd	v0,0(s8)
    2b24:	dfc20000 	ld	v0,0(s8)
    2b28:	10400067 	beqz	v0,2cc8 <main+0x15f8>
    2b2c:	00000000 	nop
    2b30:	93c20040 	lbu	v0,64(s8)
    2b34:	2c430006 	sltiu	v1,v0,6
    2b38:	10600064 	beqz	v1,2ccc <main+0x15fc>
    2b3c:	00000000 	nop
    2b40:	000218f8 	dsll	v1,v0,0x3
    2b44:	df828058 	ld	v0,-32680(gp)
    2b48:	64426e48 	daddiu	v0,v0,28232
    2b4c:	0062102d 	daddu	v0,v1,v0
    2b50:	dc420000 	ld	v0,0(v0)
    2b54:	005c102d 	daddu	v0,v0,gp
    2b58:	00400008 	jr	v0
    2b5c:	00000000 	nop
    2b60:	dfc20000 	ld	v0,0(s8)
    2b64:	24030001 	li	v1,1
    2b68:	a0430001 	sb	v1,1(v0)
    2b6c:	3c022002 	lui	v0,0x2002
    2b70:	afc20008 	sw	v0,8(s8)
    2b74:	67c20008 	daddiu	v0,s8,8
    2b78:	24060004 	li	a2,4
    2b7c:	00402825 	move	a1,v0
    2b80:	24040001 	li	a0,1
    2b84:	df8280a8 	ld	v0,-32600(gp)
    2b88:	0040c825 	move	t9,v0
    2b8c:	0411014e 	bal	30c8 <main+0x19f8>
    2b90:	00000000 	nop
    2b94:	1000004d 	b	2ccc <main+0x15fc>
    2b98:	00000000 	nop
    2b9c:	dfc20000 	ld	v0,0(s8)
    2ba0:	a0400001 	sb	zero,1(v0)
    2ba4:	3c022002 	lui	v0,0x2002
    2ba8:	34420001 	ori	v0,v0,0x1
    2bac:	afc20010 	sw	v0,16(s8)
    2bb0:	67c20010 	daddiu	v0,s8,16
    2bb4:	24060004 	li	a2,4
    2bb8:	00402825 	move	a1,v0
    2bbc:	24040001 	li	a0,1
    2bc0:	df8280a8 	ld	v0,-32600(gp)
    2bc4:	0040c825 	move	t9,v0
    2bc8:	0411013f 	bal	30c8 <main+0x19f8>
    2bcc:	00000000 	nop
    2bd0:	1000003e 	b	2ccc <main+0x15fc>
    2bd4:	00000000 	nop
    2bd8:	dfc20000 	ld	v0,0(s8)
    2bdc:	a0400001 	sb	zero,1(v0)
    2be0:	3c022002 	lui	v0,0x2002
    2be4:	34420002 	ori	v0,v0,0x2
    2be8:	afc20018 	sw	v0,24(s8)
    2bec:	67c20018 	daddiu	v0,s8,24
    2bf0:	24060004 	li	a2,4
    2bf4:	00402825 	move	a1,v0
    2bf8:	24040001 	li	a0,1
    2bfc:	df8280a8 	ld	v0,-32600(gp)
    2c00:	0040c825 	move	t9,v0
    2c04:	04110130 	bal	30c8 <main+0x19f8>
    2c08:	00000000 	nop
    2c0c:	1000002f 	b	2ccc <main+0x15fc>
    2c10:	00000000 	nop
    2c14:	dfc20000 	ld	v0,0(s8)
    2c18:	a0400001 	sb	zero,1(v0)
    2c1c:	3c022002 	lui	v0,0x2002
    2c20:	34420003 	ori	v0,v0,0x3
    2c24:	afc20020 	sw	v0,32(s8)
    2c28:	67c20020 	daddiu	v0,s8,32
    2c2c:	24060004 	li	a2,4
    2c30:	00402825 	move	a1,v0
    2c34:	24040001 	li	a0,1
    2c38:	df8280a8 	ld	v0,-32600(gp)
    2c3c:	0040c825 	move	t9,v0
    2c40:	04110121 	bal	30c8 <main+0x19f8>
    2c44:	00000000 	nop
    2c48:	10000020 	b	2ccc <main+0x15fc>
    2c4c:	00000000 	nop
    2c50:	dfc20000 	ld	v0,0(s8)
    2c54:	a0400001 	sb	zero,1(v0)
    2c58:	3c022002 	lui	v0,0x2002
    2c5c:	34420004 	ori	v0,v0,0x4
    2c60:	afc20028 	sw	v0,40(s8)
    2c64:	67c20028 	daddiu	v0,s8,40
    2c68:	24060004 	li	a2,4
    2c6c:	00402825 	move	a1,v0
    2c70:	24040001 	li	a0,1
    2c74:	df8280a8 	ld	v0,-32600(gp)
    2c78:	0040c825 	move	t9,v0
    2c7c:	04110112 	bal	30c8 <main+0x19f8>
    2c80:	00000000 	nop
    2c84:	10000011 	b	2ccc <main+0x15fc>
    2c88:	00000000 	nop
    2c8c:	dfc20000 	ld	v0,0(s8)
    2c90:	a0400001 	sb	zero,1(v0)
    2c94:	3c022002 	lui	v0,0x2002
    2c98:	34420005 	ori	v0,v0,0x5
    2c9c:	afc20030 	sw	v0,48(s8)
    2ca0:	67c20030 	daddiu	v0,s8,48
    2ca4:	24060004 	li	a2,4
    2ca8:	00402825 	move	a1,v0
    2cac:	24040001 	li	a0,1
    2cb0:	df8280a8 	ld	v0,-32600(gp)
    2cb4:	0040c825 	move	t9,v0
    2cb8:	04110103 	bal	30c8 <main+0x19f8>
    2cbc:	00000000 	nop
    2cc0:	10000002 	b	2ccc <main+0x15fc>
    2cc4:	00000000 	nop
    2cc8:	00000000 	nop
    2ccc:	03c0e825 	move	sp,s8
    2cd0:	dfbf0068 	ld	ra,104(sp)
    2cd4:	dfbe0060 	ld	s8,96(sp)
    2cd8:	dfbc0058 	ld	gp,88(sp)
    2cdc:	67bd0070 	daddiu	sp,sp,112
    2ce0:	03e00008 	jr	ra
    2ce4:	00000000 	nop
    2ce8:	67bdffd0 	daddiu	sp,sp,-48
    2cec:	ffbf0028 	sd	ra,40(sp)
    2cf0:	ffbe0020 	sd	s8,32(sp)
    2cf4:	ffbc0018 	sd	gp,24(sp)
    2cf8:	03a0f025 	move	s8,sp
    2cfc:	3c1c0002 	lui	gp,0x2
    2d00:	0399e02d 	daddu	gp,gp,t9
    2d04:	679c5368 	daddiu	gp,gp,21352
    2d08:	2402d000 	li	v0,-12288
    2d0c:	a7c20000 	sh	v0,0(s8)
    2d10:	24060002 	li	a2,2
    2d14:	03c02825 	move	a1,s8
    2d18:	24040001 	li	a0,1
    2d1c:	df8280a8 	ld	v0,-32600(gp)
    2d20:	0040c825 	move	t9,v0
    2d24:	041100e8 	bal	30c8 <main+0x19f8>
    2d28:	00000000 	nop
    2d2c:	00000000 	nop
    2d30:	03c0e825 	move	sp,s8
    2d34:	dfbf0028 	ld	ra,40(sp)
    2d38:	dfbe0020 	ld	s8,32(sp)
    2d3c:	dfbc0018 	ld	gp,24(sp)
    2d40:	67bd0030 	daddiu	sp,sp,48
    2d44:	03e00008 	jr	ra
    2d48:	00000000 	nop
    2d4c:	67bdffc0 	daddiu	sp,sp,-64
    2d50:	ffbf0038 	sd	ra,56(sp)
    2d54:	ffbe0030 	sd	s8,48(sp)
    2d58:	ffbc0028 	sd	gp,40(sp)
    2d5c:	03a0f025 	move	s8,sp
    2d60:	3c1c0002 	lui	gp,0x2
    2d64:	0399e02d 	daddu	gp,gp,t9
    2d68:	679c5304 	daddiu	gp,gp,21252
    2d6c:	ffc40010 	sd	a0,16(s8)
    2d70:	dfc40010 	ld	a0,16(s8)
    2d74:	df8280b0 	ld	v0,-32592(gp)
    2d78:	0040c825 	move	t9,v0
    2d7c:	0411fc46 	bal	1e98 <main+0x7c8>
    2d80:	00000000 	nop
    2d84:	a7c20000 	sh	v0,0(s8)
    2d88:	dfc20010 	ld	v0,16(s8)
    2d8c:	90420000 	lbu	v0,0(v0)
    2d90:	00021043 	sra	v0,v0,0x1
    2d94:	304200ff 	andi	v0,v0,0xff
    2d98:	30420003 	andi	v0,v0,0x3
    2d9c:	a3c20002 	sb	v0,2(s8)
    2da0:	2402ff90 	li	v0,-112
    2da4:	a3c20008 	sb	v0,8(s8)
    2da8:	24020003 	li	v0,3
    2dac:	a3c20009 	sb	v0,9(s8)
    2db0:	97c20000 	lhu	v0,0(s8)
    2db4:	00021202 	srl	v0,v0,0x8
    2db8:	3042ffff 	andi	v0,v0,0xffff
    2dbc:	304200ff 	andi	v0,v0,0xff
    2dc0:	a3c2000a 	sb	v0,10(s8)
    2dc4:	97c20000 	lhu	v0,0(s8)
    2dc8:	304200ff 	andi	v0,v0,0xff
    2dcc:	a3c2000b 	sb	v0,11(s8)
    2dd0:	93c20002 	lbu	v0,2(s8)
    2dd4:	a3c2000c 	sb	v0,12(s8)
    2dd8:	67c20008 	daddiu	v0,s8,8
    2ddc:	24060005 	li	a2,5
    2de0:	00402825 	move	a1,v0
    2de4:	24040001 	li	a0,1
    2de8:	df8280a8 	ld	v0,-32600(gp)
    2dec:	0040c825 	move	t9,v0
    2df0:	041100b5 	bal	30c8 <main+0x19f8>
    2df4:	00000000 	nop
    2df8:	00000000 	nop
    2dfc:	03c0e825 	move	sp,s8
    2e00:	dfbf0038 	ld	ra,56(sp)
    2e04:	dfbe0030 	ld	s8,48(sp)
    2e08:	dfbc0028 	ld	gp,40(sp)
    2e0c:	67bd0040 	daddiu	sp,sp,64
    2e10:	03e00008 	jr	ra
    2e14:	00000000 	nop
    2e18:	67bdffc0 	daddiu	sp,sp,-64
    2e1c:	ffbf0038 	sd	ra,56(sp)
    2e20:	ffbe0030 	sd	s8,48(sp)
    2e24:	ffbc0028 	sd	gp,40(sp)
    2e28:	03a0f025 	move	s8,sp
    2e2c:	3c1c0002 	lui	gp,0x2
    2e30:	0399e02d 	daddu	gp,gp,t9
    2e34:	679c5238 	daddiu	gp,gp,21048
    2e38:	ffc40010 	sd	a0,16(s8)
    2e3c:	dfc40010 	ld	a0,16(s8)
    2e40:	df8280b0 	ld	v0,-32592(gp)
    2e44:	0040c825 	move	t9,v0
    2e48:	0411fc13 	bal	1e98 <main+0x7c8>
    2e4c:	00000000 	nop
    2e50:	a7c20000 	sh	v0,0(s8)
    2e54:	2402ffb0 	li	v0,-80
    2e58:	a3c20008 	sb	v0,8(s8)
    2e5c:	24020002 	li	v0,2
    2e60:	a3c20009 	sb	v0,9(s8)
    2e64:	97c20000 	lhu	v0,0(s8)
    2e68:	00021202 	srl	v0,v0,0x8
    2e6c:	3042ffff 	andi	v0,v0,0xffff
    2e70:	304200ff 	andi	v0,v0,0xff
    2e74:	a3c2000a 	sb	v0,10(s8)
    2e78:	97c20000 	lhu	v0,0(s8)
    2e7c:	304200ff 	andi	v0,v0,0xff
    2e80:	a3c2000b 	sb	v0,11(s8)
    2e84:	67c20008 	daddiu	v0,s8,8
    2e88:	24060004 	li	a2,4
    2e8c:	00402825 	move	a1,v0
    2e90:	24040001 	li	a0,1
    2e94:	df8280a8 	ld	v0,-32600(gp)
    2e98:	0040c825 	move	t9,v0
    2e9c:	0411008a 	bal	30c8 <main+0x19f8>
    2ea0:	00000000 	nop
    2ea4:	00000000 	nop
    2ea8:	03c0e825 	move	sp,s8
    2eac:	dfbf0038 	ld	ra,56(sp)
    2eb0:	dfbe0030 	ld	s8,48(sp)
    2eb4:	dfbc0028 	ld	gp,40(sp)
    2eb8:	67bd0040 	daddiu	sp,sp,64
    2ebc:	03e00008 	jr	ra
    2ec0:	00000000 	nop
    2ec4:	67bdffc0 	daddiu	sp,sp,-64
    2ec8:	ffbf0038 	sd	ra,56(sp)
    2ecc:	ffbe0030 	sd	s8,48(sp)
    2ed0:	ffbc0028 	sd	gp,40(sp)
    2ed4:	03a0f025 	move	s8,sp
    2ed8:	3c1c0002 	lui	gp,0x2
    2edc:	0399e02d 	daddu	gp,gp,t9
    2ee0:	679c518c 	daddiu	gp,gp,20876
    2ee4:	ffc40010 	sd	a0,16(s8)
    2ee8:	dfc40010 	ld	a0,16(s8)
    2eec:	df8280b0 	ld	v0,-32592(gp)
    2ef0:	0040c825 	move	t9,v0
    2ef4:	0411fbe8 	bal	1e98 <main+0x7c8>
    2ef8:	00000000 	nop
    2efc:	a7c20000 	sh	v0,0(s8)
    2f00:	24020062 	li	v0,98
    2f04:	a3c20008 	sb	v0,8(s8)
    2f08:	24020002 	li	v0,2
    2f0c:	a3c20009 	sb	v0,9(s8)
    2f10:	97c20000 	lhu	v0,0(s8)
    2f14:	00021202 	srl	v0,v0,0x8
    2f18:	3042ffff 	andi	v0,v0,0xffff
    2f1c:	304200ff 	andi	v0,v0,0xff
    2f20:	a3c2000a 	sb	v0,10(s8)
    2f24:	97c20000 	lhu	v0,0(s8)
    2f28:	304200ff 	andi	v0,v0,0xff
    2f2c:	a3c2000b 	sb	v0,11(s8)
    2f30:	67c20008 	daddiu	v0,s8,8
    2f34:	24060004 	li	a2,4
    2f38:	00402825 	move	a1,v0
    2f3c:	24040001 	li	a0,1
    2f40:	df8280a8 	ld	v0,-32600(gp)
    2f44:	0040c825 	move	t9,v0
    2f48:	0411005f 	bal	30c8 <main+0x19f8>
    2f4c:	00000000 	nop
    2f50:	00000000 	nop
    2f54:	03c0e825 	move	sp,s8
    2f58:	dfbf0038 	ld	ra,56(sp)
    2f5c:	dfbe0030 	ld	s8,48(sp)
    2f60:	dfbc0028 	ld	gp,40(sp)
    2f64:	67bd0040 	daddiu	sp,sp,64
    2f68:	03e00008 	jr	ra
    2f6c:	00000000 	nop
    2f70:	67bdffc0 	daddiu	sp,sp,-64
    2f74:	ffbf0038 	sd	ra,56(sp)
    2f78:	ffbe0030 	sd	s8,48(sp)
    2f7c:	ffbc0028 	sd	gp,40(sp)
    2f80:	03a0f025 	move	s8,sp
    2f84:	3c1c0002 	lui	gp,0x2
    2f88:	0399e02d 	daddu	gp,gp,t9
    2f8c:	679c50e0 	daddiu	gp,gp,20704
    2f90:	ffc40010 	sd	a0,16(s8)
    2f94:	dfc40010 	ld	a0,16(s8)
    2f98:	df8280b0 	ld	v0,-32592(gp)
    2f9c:	0040c825 	move	t9,v0
    2fa0:	0411fbbd 	bal	1e98 <main+0x7c8>
    2fa4:	00000000 	nop
    2fa8:	a7c20000 	sh	v0,0(s8)
    2fac:	24020070 	li	v0,112
    2fb0:	a3c20008 	sb	v0,8(s8)
    2fb4:	24020002 	li	v0,2
    2fb8:	a3c20009 	sb	v0,9(s8)
    2fbc:	97c20000 	lhu	v0,0(s8)
    2fc0:	00021202 	srl	v0,v0,0x8
    2fc4:	3042ffff 	andi	v0,v0,0xffff
    2fc8:	304200ff 	andi	v0,v0,0xff
    2fcc:	a3c2000a 	sb	v0,10(s8)
    2fd0:	97c20000 	lhu	v0,0(s8)
    2fd4:	304200ff 	andi	v0,v0,0xff
    2fd8:	a3c2000b 	sb	v0,11(s8)
    2fdc:	67c20008 	daddiu	v0,s8,8
    2fe0:	24060004 	li	a2,4
    2fe4:	00402825 	move	a1,v0
    2fe8:	24040001 	li	a0,1
    2fec:	df8280a8 	ld	v0,-32600(gp)
    2ff0:	0040c825 	move	t9,v0
    2ff4:	04110034 	bal	30c8 <main+0x19f8>
    2ff8:	00000000 	nop
    2ffc:	00000000 	nop
    3000:	03c0e825 	move	sp,s8
    3004:	dfbf0038 	ld	ra,56(sp)
    3008:	dfbe0030 	ld	s8,48(sp)
    300c:	dfbc0028 	ld	gp,40(sp)
    3010:	67bd0040 	daddiu	sp,sp,64
    3014:	03e00008 	jr	ra
    3018:	00000000 	nop
    301c:	00000000 	nop
    3020:	67bdffe0 	daddiu	sp,sp,-32
    3024:	ffbf0018 	sd	ra,24(sp)
    3028:	ffbe0010 	sd	s8,16(sp)
    302c:	ffbc0008 	sd	gp,8(sp)
    3030:	03a0f025 	move	s8,sp
    3034:	3c1c0002 	lui	gp,0x2
    3038:	0399e02d 	daddu	gp,gp,t9
    303c:	679c5030 	daddiu	gp,gp,20528
    3040:	df8280b8 	ld	v0,-32584(gp)
    3044:	dc420000 	ld	v0,0(v0)
    3048:	1040000a 	beqz	v0,3074 <main+0x19a4>
    304c:	00000000 	nop
    3050:	df8280b8 	ld	v0,-32584(gp)
    3054:	dc420000 	ld	v0,0(v0)
    3058:	00402025 	move	a0,v0
    305c:	df8281d0 	ld	v0,-32304(gp)
    3060:	0040c825 	move	t9,v0
    3064:	0320f809 	jalr	t9
    3068:	00000000 	nop
    306c:	df8280b8 	ld	v0,-32584(gp)
    3070:	fc400000 	sd	zero,0(v0)
    3074:	00000000 	nop
    3078:	03c0e825 	move	sp,s8
    307c:	dfbf0018 	ld	ra,24(sp)
    3080:	dfbe0010 	ld	s8,16(sp)
    3084:	dfbc0008 	ld	gp,8(sp)
    3088:	67bd0020 	daddiu	sp,sp,32
    308c:	03e00008 	jr	ra
    3090:	00000000 	nop
    3094:	67bdfff0 	daddiu	sp,sp,-16
    3098:	ffbe0008 	sd	s8,8(sp)
    309c:	03a0f025 	move	s8,sp
    30a0:	3c030002 	lui	v1,0x2
    30a4:	0079182d 	daddu	v1,v1,t9
    30a8:	64634fbc 	daddiu	v1,v1,20412
    30ac:	dc6280b8 	ld	v0,-32584(v1)
    30b0:	dc420000 	ld	v0,0(v0)
    30b4:	03c0e825 	move	sp,s8
    30b8:	dfbe0008 	ld	s8,8(sp)
    30bc:	67bd0010 	daddiu	sp,sp,16
    30c0:	03e00008 	jr	ra
    30c4:	00000000 	nop
    30c8:	67bdffa0 	daddiu	sp,sp,-96
    30cc:	ffbf0058 	sd	ra,88(sp)
    30d0:	ffbe0050 	sd	s8,80(sp)
    30d4:	ffbc0048 	sd	gp,72(sp)
    30d8:	03a0f025 	move	s8,sp
    30dc:	3c1c0002 	lui	gp,0x2
    30e0:	0399e02d 	daddu	gp,gp,t9
    30e4:	679c4f88 	daddiu	gp,gp,20360
    30e8:	00801025 	move	v0,a0
    30ec:	ffc50028 	sd	a1,40(s8)
    30f0:	ffc60030 	sd	a2,48(s8)
    30f4:	00021000 	sll	v0,v0,0x0
    30f8:	afc20020 	sw	v0,32(s8)
    30fc:	dfc20030 	ld	v0,48(s8)
    3100:	ffc20000 	sd	v0,0(s8)
    3104:	dfc20028 	ld	v0,40(s8)
    3108:	ffc20010 	sd	v0,16(s8)
    310c:	10000031 	b	31d4 <main+0x1b04>
    3110:	00000000 	nop
    3114:	8fc20020 	lw	v0,32(s8)
    3118:	dfc60000 	ld	a2,0(s8)
    311c:	dfc50010 	ld	a1,16(s8)
    3120:	00402025 	move	a0,v0
    3124:	df828248 	ld	v0,-32184(gp)
    3128:	0040c825 	move	t9,v0
    312c:	0320f809 	jalr	t9
    3130:	00000000 	nop
    3134:	afc20008 	sw	v0,8(s8)
    3138:	8fc20008 	lw	v0,8(s8)
    313c:	1c40001d 	bgtz	v0,31b4 <main+0x1ae4>
    3140:	00000000 	nop
    3144:	df8281e8 	ld	v0,-32280(gp)
    3148:	0040c825 	move	t9,v0
    314c:	0320f809 	jalr	t9
    3150:	00000000 	nop
    3154:	8c430000 	lw	v1,0(v0)
    3158:	24020004 	li	v0,4
    315c:	10620009 	beq	v1,v0,3184 <main+0x1ab4>
    3160:	00000000 	nop
    3164:	df8281e8 	ld	v0,-32280(gp)
    3168:	0040c825 	move	t9,v0
    316c:	0320f809 	jalr	t9
    3170:	00000000 	nop
    3174:	8c430000 	lw	v1,0(v0)
    3178:	2402000b 	li	v0,11
    317c:	14620004 	bne	v1,v0,3190 <main+0x1ac0>
    3180:	00000000 	nop
    3184:	afc00008 	sw	zero,8(s8)
    3188:	1000000a 	b	31b4 <main+0x1ae4>
    318c:	00000000 	nop
    3190:	df828058 	ld	v0,-32680(gp)
    3194:	64446e80 	daddiu	a0,v0,28288
    3198:	df828270 	ld	v0,-32144(gp)
    319c:	0040c825 	move	t9,v0
    31a0:	0320f809 	jalr	t9
    31a4:	00000000 	nop
    31a8:	2402ffff 	li	v0,-1
    31ac:	1000000d 	b	31e4 <main+0x1b14>
    31b0:	00000000 	nop
    31b4:	8fc20008 	lw	v0,8(s8)
    31b8:	dfc30000 	ld	v1,0(s8)
    31bc:	0062102f 	dsubu	v0,v1,v0
    31c0:	ffc20000 	sd	v0,0(s8)
    31c4:	8fc20008 	lw	v0,8(s8)
    31c8:	dfc30010 	ld	v1,16(s8)
    31cc:	0062102d 	daddu	v0,v1,v0
    31d0:	ffc20010 	sd	v0,16(s8)
    31d4:	dfc20000 	ld	v0,0(s8)
    31d8:	1440ffce 	bnez	v0,3114 <main+0x1a44>
    31dc:	00000000 	nop
    31e0:	8fc20034 	lw	v0,52(s8)
    31e4:	03c0e825 	move	sp,s8
    31e8:	dfbf0058 	ld	ra,88(sp)
    31ec:	dfbe0050 	ld	s8,80(sp)
    31f0:	dfbc0048 	ld	gp,72(sp)
    31f4:	67bd0060 	daddiu	sp,sp,96
    31f8:	03e00008 	jr	ra
    31fc:	00000000 	nop
    3200:	67bdfef0 	daddiu	sp,sp,-272
    3204:	ffbf0108 	sd	ra,264(sp)
    3208:	ffbe0100 	sd	s8,256(sp)
    320c:	ffbc00f8 	sd	gp,248(sp)
    3210:	03a0f025 	move	s8,sp
    3214:	3c1c0002 	lui	gp,0x2
    3218:	0399e02d 	daddu	gp,gp,t9
    321c:	679c4e50 	daddiu	gp,gp,20048
    3220:	ffc400e0 	sd	a0,224(s8)
    3224:	dfc400e0 	ld	a0,224(s8)
    3228:	df8280c0 	ld	v0,-32576(gp)
    322c:	0040c825 	move	t9,v0
    3230:	0411f9af 	bal	18f0 <main+0x220>
    3234:	00000000 	nop
    3238:	14400004 	bnez	v0,324c <main+0x1b7c>
    323c:	00000000 	nop
    3240:	24020001 	li	v0,1
    3244:	1000015d 	b	37bc <main+0x20ec>
    3248:	00000000 	nop
    324c:	ffc00038 	sd	zero,56(s8)
    3250:	67c20038 	daddiu	v0,s8,56
    3254:	00402825 	move	a1,v0
    3258:	dfc400e0 	ld	a0,224(s8)
    325c:	df8280c8 	ld	v0,-32568(gp)
    3260:	0040c825 	move	t9,v0
    3264:	0411fa0d 	bal	1a9c <main+0x3cc>
    3268:	00000000 	nop
    326c:	a7c20008 	sh	v0,8(s8)
    3270:	97c20008 	lhu	v0,8(s8)
    3274:	14400004 	bnez	v0,3288 <main+0x1bb8>
    3278:	00000000 	nop
    327c:	24020002 	li	v0,2
    3280:	1000014e 	b	37bc <main+0x20ec>
    3284:	00000000 	nop
    3288:	97c20008 	lhu	v0,8(s8)
    328c:	64420001 	daddiu	v0,v0,1
    3290:	00402025 	move	a0,v0
    3294:	df828260 	ld	v0,-32160(gp)
    3298:	0040c825 	move	t9,v0
    329c:	0320f809 	jalr	t9
    32a0:	00000000 	nop
    32a4:	ffc20010 	sd	v0,16(s8)
    32a8:	dfc20010 	ld	v0,16(s8)
    32ac:	14400004 	bnez	v0,32c0 <main+0x1bf0>
    32b0:	00000000 	nop
    32b4:	24020003 	li	v0,3
    32b8:	10000140 	b	37bc <main+0x20ec>
    32bc:	00000000 	nop
    32c0:	97c20008 	lhu	v0,8(s8)
    32c4:	64420001 	daddiu	v0,v0,1
    32c8:	00403025 	move	a2,v0
    32cc:	00002825 	move	a1,zero
    32d0:	dfc40010 	ld	a0,16(s8)
    32d4:	df8281f8 	ld	v0,-32264(gp)
    32d8:	0040c825 	move	t9,v0
    32dc:	0320f809 	jalr	t9
    32e0:	00000000 	nop
    32e4:	dfc20038 	ld	v0,56(s8)
    32e8:	97c30008 	lhu	v1,8(s8)
    32ec:	00603025 	move	a2,v1
    32f0:	00402825 	move	a1,v0
    32f4:	dfc40010 	ld	a0,16(s8)
    32f8:	df828280 	ld	v0,-32128(gp)
    32fc:	0040c825 	move	t9,v0
    3300:	0320f809 	jalr	t9
    3304:	00000000 	nop
    3308:	97c20008 	lhu	v0,8(s8)
    330c:	00403025 	move	a2,v0
    3310:	df828058 	ld	v0,-32680(gp)
    3314:	64456e88 	daddiu	a1,v0,28296
    3318:	dfc40010 	ld	a0,16(s8)
    331c:	df828218 	ld	v0,-32232(gp)
    3320:	0040c825 	move	t9,v0
    3324:	0320f809 	jalr	t9
    3328:	00000000 	nop
    332c:	1040000c 	beqz	v0,3360 <main+0x1c90>
    3330:	00000000 	nop
    3334:	dfc20010 	ld	v0,16(s8)
    3338:	10400006 	beqz	v0,3354 <main+0x1c84>
    333c:	00000000 	nop
    3340:	dfc40010 	ld	a0,16(s8)
    3344:	df8281d0 	ld	v0,-32304(gp)
    3348:	0040c825 	move	t9,v0
    334c:	0320f809 	jalr	t9
    3350:	00000000 	nop
    3354:	24020002 	li	v0,2
    3358:	10000118 	b	37bc <main+0x20ec>
    335c:	00000000 	nop
    3360:	ffc00040 	sd	zero,64(s8)
    3364:	67c20040 	daddiu	v0,s8,64
    3368:	00402825 	move	a1,v0
    336c:	dfc400e0 	ld	a0,224(s8)
    3370:	df8280d0 	ld	v0,-32560(gp)
    3374:	0040c825 	move	t9,v0
    3378:	0411fa06 	bal	1b94 <main+0x4c4>
    337c:	00000000 	nop
    3380:	a7c20018 	sh	v0,24(s8)
    3384:	97c20018 	lhu	v0,24(s8)
    3388:	14400004 	bnez	v0,339c <main+0x1ccc>
    338c:	00000000 	nop
    3390:	24020004 	li	v0,4
    3394:	10000109 	b	37bc <main+0x20ec>
    3398:	00000000 	nop
    339c:	97c20018 	lhu	v0,24(s8)
    33a0:	64420001 	daddiu	v0,v0,1
    33a4:	00402025 	move	a0,v0
    33a8:	df828260 	ld	v0,-32160(gp)
    33ac:	0040c825 	move	t9,v0
    33b0:	0320f809 	jalr	t9
    33b4:	00000000 	nop
    33b8:	ffc20020 	sd	v0,32(s8)
    33bc:	dfc20020 	ld	v0,32(s8)
    33c0:	1440000c 	bnez	v0,33f4 <main+0x1d24>
    33c4:	00000000 	nop
    33c8:	dfc20010 	ld	v0,16(s8)
    33cc:	10400006 	beqz	v0,33e8 <main+0x1d18>
    33d0:	00000000 	nop
    33d4:	dfc40010 	ld	a0,16(s8)
    33d8:	df8281d0 	ld	v0,-32304(gp)
    33dc:	0040c825 	move	t9,v0
    33e0:	0320f809 	jalr	t9
    33e4:	00000000 	nop
    33e8:	24020003 	li	v0,3
    33ec:	100000f3 	b	37bc <main+0x20ec>
    33f0:	00000000 	nop
    33f4:	97c20018 	lhu	v0,24(s8)
    33f8:	64420001 	daddiu	v0,v0,1
    33fc:	00403025 	move	a2,v0
    3400:	00002825 	move	a1,zero
    3404:	dfc40020 	ld	a0,32(s8)
    3408:	df8281f8 	ld	v0,-32264(gp)
    340c:	0040c825 	move	t9,v0
    3410:	0320f809 	jalr	t9
    3414:	00000000 	nop
    3418:	dfc20040 	ld	v0,64(s8)
    341c:	97c30018 	lhu	v1,24(s8)
    3420:	00603025 	move	a2,v1
    3424:	00402825 	move	a1,v0
    3428:	dfc40020 	ld	a0,32(s8)
    342c:	df828280 	ld	v0,-32128(gp)
    3430:	0040c825 	move	t9,v0
    3434:	0320f809 	jalr	t9
    3438:	00000000 	nop
    343c:	ffc00048 	sd	zero,72(s8)
    3440:	67c20048 	daddiu	v0,s8,72
    3444:	00402825 	move	a1,v0
    3448:	dfc400e0 	ld	a0,224(s8)
    344c:	df8280d8 	ld	v0,-32552(gp)
    3450:	0040c825 	move	t9,v0
    3454:	0411fa24 	bal	1ce8 <main+0x618>
    3458:	00000000 	nop
    345c:	a7c20028 	sh	v0,40(s8)
    3460:	97c20028 	lhu	v0,40(s8)
    3464:	14400004 	bnez	v0,3478 <main+0x1da8>
    3468:	00000000 	nop
    346c:	24020004 	li	v0,4
    3470:	100000d2 	b	37bc <main+0x20ec>
    3474:	00000000 	nop
    3478:	97c20028 	lhu	v0,40(s8)
    347c:	64420001 	daddiu	v0,v0,1
    3480:	00402025 	move	a0,v0
    3484:	df828260 	ld	v0,-32160(gp)
    3488:	0040c825 	move	t9,v0
    348c:	0320f809 	jalr	t9
    3490:	00000000 	nop
    3494:	ffc20030 	sd	v0,48(s8)
    3498:	dfc20030 	ld	v0,48(s8)
    349c:	14400014 	bnez	v0,34f0 <main+0x1e20>
    34a0:	00000000 	nop
    34a4:	dfc20010 	ld	v0,16(s8)
    34a8:	10400006 	beqz	v0,34c4 <main+0x1df4>
    34ac:	00000000 	nop
    34b0:	dfc40010 	ld	a0,16(s8)
    34b4:	df8281d0 	ld	v0,-32304(gp)
    34b8:	0040c825 	move	t9,v0
    34bc:	0320f809 	jalr	t9
    34c0:	00000000 	nop
    34c4:	dfc20020 	ld	v0,32(s8)
    34c8:	10400006 	beqz	v0,34e4 <main+0x1e14>
    34cc:	00000000 	nop
    34d0:	dfc40020 	ld	a0,32(s8)
    34d4:	df8281d0 	ld	v0,-32304(gp)
    34d8:	0040c825 	move	t9,v0
    34dc:	0320f809 	jalr	t9
    34e0:	00000000 	nop
    34e4:	24020003 	li	v0,3
    34e8:	100000b4 	b	37bc <main+0x20ec>
    34ec:	00000000 	nop
    34f0:	97c20028 	lhu	v0,40(s8)
    34f4:	64420001 	daddiu	v0,v0,1
    34f8:	00403025 	move	a2,v0
    34fc:	00002825 	move	a1,zero
    3500:	dfc40030 	ld	a0,48(s8)
    3504:	df8281f8 	ld	v0,-32264(gp)
    3508:	0040c825 	move	t9,v0
    350c:	0320f809 	jalr	t9
    3510:	00000000 	nop
    3514:	dfc20048 	ld	v0,72(s8)
    3518:	97c30028 	lhu	v1,40(s8)
    351c:	00603025 	move	a2,v1
    3520:	00402825 	move	a1,v0
    3524:	dfc40030 	ld	a0,48(s8)
    3528:	df828280 	ld	v0,-32128(gp)
    352c:	0040c825 	move	t9,v0
    3530:	0320f809 	jalr	t9
    3534:	00000000 	nop
    3538:	67c20050 	daddiu	v0,s8,80
    353c:	24060011 	li	a2,17
    3540:	00002825 	move	a1,zero
    3544:	00402025 	move	a0,v0
    3548:	df8281f8 	ld	v0,-32264(gp)
    354c:	0040c825 	move	t9,v0
    3550:	0320f809 	jalr	t9
    3554:	00000000 	nop
    3558:	67c20068 	daddiu	v0,s8,104
    355c:	24060011 	li	a2,17
    3560:	00002825 	move	a1,zero
    3564:	00402025 	move	a0,v0
    3568:	df8281f8 	ld	v0,-32264(gp)
    356c:	0040c825 	move	t9,v0
    3570:	0320f809 	jalr	t9
    3574:	00000000 	nop
    3578:	67c30068 	daddiu	v1,s8,104
    357c:	24060010 	li	a2,16
    3580:	df828058 	ld	v0,-32680(gp)
    3584:	64456e98 	daddiu	a1,v0,28312
    3588:	00602025 	move	a0,v1
    358c:	df828280 	ld	v0,-32128(gp)
    3590:	0040c825 	move	t9,v0
    3594:	0320f809 	jalr	t9
    3598:	00000000 	nop
    359c:	67c20080 	daddiu	v0,s8,128
    35a0:	00402025 	move	a0,v0
    35a4:	df8280e0 	ld	v0,-32544(gp)
    35a8:	0040c825 	move	t9,v0
    35ac:	04110548 	bal	4ad0 <main+0x3400>
    35b0:	00000000 	nop
    35b4:	97c20028 	lhu	v0,40(s8)
    35b8:	67c30080 	daddiu	v1,s8,128
    35bc:	00403025 	move	a2,v0
    35c0:	dfc50030 	ld	a1,48(s8)
    35c4:	00602025 	move	a0,v1
    35c8:	df8280e8 	ld	v0,-32536(gp)
    35cc:	0040c825 	move	t9,v0
    35d0:	0411055d 	bal	4b48 <main+0x3478>
    35d4:	00000000 	nop
    35d8:	67c30050 	daddiu	v1,s8,80
    35dc:	67c20080 	daddiu	v0,s8,128
    35e0:	00602825 	move	a1,v1
    35e4:	00402025 	move	a0,v0
    35e8:	df8280f0 	ld	v0,-32528(gp)
    35ec:	0040c825 	move	t9,v0
    35f0:	041105dc 	bal	4d64 <main+0x3694>
    35f4:	00000000 	nop
    35f8:	afc00000 	sw	zero,0(s8)
    35fc:	1000000e 	b	3638 <main+0x1f68>
    3600:	00000000 	nop
    3604:	8fc20000 	lw	v0,0(s8)
    3608:	dfc30020 	ld	v1,32(s8)
    360c:	0062102d 	daddu	v0,v1,v0
    3610:	90430000 	lbu	v1,0(v0)
    3614:	8fc20000 	lw	v0,0(s8)
    3618:	dfc40020 	ld	a0,32(s8)
    361c:	0082102d 	daddu	v0,a0,v0
    3620:	3863001d 	xori	v1,v1,0x1d
    3624:	306300ff 	andi	v1,v1,0xff
    3628:	a0430000 	sb	v1,0(v0)
    362c:	8fc20000 	lw	v0,0(s8)
    3630:	24420001 	addiu	v0,v0,1
    3634:	afc20000 	sw	v0,0(s8)
    3638:	97c20018 	lhu	v0,24(s8)
    363c:	8fc30000 	lw	v1,0(s8)
    3640:	0062102a 	slt	v0,v1,v0
    3644:	1440ffef 	bnez	v0,3604 <main+0x1f34>
    3648:	00000000 	nop
    364c:	afc00004 	sw	zero,4(s8)
    3650:	1000000c 	b	3684 <main+0x1fb4>
    3654:	00000000 	nop
    3658:	8fc20004 	lw	v0,4(s8)
    365c:	03c2102d 	daddu	v0,s8,v0
    3660:	90420068 	lbu	v0,104(v0)
    3664:	38420059 	xori	v0,v0,0x59
    3668:	304200ff 	andi	v0,v0,0xff
    366c:	8fc30004 	lw	v1,4(s8)
    3670:	03c3182d 	daddu	v1,s8,v1
    3674:	a0620068 	sb	v0,104(v1)
    3678:	8fc20004 	lw	v0,4(s8)
    367c:	24420001 	addiu	v0,v0,1
    3680:	afc20004 	sw	v0,4(s8)
    3684:	8fc20004 	lw	v0,4(s8)
    3688:	28420010 	slti	v0,v0,16
    368c:	1440fff2 	bnez	v0,3658 <main+0x1f88>
    3690:	00000000 	nop
    3694:	97c20018 	lhu	v0,24(s8)
    3698:	00403025 	move	a2,v0
    369c:	df828058 	ld	v0,-32680(gp)
    36a0:	64456eb0 	daddiu	a1,v0,28336
    36a4:	dfc40020 	ld	a0,32(s8)
    36a8:	df828220 	ld	v0,-32224(gp)
    36ac:	0040c825 	move	t9,v0
    36b0:	0320f809 	jalr	t9
    36b4:	00000000 	nop
    36b8:	1440000c 	bnez	v0,36ec <main+0x201c>
    36bc:	00000000 	nop
    36c0:	67c30068 	daddiu	v1,s8,104
    36c4:	67c20050 	daddiu	v0,s8,80
    36c8:	24060010 	li	a2,16
    36cc:	00602825 	move	a1,v1
    36d0:	00402025 	move	a0,v0
    36d4:	df828220 	ld	v0,-32224(gp)
    36d8:	0040c825 	move	t9,v0
    36dc:	0320f809 	jalr	t9
    36e0:	00000000 	nop
    36e4:	1040001c 	beqz	v0,3758 <main+0x2088>
    36e8:	00000000 	nop
    36ec:	dfc20010 	ld	v0,16(s8)
    36f0:	10400006 	beqz	v0,370c <main+0x203c>
    36f4:	00000000 	nop
    36f8:	dfc40010 	ld	a0,16(s8)
    36fc:	df8281d0 	ld	v0,-32304(gp)
    3700:	0040c825 	move	t9,v0
    3704:	0320f809 	jalr	t9
    3708:	00000000 	nop
    370c:	dfc20020 	ld	v0,32(s8)
    3710:	10400006 	beqz	v0,372c <main+0x205c>
    3714:	00000000 	nop
    3718:	dfc40020 	ld	a0,32(s8)
    371c:	df8281d0 	ld	v0,-32304(gp)
    3720:	0040c825 	move	t9,v0
    3724:	0320f809 	jalr	t9
    3728:	00000000 	nop
    372c:	dfc20030 	ld	v0,48(s8)
    3730:	10400006 	beqz	v0,374c <main+0x207c>
    3734:	00000000 	nop
    3738:	dfc40030 	ld	a0,48(s8)
    373c:	df8281d0 	ld	v0,-32304(gp)
    3740:	0040c825 	move	t9,v0
    3744:	0320f809 	jalr	t9
    3748:	00000000 	nop
    374c:	24020005 	li	v0,5
    3750:	1000001a 	b	37bc <main+0x20ec>
    3754:	00000000 	nop
    3758:	dfc20010 	ld	v0,16(s8)
    375c:	10400006 	beqz	v0,3778 <main+0x20a8>
    3760:	00000000 	nop
    3764:	dfc40010 	ld	a0,16(s8)
    3768:	df8281d0 	ld	v0,-32304(gp)
    376c:	0040c825 	move	t9,v0
    3770:	0320f809 	jalr	t9
    3774:	00000000 	nop
    3778:	dfc20020 	ld	v0,32(s8)
    377c:	10400006 	beqz	v0,3798 <main+0x20c8>
    3780:	00000000 	nop
    3784:	dfc40020 	ld	a0,32(s8)
    3788:	df8281d0 	ld	v0,-32304(gp)
    378c:	0040c825 	move	t9,v0
    3790:	0320f809 	jalr	t9
    3794:	00000000 	nop
    3798:	dfc20030 	ld	v0,48(s8)
    379c:	10400006 	beqz	v0,37b8 <main+0x20e8>
    37a0:	00000000 	nop
    37a4:	dfc40030 	ld	a0,48(s8)
    37a8:	df8281d0 	ld	v0,-32304(gp)
    37ac:	0040c825 	move	t9,v0
    37b0:	0320f809 	jalr	t9
    37b4:	00000000 	nop
    37b8:	00001025 	move	v0,zero
    37bc:	03c0e825 	move	sp,s8
    37c0:	dfbf0108 	ld	ra,264(sp)
    37c4:	dfbe0100 	ld	s8,256(sp)
    37c8:	dfbc00f8 	ld	gp,248(sp)
    37cc:	67bd0110 	daddiu	sp,sp,272
    37d0:	03e00008 	jr	ra
    37d4:	00000000 	nop
    37d8:	67bdffc0 	daddiu	sp,sp,-64
    37dc:	ffbf0038 	sd	ra,56(sp)
    37e0:	ffbe0030 	sd	s8,48(sp)
    37e4:	ffbc0028 	sd	gp,40(sp)
    37e8:	03a0f025 	move	s8,sp
    37ec:	3c1c0002 	lui	gp,0x2
    37f0:	0399e02d 	daddu	gp,gp,t9
    37f4:	679c4878 	daddiu	gp,gp,18552
    37f8:	00801025 	move	v0,a0
    37fc:	00021000 	sll	v0,v0,0x0
    3800:	afc20010 	sw	v0,16(s8)
    3804:	df8280b8 	ld	v0,-32584(gp)
    3808:	dc420000 	ld	v0,0(v0)
    380c:	ffc20000 	sd	v0,0(s8)
    3810:	df8380f8 	ld	v1,-32520(gp)
    3814:	9fc20010 	lwu	v0,16(s8)
    3818:	00021178 	dsll	v0,v0,0x5
    381c:	0062102d 	daddu	v0,v1,v0
    3820:	94430008 	lhu	v1,8(v0)
    3824:	2402000c 	li	v0,12
    3828:	1462007a 	bne	v1,v0,3a14 <main+0x2344>
    382c:	00000000 	nop
    3830:	df8380f8 	ld	v1,-32520(gp)
    3834:	9fc20010 	lwu	v0,16(s8)
    3838:	00021178 	dsll	v0,v0,0x5
    383c:	0062102d 	daddu	v0,v1,v0
    3840:	dc430000 	ld	v1,0(v0)
    3844:	2406000c 	li	a2,12
    3848:	df828058 	ld	v0,-32680(gp)
    384c:	64456ec0 	daddiu	a1,v0,28352
    3850:	00602025 	move	a0,v1
    3854:	df828218 	ld	v0,-32232(gp)
    3858:	0040c825 	move	t9,v0
    385c:	0320f809 	jalr	t9
    3860:	00000000 	nop
    3864:	1440006b 	bnez	v0,3a14 <main+0x2344>
    3868:	00000000 	nop
    386c:	df8380f8 	ld	v1,-32520(gp)
    3870:	9fc20010 	lwu	v0,16(s8)
    3874:	00021178 	dsll	v0,v0,0x5
    3878:	0062102d 	daddu	v0,v1,v0
    387c:	94420008 	lhu	v0,8(v0)
    3880:	00401825 	move	v1,v0
    3884:	df8480f8 	ld	a0,-32520(gp)
    3888:	9fc20010 	lwu	v0,16(s8)
    388c:	00021178 	dsll	v0,v0,0x5
    3890:	0082102d 	daddu	v0,a0,v0
    3894:	94420018 	lhu	v0,24(v0)
    3898:	00621021 	addu	v0,v1,v0
    389c:	00402025 	move	a0,v0
    38a0:	df828260 	ld	v0,-32160(gp)
    38a4:	0040c825 	move	t9,v0
    38a8:	0320f809 	jalr	t9
    38ac:	00000000 	nop
    38b0:	ffc20008 	sd	v0,8(s8)
    38b4:	dfc40008 	ld	a0,8(s8)
    38b8:	df8281d0 	ld	v0,-32304(gp)
    38bc:	0040c825 	move	t9,v0
    38c0:	0320f809 	jalr	t9
    38c4:	00000000 	nop
    38c8:	ffc00008 	sd	zero,8(s8)
    38cc:	df8380f8 	ld	v1,-32520(gp)
    38d0:	9fc20010 	lwu	v0,16(s8)
    38d4:	00021178 	dsll	v0,v0,0x5
    38d8:	0062102d 	daddu	v0,v1,v0
    38dc:	94420018 	lhu	v0,24(v0)
    38e0:	10400013 	beqz	v0,3930 <main+0x2260>
    38e4:	00000000 	nop
    38e8:	df8380f8 	ld	v1,-32520(gp)
    38ec:	9fc20010 	lwu	v0,16(s8)
    38f0:	00021178 	dsll	v0,v0,0x5
    38f4:	0062102d 	daddu	v0,v1,v0
    38f8:	94420018 	lhu	v0,24(v0)
    38fc:	2c420021 	sltiu	v0,v0,33
    3900:	1040000b 	beqz	v0,3930 <main+0x2260>
    3904:	00000000 	nop
    3908:	df8380f8 	ld	v1,-32520(gp)
    390c:	9fc20010 	lwu	v0,16(s8)
    3910:	00021178 	dsll	v0,v0,0x5
    3914:	0062102d 	daddu	v0,v1,v0
    3918:	dc420010 	ld	v0,16(v0)
    391c:	00402025 	move	a0,v0
    3920:	df8281d0 	ld	v0,-32304(gp)
    3924:	0040c825 	move	t9,v0
    3928:	0320f809 	jalr	t9
    392c:	00000000 	nop
    3930:	dfc20000 	ld	v0,0(s8)
    3934:	90430002 	lbu	v1,2(v0)
    3938:	24020001 	li	v0,1
    393c:	14620019 	bne	v1,v0,39a4 <main+0x22d4>
    3940:	00000000 	nop
    3944:	dfc20000 	ld	v0,0(s8)
    3948:	90430003 	lbu	v1,3(v0)
    394c:	24020006 	li	v0,6
    3950:	14620014 	bne	v1,v0,39a4 <main+0x22d4>
    3954:	00000000 	nop
    3958:	df8380f8 	ld	v1,-32520(gp)
    395c:	9fc20010 	lwu	v0,16(s8)
    3960:	00021178 	dsll	v0,v0,0x5
    3964:	0062102d 	daddu	v0,v1,v0
    3968:	dc440010 	ld	a0,16(v0)
    396c:	df8380f8 	ld	v1,-32520(gp)
    3970:	9fc20010 	lwu	v0,16(s8)
    3974:	00021178 	dsll	v0,v0,0x5
    3978:	0062102d 	daddu	v0,v1,v0
    397c:	94420018 	lhu	v0,24(v0)
    3980:	00003825 	move	a3,zero
    3984:	00403025 	move	a2,v0
    3988:	00802825 	move	a1,a0
    398c:	df828058 	ld	v0,-32680(gp)
    3990:	64446ec0 	daddiu	a0,v0,28352
    3994:	df828100 	ld	v0,-32512(gp)
    3998:	0040c825 	move	t9,v0
    399c:	0411faf9 	bal	2584 <main+0xeb4>
    39a0:	00000000 	nop
    39a4:	df8380f8 	ld	v1,-32520(gp)
    39a8:	9fc20010 	lwu	v0,16(s8)
    39ac:	00021178 	dsll	v0,v0,0x5
    39b0:	0062102d 	daddu	v0,v1,v0
    39b4:	94420018 	lhu	v0,24(v0)
    39b8:	2c420021 	sltiu	v0,v0,33
    39bc:	1440000b 	bnez	v0,39ec <main+0x231c>
    39c0:	00000000 	nop
    39c4:	df8380f8 	ld	v1,-32520(gp)
    39c8:	9fc20010 	lwu	v0,16(s8)
    39cc:	00021178 	dsll	v0,v0,0x5
    39d0:	0062102d 	daddu	v0,v1,v0
    39d4:	dc420010 	ld	v0,16(v0)
    39d8:	00402025 	move	a0,v0
    39dc:	df8281d0 	ld	v0,-32304(gp)
    39e0:	0040c825 	move	t9,v0
    39e4:	0320f809 	jalr	t9
    39e8:	00000000 	nop
    39ec:	df8380f8 	ld	v1,-32520(gp)
    39f0:	9fc20010 	lwu	v0,16(s8)
    39f4:	00021178 	dsll	v0,v0,0x5
    39f8:	0062102d 	daddu	v0,v1,v0
    39fc:	fc400010 	sd	zero,16(v0)
    3a00:	df8380f8 	ld	v1,-32520(gp)
    3a04:	9fc20010 	lwu	v0,16(s8)
    3a08:	00021178 	dsll	v0,v0,0x5
    3a0c:	0062102d 	daddu	v0,v1,v0
    3a10:	a4400018 	sh	zero,24(v0)
    3a14:	00000000 	nop
    3a18:	03c0e825 	move	sp,s8
    3a1c:	dfbf0038 	ld	ra,56(sp)
    3a20:	dfbe0030 	ld	s8,48(sp)
    3a24:	dfbc0028 	ld	gp,40(sp)
    3a28:	67bd0040 	daddiu	sp,sp,64
    3a2c:	03e00008 	jr	ra
    3a30:	00000000 	nop
    3a34:	67bdff90 	daddiu	sp,sp,-112
    3a38:	ffbf0068 	sd	ra,104(sp)
    3a3c:	ffbe0060 	sd	s8,96(sp)
    3a40:	ffbc0058 	sd	gp,88(sp)
    3a44:	03a0f025 	move	s8,sp
    3a48:	3c1c0002 	lui	gp,0x2
    3a4c:	0399e02d 	daddu	gp,gp,t9
    3a50:	679c461c 	daddiu	gp,gp,17948
    3a54:	ffc40040 	sd	a0,64(s8)
    3a58:	dfc20040 	ld	v0,64(s8)
    3a5c:	90420000 	lbu	v0,0(v0)
    3a60:	00021043 	sra	v0,v0,0x1
    3a64:	304200ff 	andi	v0,v0,0xff
    3a68:	30420003 	andi	v0,v0,0x3
    3a6c:	a3c20004 	sb	v0,4(s8)
    3a70:	93c20004 	lbu	v0,4(s8)
    3a74:	1040003f 	beqz	v0,3b74 <main+0x24a4>
    3a78:	00000000 	nop
    3a7c:	93c30004 	lbu	v1,4(s8)
    3a80:	24020001 	li	v0,1
    3a84:	1462001d 	bne	v1,v0,3afc <main+0x242c>
    3a88:	00000000 	nop
    3a8c:	dfc40040 	ld	a0,64(s8)
    3a90:	df8280b0 	ld	v0,-32592(gp)
    3a94:	0040c825 	move	t9,v0
    3a98:	0411f8ff 	bal	1e98 <main+0x7c8>
    3a9c:	00000000 	nop
    3aa0:	a7c20008 	sh	v0,8(s8)
    3aa4:	24020040 	li	v0,64
    3aa8:	a3c20030 	sb	v0,48(s8)
    3aac:	24020002 	li	v0,2
    3ab0:	a3c20031 	sb	v0,49(s8)
    3ab4:	97c20008 	lhu	v0,8(s8)
    3ab8:	00021202 	srl	v0,v0,0x8
    3abc:	3042ffff 	andi	v0,v0,0xffff
    3ac0:	304200ff 	andi	v0,v0,0xff
    3ac4:	a3c20032 	sb	v0,50(s8)
    3ac8:	97c20008 	lhu	v0,8(s8)
    3acc:	304200ff 	andi	v0,v0,0xff
    3ad0:	a3c20033 	sb	v0,51(s8)
    3ad4:	67c20030 	daddiu	v0,s8,48
    3ad8:	24060004 	li	a2,4
    3adc:	00402825 	move	a1,v0
    3ae0:	24040001 	li	a0,1
    3ae4:	df8280a8 	ld	v0,-32600(gp)
    3ae8:	0040c825 	move	t9,v0
    3aec:	0411fd76 	bal	30c8 <main+0x19f8>
    3af0:	00000000 	nop
    3af4:	1000001f 	b	3b74 <main+0x24a4>
    3af8:	00000000 	nop
    3afc:	93c30004 	lbu	v1,4(s8)
    3b00:	24020002 	li	v0,2
    3b04:	146200ca 	bne	v1,v0,3e30 <main+0x2760>
    3b08:	00000000 	nop
    3b0c:	dfc40040 	ld	a0,64(s8)
    3b10:	df8280b0 	ld	v0,-32592(gp)
    3b14:	0040c825 	move	t9,v0
    3b18:	0411f8df 	bal	1e98 <main+0x7c8>
    3b1c:	00000000 	nop
    3b20:	a7c20006 	sh	v0,6(s8)
    3b24:	24020050 	li	v0,80
    3b28:	a3c20038 	sb	v0,56(s8)
    3b2c:	24020002 	li	v0,2
    3b30:	a3c20039 	sb	v0,57(s8)
    3b34:	97c20006 	lhu	v0,6(s8)
    3b38:	00021202 	srl	v0,v0,0x8
    3b3c:	3042ffff 	andi	v0,v0,0xffff
    3b40:	304200ff 	andi	v0,v0,0xff
    3b44:	a3c2003a 	sb	v0,58(s8)
    3b48:	97c20006 	lhu	v0,6(s8)
    3b4c:	304200ff 	andi	v0,v0,0xff
    3b50:	a3c2003b 	sb	v0,59(s8)
    3b54:	67c20038 	daddiu	v0,s8,56
    3b58:	24060004 	li	a2,4
    3b5c:	00402825 	move	a1,v0
    3b60:	24040001 	li	a0,1
    3b64:	df8280a8 	ld	v0,-32600(gp)
    3b68:	0040c825 	move	t9,v0
    3b6c:	0411fd56 	bal	30c8 <main+0x19f8>
    3b70:	00000000 	nop
    3b74:	ffc00020 	sd	zero,32(s8)
    3b78:	67c20020 	daddiu	v0,s8,32
    3b7c:	00402825 	move	a1,v0
    3b80:	dfc40040 	ld	a0,64(s8)
    3b84:	df828080 	ld	v0,-32640(gp)
    3b88:	0040c825 	move	t9,v0
    3b8c:	0411f953 	bal	20dc <main+0xa0c>
    3b90:	00000000 	nop
    3b94:	a7c2000a 	sh	v0,10(s8)
    3b98:	97c2000a 	lhu	v0,10(s8)
    3b9c:	104000a7 	beqz	v0,3e3c <main+0x276c>
    3ba0:	00000000 	nop
    3ba4:	afc00000 	sw	zero,0(s8)
    3ba8:	afc00000 	sw	zero,0(s8)
    3bac:	1000001b 	b	3c1c <main+0x254c>
    3bb0:	00000000 	nop
    3bb4:	df8380f8 	ld	v1,-32520(gp)
    3bb8:	9fc20000 	lwu	v0,0(s8)
    3bbc:	00021178 	dsll	v0,v0,0x5
    3bc0:	0062102d 	daddu	v0,v1,v0
    3bc4:	94430008 	lhu	v1,8(v0)
    3bc8:	97c2000a 	lhu	v0,10(s8)
    3bcc:	14430010 	bne	v0,v1,3c10 <main+0x2540>
    3bd0:	00000000 	nop
    3bd4:	dfc40020 	ld	a0,32(s8)
    3bd8:	df8380f8 	ld	v1,-32520(gp)
    3bdc:	9fc20000 	lwu	v0,0(s8)
    3be0:	00021178 	dsll	v0,v0,0x5
    3be4:	0062102d 	daddu	v0,v1,v0
    3be8:	dc420000 	ld	v0,0(v0)
    3bec:	97c3000a 	lhu	v1,10(s8)
    3bf0:	00603025 	move	a2,v1
    3bf4:	00402825 	move	a1,v0
    3bf8:	df828218 	ld	v0,-32232(gp)
    3bfc:	0040c825 	move	t9,v0
    3c00:	0320f809 	jalr	t9
    3c04:	00000000 	nop
    3c08:	1040000a 	beqz	v0,3c34 <main+0x2564>
    3c0c:	00000000 	nop
    3c10:	8fc20000 	lw	v0,0(s8)
    3c14:	24420001 	addiu	v0,v0,1
    3c18:	afc20000 	sw	v0,0(s8)
    3c1c:	8fc20000 	lw	v0,0(s8)
    3c20:	2c42000e 	sltiu	v0,v0,14
    3c24:	1440ffe3 	bnez	v0,3bb4 <main+0x24e4>
    3c28:	00000000 	nop
    3c2c:	10000002 	b	3c38 <main+0x2568>
    3c30:	00000000 	nop
    3c34:	00000000 	nop
    3c38:	8fc30000 	lw	v1,0(s8)
    3c3c:	2402000e 	li	v0,14
    3c40:	10620081 	beq	v1,v0,3e48 <main+0x2778>
    3c44:	00000000 	nop
    3c48:	ffc00028 	sd	zero,40(s8)
    3c4c:	67c20028 	daddiu	v0,s8,40
    3c50:	00402825 	move	a1,v0
    3c54:	dfc40040 	ld	a0,64(s8)
    3c58:	df828088 	ld	v0,-32632(gp)
    3c5c:	0040c825 	move	t9,v0
    3c60:	0411f982 	bal	226c <main+0xb9c>
    3c64:	00000000 	nop
    3c68:	a7c2000c 	sh	v0,12(s8)
    3c6c:	97c2000c 	lhu	v0,12(s8)
    3c70:	10400078 	beqz	v0,3e54 <main+0x2784>
    3c74:	00000000 	nop
    3c78:	df8380f8 	ld	v1,-32520(gp)
    3c7c:	9fc20000 	lwu	v0,0(s8)
    3c80:	00021178 	dsll	v0,v0,0x5
    3c84:	0062102d 	daddu	v0,v1,v0
    3c88:	94420018 	lhu	v0,24(v0)
    3c8c:	97c3000c 	lhu	v1,12(s8)
    3c90:	0043102b 	sltu	v0,v0,v1
    3c94:	1040003d 	beqz	v0,3d8c <main+0x26bc>
    3c98:	00000000 	nop
    3c9c:	97c2000c 	lhu	v0,12(s8)
    3ca0:	64420001 	daddiu	v0,v0,1
    3ca4:	00402025 	move	a0,v0
    3ca8:	df828260 	ld	v0,-32160(gp)
    3cac:	0040c825 	move	t9,v0
    3cb0:	0320f809 	jalr	t9
    3cb4:	00000000 	nop
    3cb8:	ffc20018 	sd	v0,24(s8)
    3cbc:	dfc20018 	ld	v0,24(s8)
    3cc0:	10400067 	beqz	v0,3e60 <main+0x2790>
    3cc4:	00000000 	nop
    3cc8:	97c2000c 	lhu	v0,12(s8)
    3ccc:	64420001 	daddiu	v0,v0,1
    3cd0:	00403025 	move	a2,v0
    3cd4:	00002825 	move	a1,zero
    3cd8:	dfc40018 	ld	a0,24(s8)
    3cdc:	df8281f8 	ld	v0,-32264(gp)
    3ce0:	0040c825 	move	t9,v0
    3ce4:	0320f809 	jalr	t9
    3ce8:	00000000 	nop
    3cec:	dfc20028 	ld	v0,40(s8)
    3cf0:	97c3000c 	lhu	v1,12(s8)
    3cf4:	00603025 	move	a2,v1
    3cf8:	00402825 	move	a1,v0
    3cfc:	dfc40018 	ld	a0,24(s8)
    3d00:	df828280 	ld	v0,-32128(gp)
    3d04:	0040c825 	move	t9,v0
    3d08:	0320f809 	jalr	t9
    3d0c:	00000000 	nop
    3d10:	df8380f8 	ld	v1,-32520(gp)
    3d14:	9fc20000 	lwu	v0,0(s8)
    3d18:	00021178 	dsll	v0,v0,0x5
    3d1c:	0062102d 	daddu	v0,v1,v0
    3d20:	dc420010 	ld	v0,16(v0)
    3d24:	1040000b 	beqz	v0,3d54 <main+0x2684>
    3d28:	00000000 	nop
    3d2c:	df8380f8 	ld	v1,-32520(gp)
    3d30:	9fc20000 	lwu	v0,0(s8)
    3d34:	00021178 	dsll	v0,v0,0x5
    3d38:	0062102d 	daddu	v0,v1,v0
    3d3c:	dc420010 	ld	v0,16(v0)
    3d40:	00402025 	move	a0,v0
    3d44:	df8281d0 	ld	v0,-32304(gp)
    3d48:	0040c825 	move	t9,v0
    3d4c:	0320f809 	jalr	t9
    3d50:	00000000 	nop
    3d54:	df8380f8 	ld	v1,-32520(gp)
    3d58:	9fc20000 	lwu	v0,0(s8)
    3d5c:	00021178 	dsll	v0,v0,0x5
    3d60:	0062102d 	daddu	v0,v1,v0
    3d64:	dfc30018 	ld	v1,24(s8)
    3d68:	fc430010 	sd	v1,16(v0)
    3d6c:	df8380f8 	ld	v1,-32520(gp)
    3d70:	9fc20000 	lwu	v0,0(s8)
    3d74:	00021178 	dsll	v0,v0,0x5
    3d78:	0062102d 	daddu	v0,v1,v0
    3d7c:	97c3000c 	lhu	v1,12(s8)
    3d80:	a4430018 	sh	v1,24(v0)
    3d84:	10000022 	b	3e10 <main+0x2740>
    3d88:	00000000 	nop
    3d8c:	df8380f8 	ld	v1,-32520(gp)
    3d90:	9fc20000 	lwu	v0,0(s8)
    3d94:	00021178 	dsll	v0,v0,0x5
    3d98:	0062102d 	daddu	v0,v1,v0
    3d9c:	dc420010 	ld	v0,16(v0)
    3da0:	ffc20010 	sd	v0,16(s8)
    3da4:	df8380f8 	ld	v1,-32520(gp)
    3da8:	9fc20000 	lwu	v0,0(s8)
    3dac:	00021178 	dsll	v0,v0,0x5
    3db0:	0062102d 	daddu	v0,v1,v0
    3db4:	94420018 	lhu	v0,24(v0)
    3db8:	00403025 	move	a2,v0
    3dbc:	00002825 	move	a1,zero
    3dc0:	dfc40010 	ld	a0,16(s8)
    3dc4:	df8281f8 	ld	v0,-32264(gp)
    3dc8:	0040c825 	move	t9,v0
    3dcc:	0320f809 	jalr	t9
    3dd0:	00000000 	nop
    3dd4:	dfc20028 	ld	v0,40(s8)
    3dd8:	97c3000c 	lhu	v1,12(s8)
    3ddc:	00603025 	move	a2,v1
    3de0:	00402825 	move	a1,v0
    3de4:	dfc40010 	ld	a0,16(s8)
    3de8:	df828280 	ld	v0,-32128(gp)
    3dec:	0040c825 	move	t9,v0
    3df0:	0320f809 	jalr	t9
    3df4:	00000000 	nop
    3df8:	df8380f8 	ld	v1,-32520(gp)
    3dfc:	9fc20000 	lwu	v0,0(s8)
    3e00:	00021178 	dsll	v0,v0,0x5
    3e04:	0062102d 	daddu	v0,v1,v0
    3e08:	97c3000c 	lhu	v1,12(s8)
    3e0c:	a4430018 	sh	v1,24(v0)
    3e10:	8fc20000 	lw	v0,0(s8)
    3e14:	00402025 	move	a0,v0
    3e18:	df828108 	ld	v0,-32504(gp)
    3e1c:	0040c825 	move	t9,v0
    3e20:	0411fe6d 	bal	37d8 <main+0x2108>
    3e24:	00000000 	nop
    3e28:	1000000e 	b	3e64 <main+0x2794>
    3e2c:	00000000 	nop
    3e30:	00000000 	nop
    3e34:	1000000b 	b	3e64 <main+0x2794>
    3e38:	00000000 	nop
    3e3c:	00000000 	nop
    3e40:	10000008 	b	3e64 <main+0x2794>
    3e44:	00000000 	nop
    3e48:	00000000 	nop
    3e4c:	10000005 	b	3e64 <main+0x2794>
    3e50:	00000000 	nop
    3e54:	00000000 	nop
    3e58:	10000002 	b	3e64 <main+0x2794>
    3e5c:	00000000 	nop
    3e60:	00000000 	nop
    3e64:	03c0e825 	move	sp,s8
    3e68:	dfbf0068 	ld	ra,104(sp)
    3e6c:	dfbe0060 	ld	s8,96(sp)
    3e70:	dfbc0058 	ld	gp,88(sp)
    3e74:	67bd0070 	daddiu	sp,sp,112
    3e78:	03e00008 	jr	ra
    3e7c:	00000000 	nop
    3e80:	67bdffa0 	daddiu	sp,sp,-96
    3e84:	ffbf0058 	sd	ra,88(sp)
    3e88:	ffbe0050 	sd	s8,80(sp)
    3e8c:	ffbc0048 	sd	gp,72(sp)
    3e90:	03a0f025 	move	s8,sp
    3e94:	3c1c0002 	lui	gp,0x2
    3e98:	0399e02d 	daddu	gp,gp,t9
    3e9c:	679c41d0 	daddiu	gp,gp,16848
    3ea0:	ffc40030 	sd	a0,48(s8)
    3ea4:	ffc00020 	sd	zero,32(s8)
    3ea8:	67c20020 	daddiu	v0,s8,32
    3eac:	00402825 	move	a1,v0
    3eb0:	dfc40030 	ld	a0,48(s8)
    3eb4:	df828110 	ld	v0,-32496(gp)
    3eb8:	0040c825 	move	t9,v0
    3ebc:	0411f93b 	bal	23ac <main+0xcdc>
    3ec0:	00000000 	nop
    3ec4:	a7c20000 	sh	v0,0(s8)
    3ec8:	97c20000 	lhu	v0,0(s8)
    3ecc:	10400074 	beqz	v0,40a0 <main+0x29d0>
    3ed0:	00000000 	nop
    3ed4:	97c20000 	lhu	v0,0(s8)
    3ed8:	24420001 	addiu	v0,v0,1
    3edc:	a7c20008 	sh	v0,8(s8)
    3ee0:	97c20008 	lhu	v0,8(s8)
    3ee4:	24420001 	addiu	v0,v0,1
    3ee8:	00402025 	move	a0,v0
    3eec:	df828260 	ld	v0,-32160(gp)
    3ef0:	0040c825 	move	t9,v0
    3ef4:	0320f809 	jalr	t9
    3ef8:	00000000 	nop
    3efc:	ffc20010 	sd	v0,16(s8)
    3f00:	dfc20010 	ld	v0,16(s8)
    3f04:	10400069 	beqz	v0,40ac <main+0x29dc>
    3f08:	00000000 	nop
    3f0c:	97c20008 	lhu	v0,8(s8)
    3f10:	24420001 	addiu	v0,v0,1
    3f14:	00403025 	move	a2,v0
    3f18:	00002825 	move	a1,zero
    3f1c:	dfc40010 	ld	a0,16(s8)
    3f20:	df8281f8 	ld	v0,-32264(gp)
    3f24:	0040c825 	move	t9,v0
    3f28:	0320f809 	jalr	t9
    3f2c:	00000000 	nop
    3f30:	97c20000 	lhu	v0,0(s8)
    3f34:	2c420110 	sltiu	v0,v0,272
    3f38:	14400003 	bnez	v0,3f48 <main+0x2878>
    3f3c:	00000000 	nop
    3f40:	24020110 	li	v0,272
    3f44:	a7c20000 	sh	v0,0(s8)
    3f48:	dfc20020 	ld	v0,32(s8)
    3f4c:	97c30000 	lhu	v1,0(s8)
    3f50:	00603025 	move	a2,v1
    3f54:	00402825 	move	a1,v0
    3f58:	dfc40010 	ld	a0,16(s8)
    3f5c:	df828280 	ld	v0,-32128(gp)
    3f60:	0040c825 	move	t9,v0
    3f64:	0320f809 	jalr	t9
    3f68:	00000000 	nop
    3f6c:	97c30000 	lhu	v1,0(s8)
    3f70:	2402000c 	li	v0,12
    3f74:	14620013 	bne	v1,v0,3fc4 <main+0x28f4>
    3f78:	00000000 	nop
    3f7c:	2406000c 	li	a2,12
    3f80:	df828058 	ld	v0,-32680(gp)
    3f84:	64456ec0 	daddiu	a1,v0,28352
    3f88:	dfc40010 	ld	a0,16(s8)
    3f8c:	df828218 	ld	v0,-32232(gp)
    3f90:	0040c825 	move	t9,v0
    3f94:	0320f809 	jalr	t9
    3f98:	00000000 	nop
    3f9c:	14400009 	bnez	v0,3fc4 <main+0x28f4>
    3fa0:	00000000 	nop
    3fa4:	df8280a0 	ld	v0,-32608(gp)
    3fa8:	0040c825 	move	t9,v0
    3fac:	0411fc39 	bal	3094 <main+0x19c4>
    3fb0:	00000000 	nop
    3fb4:	ffc20018 	sd	v0,24(s8)
    3fb8:	dfc20018 	ld	v0,24(s8)
    3fbc:	24030001 	li	v1,1
    3fc0:	a0430002 	sb	v1,2(v0)
    3fc4:	afc00004 	sw	zero,4(s8)
    3fc8:	1000002f 	b	4088 <main+0x29b8>
    3fcc:	00000000 	nop
    3fd0:	df8380f8 	ld	v1,-32520(gp)
    3fd4:	8fc20004 	lw	v0,4(s8)
    3fd8:	00021178 	dsll	v0,v0,0x5
    3fdc:	0062102d 	daddu	v0,v1,v0
    3fe0:	dc420000 	ld	v0,0(v0)
    3fe4:	14400025 	bnez	v0,407c <main+0x29ac>
    3fe8:	00000000 	nop
    3fec:	df8380f8 	ld	v1,-32520(gp)
    3ff0:	8fc20004 	lw	v0,4(s8)
    3ff4:	00021178 	dsll	v0,v0,0x5
    3ff8:	0062102d 	daddu	v0,v1,v0
    3ffc:	94420008 	lhu	v0,8(v0)
    4000:	1440001e 	bnez	v0,407c <main+0x29ac>
    4004:	00000000 	nop
    4008:	df8380f8 	ld	v1,-32520(gp)
    400c:	8fc20004 	lw	v0,4(s8)
    4010:	00021178 	dsll	v0,v0,0x5
    4014:	0062102d 	daddu	v0,v1,v0
    4018:	dc420010 	ld	v0,16(v0)
    401c:	14400017 	bnez	v0,407c <main+0x29ac>
    4020:	00000000 	nop
    4024:	df8380f8 	ld	v1,-32520(gp)
    4028:	8fc20004 	lw	v0,4(s8)
    402c:	00021178 	dsll	v0,v0,0x5
    4030:	0062102d 	daddu	v0,v1,v0
    4034:	94420018 	lhu	v0,24(v0)
    4038:	14400010 	bnez	v0,407c <main+0x29ac>
    403c:	00000000 	nop
    4040:	df8380f8 	ld	v1,-32520(gp)
    4044:	8fc20004 	lw	v0,4(s8)
    4048:	00021178 	dsll	v0,v0,0x5
    404c:	0062102d 	daddu	v0,v1,v0
    4050:	dfc30010 	ld	v1,16(s8)
    4054:	fc430000 	sd	v1,0(v0)
    4058:	df8380f8 	ld	v1,-32520(gp)
    405c:	8fc20004 	lw	v0,4(s8)
    4060:	00021178 	dsll	v0,v0,0x5
    4064:	0062102d 	daddu	v0,v1,v0
    4068:	97c30000 	lhu	v1,0(s8)
    406c:	a4430008 	sh	v1,8(v0)
    4070:	00000000 	nop
    4074:	1000000e 	b	40b0 <main+0x29e0>
    4078:	00000000 	nop
    407c:	8fc20004 	lw	v0,4(s8)
    4080:	24420001 	addiu	v0,v0,1
    4084:	afc20004 	sw	v0,4(s8)
    4088:	8fc20004 	lw	v0,4(s8)
    408c:	2842000e 	slti	v0,v0,14
    4090:	1440ffcf 	bnez	v0,3fd0 <main+0x2900>
    4094:	00000000 	nop
    4098:	10000005 	b	40b0 <main+0x29e0>
    409c:	00000000 	nop
    40a0:	00000000 	nop
    40a4:	10000002 	b	40b0 <main+0x29e0>
    40a8:	00000000 	nop
    40ac:	00000000 	nop
    40b0:	03c0e825 	move	sp,s8
    40b4:	dfbf0058 	ld	ra,88(sp)
    40b8:	dfbe0050 	ld	s8,80(sp)
    40bc:	dfbc0048 	ld	gp,72(sp)
    40c0:	67bd0060 	daddiu	sp,sp,96
    40c4:	03e00008 	jr	ra
    40c8:	00000000 	nop
    40cc:	67bdffb0 	daddiu	sp,sp,-80
    40d0:	ffbf0048 	sd	ra,72(sp)
    40d4:	ffbe0040 	sd	s8,64(sp)
    40d8:	ffbc0038 	sd	gp,56(sp)
    40dc:	03a0f025 	move	s8,sp
    40e0:	3c1c0002 	lui	gp,0x2
    40e4:	0399e02d 	daddu	gp,gp,t9
    40e8:	679c3f84 	daddiu	gp,gp,16260
    40ec:	ffc40020 	sd	a0,32(s8)
    40f0:	ffc00010 	sd	zero,16(s8)
    40f4:	67c20010 	daddiu	v0,s8,16
    40f8:	00402825 	move	a1,v0
    40fc:	dfc40020 	ld	a0,32(s8)
    4100:	df828118 	ld	v0,-32488(gp)
    4104:	0040c825 	move	t9,v0
    4108:	0411f8e3 	bal	2498 <main+0xdc8>
    410c:	00000000 	nop
    4110:	a7c20004 	sh	v0,4(s8)
    4114:	97c20004 	lhu	v0,4(s8)
    4118:	1040006e 	beqz	v0,42d4 <main+0x2c04>
    411c:	00000000 	nop
    4120:	97c30004 	lhu	v1,4(s8)
    4124:	2402000c 	li	v0,12
    4128:	14620013 	bne	v1,v0,4178 <main+0x2aa8>
    412c:	00000000 	nop
    4130:	dfc30010 	ld	v1,16(s8)
    4134:	2406000c 	li	a2,12
    4138:	df828058 	ld	v0,-32680(gp)
    413c:	64456ec0 	daddiu	a1,v0,28352
    4140:	00602025 	move	a0,v1
    4144:	df828218 	ld	v0,-32232(gp)
    4148:	0040c825 	move	t9,v0
    414c:	0320f809 	jalr	t9
    4150:	00000000 	nop
    4154:	14400008 	bnez	v0,4178 <main+0x2aa8>
    4158:	00000000 	nop
    415c:	df8280a0 	ld	v0,-32608(gp)
    4160:	0040c825 	move	t9,v0
    4164:	0411fbcb 	bal	3094 <main+0x19c4>
    4168:	00000000 	nop
    416c:	ffc20008 	sd	v0,8(s8)
    4170:	dfc20008 	ld	v0,8(s8)
    4174:	a0400002 	sb	zero,2(v0)
    4178:	afc00000 	sw	zero,0(s8)
    417c:	1000004c 	b	42b0 <main+0x2be0>
    4180:	00000000 	nop
    4184:	df8380f8 	ld	v1,-32520(gp)
    4188:	8fc20000 	lw	v0,0(s8)
    418c:	00021178 	dsll	v0,v0,0x5
    4190:	0062102d 	daddu	v0,v1,v0
    4194:	94430008 	lhu	v1,8(v0)
    4198:	97c20004 	lhu	v0,4(s8)
    419c:	14430041 	bne	v0,v1,42a4 <main+0x2bd4>
    41a0:	00000000 	nop
    41a4:	dfc40010 	ld	a0,16(s8)
    41a8:	df8380f8 	ld	v1,-32520(gp)
    41ac:	8fc20000 	lw	v0,0(s8)
    41b0:	00021178 	dsll	v0,v0,0x5
    41b4:	0062102d 	daddu	v0,v1,v0
    41b8:	dc420000 	ld	v0,0(v0)
    41bc:	97c30004 	lhu	v1,4(s8)
    41c0:	00603025 	move	a2,v1
    41c4:	00402825 	move	a1,v0
    41c8:	df828218 	ld	v0,-32232(gp)
    41cc:	0040c825 	move	t9,v0
    41d0:	0320f809 	jalr	t9
    41d4:	00000000 	nop
    41d8:	14400032 	bnez	v0,42a4 <main+0x2bd4>
    41dc:	00000000 	nop
    41e0:	df8380f8 	ld	v1,-32520(gp)
    41e4:	8fc20000 	lw	v0,0(s8)
    41e8:	00021178 	dsll	v0,v0,0x5
    41ec:	0062102d 	daddu	v0,v1,v0
    41f0:	dc420000 	ld	v0,0(v0)
    41f4:	00402025 	move	a0,v0
    41f8:	df8281d0 	ld	v0,-32304(gp)
    41fc:	0040c825 	move	t9,v0
    4200:	0320f809 	jalr	t9
    4204:	00000000 	nop
    4208:	df8380f8 	ld	v1,-32520(gp)
    420c:	8fc20000 	lw	v0,0(s8)
    4210:	00021178 	dsll	v0,v0,0x5
    4214:	0062102d 	daddu	v0,v1,v0
    4218:	fc400000 	sd	zero,0(v0)
    421c:	df8380f8 	ld	v1,-32520(gp)
    4220:	8fc20000 	lw	v0,0(s8)
    4224:	00021178 	dsll	v0,v0,0x5
    4228:	0062102d 	daddu	v0,v1,v0
    422c:	a4400008 	sh	zero,8(v0)
    4230:	df8380f8 	ld	v1,-32520(gp)
    4234:	8fc20000 	lw	v0,0(s8)
    4238:	00021178 	dsll	v0,v0,0x5
    423c:	0062102d 	daddu	v0,v1,v0
    4240:	dc420010 	ld	v0,16(v0)
    4244:	10400020 	beqz	v0,42c8 <main+0x2bf8>
    4248:	00000000 	nop
    424c:	df8380f8 	ld	v1,-32520(gp)
    4250:	8fc20000 	lw	v0,0(s8)
    4254:	00021178 	dsll	v0,v0,0x5
    4258:	0062102d 	daddu	v0,v1,v0
    425c:	dc420010 	ld	v0,16(v0)
    4260:	00402025 	move	a0,v0
    4264:	df8281d0 	ld	v0,-32304(gp)
    4268:	0040c825 	move	t9,v0
    426c:	0320f809 	jalr	t9
    4270:	00000000 	nop
    4274:	df8380f8 	ld	v1,-32520(gp)
    4278:	8fc20000 	lw	v0,0(s8)
    427c:	00021178 	dsll	v0,v0,0x5
    4280:	0062102d 	daddu	v0,v1,v0
    4284:	fc400010 	sd	zero,16(v0)
    4288:	df8380f8 	ld	v1,-32520(gp)
    428c:	8fc20000 	lw	v0,0(s8)
    4290:	00021178 	dsll	v0,v0,0x5
    4294:	0062102d 	daddu	v0,v1,v0
    4298:	a4400018 	sh	zero,24(v0)
    429c:	1000000a 	b	42c8 <main+0x2bf8>
    42a0:	00000000 	nop
    42a4:	8fc20000 	lw	v0,0(s8)
    42a8:	24420001 	addiu	v0,v0,1
    42ac:	afc20000 	sw	v0,0(s8)
    42b0:	8fc20000 	lw	v0,0(s8)
    42b4:	2842000e 	slti	v0,v0,14
    42b8:	1440ffb2 	bnez	v0,4184 <main+0x2ab4>
    42bc:	00000000 	nop
    42c0:	10000005 	b	42d8 <main+0x2c08>
    42c4:	00000000 	nop
    42c8:	00000000 	nop
    42cc:	10000002 	b	42d8 <main+0x2c08>
    42d0:	00000000 	nop
    42d4:	00000000 	nop
    42d8:	03c0e825 	move	sp,s8
    42dc:	dfbf0048 	ld	ra,72(sp)
    42e0:	dfbe0040 	ld	s8,64(sp)
    42e4:	dfbc0038 	ld	gp,56(sp)
    42e8:	67bd0050 	daddiu	sp,sp,80
    42ec:	03e00008 	jr	ra
    42f0:	00000000 	nop
    42f4:	67bdffd0 	daddiu	sp,sp,-48
    42f8:	ffbe0028 	sd	s8,40(sp)
    42fc:	03a0f025 	move	s8,sp
    4300:	ffc40010 	sd	a0,16(s8)
    4304:	24020001 	li	v0,1
    4308:	afc20000 	sw	v0,0(s8)
    430c:	afc00004 	sw	zero,4(s8)
    4310:	dfc20010 	ld	v0,16(s8)
    4314:	64420001 	daddiu	v0,v0,1
    4318:	ffc20010 	sd	v0,16(s8)
    431c:	dfc20010 	ld	v0,16(s8)
    4320:	90420000 	lbu	v0,0(v0)
    4324:	a3c20008 	sb	v0,8(s8)
    4328:	93c20008 	lbu	v0,8(s8)
    432c:	3042007f 	andi	v0,v0,0x7f
    4330:	8fc30000 	lw	v1,0(s8)
    4334:	00620018 	mult	v1,v0
    4338:	00001012 	mflo	v0
    433c:	8fc30004 	lw	v1,4(s8)
    4340:	00621021 	addu	v0,v1,v0
    4344:	afc20004 	sw	v0,4(s8)
    4348:	8fc20000 	lw	v0,0(s8)
    434c:	000211c0 	sll	v0,v0,0x7
    4350:	afc20000 	sw	v0,0(s8)
    4354:	8fc30000 	lw	v1,0(s8)
    4358:	3c020020 	lui	v0,0x20
    435c:	34420001 	ori	v0,v0,0x1
    4360:	0062102a 	slt	v0,v1,v0
    4364:	14400004 	bnez	v0,4378 <main+0x2ca8>
    4368:	00000000 	nop
    436c:	2402ffff 	li	v0,-1
    4370:	10000005 	b	4388 <main+0x2cb8>
    4374:	00000000 	nop
    4378:	83c20008 	lb	v0,8(s8)
    437c:	0440ffe4 	bltz	v0,4310 <main+0x2c40>
    4380:	00000000 	nop
    4384:	8fc20004 	lw	v0,4(s8)
    4388:	03c0e825 	move	sp,s8
    438c:	dfbe0028 	ld	s8,40(sp)
    4390:	67bd0030 	daddiu	sp,sp,48
    4394:	03e00008 	jr	ra
    4398:	00000000 	nop
    439c:	67bd8010 	daddiu	sp,sp,-32752
    43a0:	ffbf7fe8 	sd	ra,32744(sp)
    43a4:	ffbe7fe0 	sd	s8,32736(sp)
    43a8:	ffbc7fd8 	sd	gp,32728(sp)
    43ac:	3c030001 	lui	v1,0x1
    43b0:	34630080 	ori	v1,v1,0x80
    43b4:	03a3e82f 	dsubu	sp,sp,v1
    43b8:	03a0f025 	move	s8,sp
    43bc:	3c1c0002 	lui	gp,0x2
    43c0:	0399e02d 	daddu	gp,gp,t9
    43c4:	679c3cb4 	daddiu	gp,gp,15540
    43c8:	df8280b8 	ld	v0,-32584(gp)
    43cc:	dc420000 	ld	v0,0(v0)
    43d0:	ffc20018 	sd	v0,24(s8)
    43d4:	dfc20018 	ld	v0,24(s8)
    43d8:	14400004 	bnez	v0,43ec <main+0x2d1c>
    43dc:	00000000 	nop
    43e0:	00001025 	move	v0,zero
    43e4:	1000017c 	b	49d8 <main+0x3308>
    43e8:	00000000 	nop
    43ec:	dfc20018 	ld	v0,24(s8)
    43f0:	90420000 	lbu	v0,0(v0)
    43f4:	a3c20020 	sb	v0,32(s8)
    43f8:	67c30030 	daddiu	v1,s8,48
    43fc:	3c020001 	lui	v0,0x1
    4400:	34428011 	ori	v0,v0,0x8011
    4404:	00403025 	move	a2,v0
    4408:	00002825 	move	a1,zero
    440c:	00602025 	move	a0,v1
    4410:	df8281f8 	ld	v0,-32264(gp)
    4414:	0040c825 	move	t9,v0
    4418:	0320f809 	jalr	t9
    441c:	00000000 	nop
    4420:	dfc20018 	ld	v0,24(s8)
    4424:	64420004 	daddiu	v0,v0,4
    4428:	93c30020 	lbu	v1,32(s8)
    442c:	67c40030 	daddiu	a0,s8,48
    4430:	00603025 	move	a2,v1
    4434:	00402825 	move	a1,v0
    4438:	df828280 	ld	v0,-32128(gp)
    443c:	0040c825 	move	t9,v0
    4440:	0320f809 	jalr	t9
    4444:	00000000 	nop
    4448:	93c20020 	lbu	v0,32(s8)
    444c:	67c30030 	daddiu	v1,s8,48
    4450:	0062202d 	daddu	a0,v1,v0
    4454:	93c20020 	lbu	v0,32(s8)
    4458:	24030005 	li	v1,5
    445c:	00621023 	subu	v0,v1,v0
    4460:	00403025 	move	a2,v0
    4464:	00802825 	move	a1,a0
    4468:	00002025 	move	a0,zero
    446c:	df828228 	ld	v0,-32216(gp)
    4470:	0040c825 	move	t9,v0
    4474:	0320f809 	jalr	t9
    4478:	00000000 	nop
    447c:	afc20024 	sw	v0,36(s8)
    4480:	8fc20024 	lw	v0,36(s8)
    4484:	18400008 	blez	v0,44a8 <main+0x2dd8>
    4488:	00000000 	nop
    448c:	93c20020 	lbu	v0,32(s8)
    4490:	24030005 	li	v1,5
    4494:	00621023 	subu	v0,v1,v0
    4498:	8fc30024 	lw	v1,36(s8)
    449c:	0043102a 	slt	v0,v0,v1
    44a0:	1040001f 	beqz	v0,4520 <main+0x2e50>
    44a4:	00000000 	nop
    44a8:	df8281e8 	ld	v0,-32280(gp)
    44ac:	0040c825 	move	t9,v0
    44b0:	0320f809 	jalr	t9
    44b4:	00000000 	nop
    44b8:	8c430000 	lw	v1,0(v0)
    44bc:	24020004 	li	v0,4
    44c0:	10620011 	beq	v1,v0,4508 <main+0x2e38>
    44c4:	00000000 	nop
    44c8:	df8281e8 	ld	v0,-32280(gp)
    44cc:	0040c825 	move	t9,v0
    44d0:	0320f809 	jalr	t9
    44d4:	00000000 	nop
    44d8:	8c430000 	lw	v1,0(v0)
    44dc:	2402000b 	li	v0,11
    44e0:	10620009 	beq	v1,v0,4508 <main+0x2e38>
    44e4:	00000000 	nop
    44e8:	df8281e8 	ld	v0,-32280(gp)
    44ec:	0040c825 	move	t9,v0
    44f0:	0320f809 	jalr	t9
    44f4:	00000000 	nop
    44f8:	8c430000 	lw	v1,0(v0)
    44fc:	2402000b 	li	v0,11
    4500:	14620004 	bne	v1,v0,4514 <main+0x2e44>
    4504:	00000000 	nop
    4508:	00001025 	move	v0,zero
    450c:	10000132 	b	49d8 <main+0x3308>
    4510:	00000000 	nop
    4514:	00001025 	move	v0,zero
    4518:	1000012f 	b	49d8 <main+0x3308>
    451c:	00000000 	nop
    4520:	67c20030 	daddiu	v0,s8,48
    4524:	00402025 	move	a0,v0
    4528:	df828120 	ld	v0,-32480(gp)
    452c:	0040c825 	move	t9,v0
    4530:	0411ff70 	bal	42f4 <main+0x2c24>
    4534:	00000000 	nop
    4538:	afc20028 	sw	v0,40(s8)
    453c:	afc00000 	sw	zero,0(s8)
    4540:	8fc20028 	lw	v0,40(s8)
    4544:	28420080 	slti	v0,v0,128
    4548:	10400005 	beqz	v0,4560 <main+0x2e90>
    454c:	00000000 	nop
    4550:	24020001 	li	v0,1
    4554:	afc20000 	sw	v0,0(s8)
    4558:	10000019 	b	45c0 <main+0x2ef0>
    455c:	00000000 	nop
    4560:	8fc20028 	lw	v0,40(s8)
    4564:	28424000 	slti	v0,v0,16384
    4568:	10400005 	beqz	v0,4580 <main+0x2eb0>
    456c:	00000000 	nop
    4570:	24020002 	li	v0,2
    4574:	afc20000 	sw	v0,0(s8)
    4578:	10000011 	b	45c0 <main+0x2ef0>
    457c:	00000000 	nop
    4580:	8fc30028 	lw	v1,40(s8)
    4584:	3c020020 	lui	v0,0x20
    4588:	0062102a 	slt	v0,v1,v0
    458c:	10400005 	beqz	v0,45a4 <main+0x2ed4>
    4590:	00000000 	nop
    4594:	24020003 	li	v0,3
    4598:	afc20000 	sw	v0,0(s8)
    459c:	10000008 	b	45c0 <main+0x2ef0>
    45a0:	00000000 	nop
    45a4:	8fc30028 	lw	v1,40(s8)
    45a8:	3c021000 	lui	v0,0x1000
    45ac:	0062102a 	slt	v0,v1,v0
    45b0:	10400003 	beqz	v0,45c0 <main+0x2ef0>
    45b4:	00000000 	nop
    45b8:	24020004 	li	v0,4
    45bc:	afc20000 	sw	v0,0(s8)
    45c0:	8fc30028 	lw	v1,40(s8)
    45c4:	3c020001 	lui	v0,0x1
    45c8:	3442800c 	ori	v0,v0,0x800c
    45cc:	0062102b 	sltu	v0,v1,v0
    45d0:	14400006 	bnez	v0,45ec <main+0x2f1c>
    45d4:	00000000 	nop
    45d8:	dfc20018 	ld	v0,24(s8)
    45dc:	a0400000 	sb	zero,0(v0)
    45e0:	24020001 	li	v0,1
    45e4:	100000fc 	b	49d8 <main+0x3308>
    45e8:	00000000 	nop
    45ec:	93c20020 	lbu	v0,32(s8)
    45f0:	8fc30024 	lw	v1,36(s8)
    45f4:	00621021 	addu	v0,v1,v0
    45f8:	afc20004 	sw	v0,4(s8)
    45fc:	8fc20000 	lw	v0,0(s8)
    4600:	24420001 	addiu	v0,v0,1
    4604:	8fc30004 	lw	v1,4(s8)
    4608:	00621023 	subu	v0,v1,v0
    460c:	8fc30028 	lw	v1,40(s8)
    4610:	00621023 	subu	v0,v1,v0
    4614:	afc20008 	sw	v0,8(s8)
    4618:	8fc20008 	lw	v0,8(s8)
    461c:	04410018 	bgez	v0,4680 <main+0x2fb0>
    4620:	00000000 	nop
    4624:	8fc20008 	lw	v0,8(s8)
    4628:	304200ff 	andi	v0,v0,0xff
    462c:	00021023 	negu	v0,v0
    4630:	a3c20020 	sb	v0,32(s8)
    4634:	dfc20018 	ld	v0,24(s8)
    4638:	64440004 	daddiu	a0,v0,4
    463c:	93c20020 	lbu	v0,32(s8)
    4640:	8fc30004 	lw	v1,4(s8)
    4644:	00621023 	subu	v0,v1,v0
    4648:	67c30030 	daddiu	v1,s8,48
    464c:	0062102d 	daddu	v0,v1,v0
    4650:	93c30020 	lbu	v1,32(s8)
    4654:	00603025 	move	a2,v1
    4658:	00402825 	move	a1,v0
    465c:	df828280 	ld	v0,-32128(gp)
    4660:	0040c825 	move	t9,v0
    4664:	0320f809 	jalr	t9
    4668:	00000000 	nop
    466c:	dfc20018 	ld	v0,24(s8)
    4670:	93c30020 	lbu	v1,32(s8)
    4674:	a0430000 	sb	v1,0(v0)
    4678:	10000003 	b	4688 <main+0x2fb8>
    467c:	00000000 	nop
    4680:	dfc20018 	ld	v0,24(s8)
    4684:	a0400000 	sb	zero,0(v0)
    4688:	afc0000c 	sw	zero,12(s8)
    468c:	1000002f 	b	474c <main+0x307c>
    4690:	00000000 	nop
    4694:	67c30030 	daddiu	v1,s8,48
    4698:	8fc20004 	lw	v0,4(s8)
    469c:	0062102d 	daddu	v0,v1,v0
    46a0:	8fc30008 	lw	v1,8(s8)
    46a4:	00603025 	move	a2,v1
    46a8:	00402825 	move	a1,v0
    46ac:	00002025 	move	a0,zero
    46b0:	df828228 	ld	v0,-32216(gp)
    46b4:	0040c825 	move	t9,v0
    46b8:	0320f809 	jalr	t9
    46bc:	00000000 	nop
    46c0:	afc20010 	sw	v0,16(s8)
    46c4:	8fc20010 	lw	v0,16(s8)
    46c8:	14400004 	bnez	v0,46dc <main+0x300c>
    46cc:	00000000 	nop
    46d0:	24020001 	li	v0,1
    46d4:	100000c0 	b	49d8 <main+0x3308>
    46d8:	00000000 	nop
    46dc:	8fc20010 	lw	v0,16(s8)
    46e0:	04410012 	bgez	v0,472c <main+0x305c>
    46e4:	00000000 	nop
    46e8:	8fc2000c 	lw	v0,12(s8)
    46ec:	24430001 	addiu	v1,v0,1
    46f0:	afc3000c 	sw	v1,12(s8)
    46f4:	284203e8 	slti	v0,v0,1000
    46f8:	10400009 	beqz	v0,4720 <main+0x3050>
    46fc:	00000000 	nop
    4700:	240403e8 	li	a0,1000
    4704:	df828288 	ld	v0,-32120(gp)
    4708:	0040c825 	move	t9,v0
    470c:	0320f809 	jalr	t9
    4710:	00000000 	nop
    4714:	afc00010 	sw	zero,16(s8)
    4718:	10000004 	b	472c <main+0x305c>
    471c:	00000000 	nop
    4720:	00001025 	move	v0,zero
    4724:	100000ac 	b	49d8 <main+0x3308>
    4728:	00000000 	nop
    472c:	8fc30008 	lw	v1,8(s8)
    4730:	8fc20010 	lw	v0,16(s8)
    4734:	00621023 	subu	v0,v1,v0
    4738:	afc20008 	sw	v0,8(s8)
    473c:	8fc30004 	lw	v1,4(s8)
    4740:	8fc20010 	lw	v0,16(s8)
    4744:	00621021 	addu	v0,v1,v0
    4748:	afc20004 	sw	v0,4(s8)
    474c:	8fc20008 	lw	v0,8(s8)
    4750:	1c40ffd0 	bgtz	v0,4694 <main+0x2fc4>
    4754:	00000000 	nop
    4758:	93c20030 	lbu	v0,48(s8)
    475c:	00021102 	srl	v0,v0,0x4
    4760:	a3c2002c 	sb	v0,44(s8)
    4764:	93c2002c 	lbu	v0,44(s8)
    4768:	2c43000f 	sltiu	v1,v0,15
    476c:	10600099 	beqz	v1,49d4 <main+0x3304>
    4770:	00000000 	nop
    4774:	000218f8 	dsll	v1,v0,0x3
    4778:	df828058 	ld	v0,-32680(gp)
    477c:	64426ed0 	daddiu	v0,v0,28368
    4780:	0062102d 	daddu	v0,v1,v0
    4784:	dc420000 	ld	v0,0(v0)
    4788:	005c102d 	daddu	v0,v0,gp
    478c:	00400008 	jr	v0
    4790:	00000000 	nop
    4794:	67c20030 	daddiu	v0,s8,48
    4798:	00402025 	move	a0,v0
    479c:	df828128 	ld	v0,-32472(gp)
    47a0:	0040c825 	move	t9,v0
    47a4:	0411fa96 	bal	3200 <main+0x1b30>
    47a8:	00000000 	nop
    47ac:	a3c2002d 	sb	v0,45(s8)
    47b0:	93c2002d 	lbu	v0,45(s8)
    47b4:	00402025 	move	a0,v0
    47b8:	df828130 	ld	v0,-32464(gp)
    47bc:	0040c825 	move	t9,v0
    47c0:	0411f8c8 	bal	2ae4 <main+0x1414>
    47c4:	00000000 	nop
    47c8:	93c2002d 	lbu	v0,45(s8)
    47cc:	10400004 	beqz	v0,47e0 <main+0x3110>
    47d0:	00000000 	nop
    47d4:	00001025 	move	v0,zero
    47d8:	1000007f 	b	49d8 <main+0x3308>
    47dc:	00000000 	nop
    47e0:	24020001 	li	v0,1
    47e4:	1000007c 	b	49d8 <main+0x3308>
    47e8:	00000000 	nop
    47ec:	dfc20018 	ld	v0,24(s8)
    47f0:	90420001 	lbu	v0,1(v0)
    47f4:	14400004 	bnez	v0,4808 <main+0x3138>
    47f8:	00000000 	nop
    47fc:	24020001 	li	v0,1
    4800:	10000075 	b	49d8 <main+0x3308>
    4804:	00000000 	nop
    4808:	67c20030 	daddiu	v0,s8,48
    480c:	00402025 	move	a0,v0
    4810:	df828138 	ld	v0,-32456(gp)
    4814:	0040c825 	move	t9,v0
    4818:	0411fc86 	bal	3a34 <main+0x2364>
    481c:	00000000 	nop
    4820:	24020001 	li	v0,1
    4824:	1000006c 	b	49d8 <main+0x3308>
    4828:	00000000 	nop
    482c:	dfc20018 	ld	v0,24(s8)
    4830:	90420001 	lbu	v0,1(v0)
    4834:	14400004 	bnez	v0,4848 <main+0x3178>
    4838:	00000000 	nop
    483c:	24020001 	li	v0,1
    4840:	10000065 	b	49d8 <main+0x3308>
    4844:	00000000 	nop
    4848:	67c20030 	daddiu	v0,s8,48
    484c:	00402025 	move	a0,v0
    4850:	df828140 	ld	v0,-32448(gp)
    4854:	0040c825 	move	t9,v0
    4858:	0411f9c5 	bal	2f70 <main+0x18a0>
    485c:	00000000 	nop
    4860:	24020001 	li	v0,1
    4864:	1000005c 	b	49d8 <main+0x3308>
    4868:	00000000 	nop
    486c:	dfc20018 	ld	v0,24(s8)
    4870:	90420001 	lbu	v0,1(v0)
    4874:	14400004 	bnez	v0,4888 <main+0x31b8>
    4878:	00000000 	nop
    487c:	24020001 	li	v0,1
    4880:	10000055 	b	49d8 <main+0x3308>
    4884:	00000000 	nop
    4888:	67c20030 	daddiu	v0,s8,48
    488c:	00402025 	move	a0,v0
    4890:	df828148 	ld	v0,-32440(gp)
    4894:	0040c825 	move	t9,v0
    4898:	0411f98a 	bal	2ec4 <main+0x17f4>
    489c:	00000000 	nop
    48a0:	24020001 	li	v0,1
    48a4:	1000004c 	b	49d8 <main+0x3308>
    48a8:	00000000 	nop
    48ac:	24020001 	li	v0,1
    48b0:	10000049 	b	49d8 <main+0x3308>
    48b4:	00000000 	nop
    48b8:	dfc20018 	ld	v0,24(s8)
    48bc:	90420001 	lbu	v0,1(v0)
    48c0:	14400004 	bnez	v0,48d4 <main+0x3204>
    48c4:	00000000 	nop
    48c8:	24020001 	li	v0,1
    48cc:	10000042 	b	49d8 <main+0x3308>
    48d0:	00000000 	nop
    48d4:	67c20030 	daddiu	v0,s8,48
    48d8:	00402025 	move	a0,v0
    48dc:	df828150 	ld	v0,-32432(gp)
    48e0:	0040c825 	move	t9,v0
    48e4:	0411fd66 	bal	3e80 <main+0x27b0>
    48e8:	00000000 	nop
    48ec:	67c20030 	daddiu	v0,s8,48
    48f0:	00402025 	move	a0,v0
    48f4:	df828158 	ld	v0,-32424(gp)
    48f8:	0040c825 	move	t9,v0
    48fc:	0411f913 	bal	2d4c <main+0x167c>
    4900:	00000000 	nop
    4904:	24020001 	li	v0,1
    4908:	10000033 	b	49d8 <main+0x3308>
    490c:	00000000 	nop
    4910:	dfc20018 	ld	v0,24(s8)
    4914:	90420001 	lbu	v0,1(v0)
    4918:	14400004 	bnez	v0,492c <main+0x325c>
    491c:	00000000 	nop
    4920:	24020001 	li	v0,1
    4924:	1000002c 	b	49d8 <main+0x3308>
    4928:	00000000 	nop
    492c:	67c20030 	daddiu	v0,s8,48
    4930:	00402025 	move	a0,v0
    4934:	df828160 	ld	v0,-32416(gp)
    4938:	0040c825 	move	t9,v0
    493c:	0411fde3 	bal	40cc <main+0x29fc>
    4940:	00000000 	nop
    4944:	67c20030 	daddiu	v0,s8,48
    4948:	00402025 	move	a0,v0
    494c:	df828168 	ld	v0,-32408(gp)
    4950:	0040c825 	move	t9,v0
    4954:	0411f930 	bal	2e18 <main+0x1748>
    4958:	00000000 	nop
    495c:	24020001 	li	v0,1
    4960:	1000001d 	b	49d8 <main+0x3308>
    4964:	00000000 	nop
    4968:	dfc20018 	ld	v0,24(s8)
    496c:	90420001 	lbu	v0,1(v0)
    4970:	14400004 	bnez	v0,4984 <main+0x32b4>
    4974:	00000000 	nop
    4978:	24020001 	li	v0,1
    497c:	10000016 	b	49d8 <main+0x3308>
    4980:	00000000 	nop
    4984:	dfc20018 	ld	v0,24(s8)
    4988:	90420002 	lbu	v0,2(v0)
    498c:	10400007 	beqz	v0,49ac <main+0x32dc>
    4990:	00000000 	nop
    4994:	dfc20018 	ld	v0,24(s8)
    4998:	90420003 	lbu	v0,3(v0)
    499c:	24420001 	addiu	v0,v0,1
    49a0:	304300ff 	andi	v1,v0,0xff
    49a4:	dfc20018 	ld	v0,24(s8)
    49a8:	a0430003 	sb	v1,3(v0)
    49ac:	df828170 	ld	v0,-32400(gp)
    49b0:	0040c825 	move	t9,v0
    49b4:	0411f8cc 	bal	2ce8 <main+0x1618>
    49b8:	00000000 	nop
    49bc:	24020001 	li	v0,1
    49c0:	10000005 	b	49d8 <main+0x3308>
    49c4:	00000000 	nop
    49c8:	00001025 	move	v0,zero
    49cc:	10000002 	b	49d8 <main+0x3308>
    49d0:	00000000 	nop
    49d4:	24020001 	li	v0,1
    49d8:	3c080001 	lui	a4,0x1
    49dc:	35080080 	ori	a4,a4,0x80
    49e0:	03c8e82d 	daddu	sp,s8,a4
    49e4:	dfbf7fe8 	ld	ra,32744(sp)
    49e8:	dfbe7fe0 	ld	s8,32736(sp)
    49ec:	dfbc7fd8 	ld	gp,32728(sp)
    49f0:	67bd7ff0 	daddiu	sp,sp,32752
    49f4:	03e00008 	jr	ra
    49f8:	00000000 	nop
    49fc:	67bdffd0 	daddiu	sp,sp,-48
    4a00:	ffbf0028 	sd	ra,40(sp)
    4a04:	ffbe0020 	sd	s8,32(sp)
    4a08:	ffbc0018 	sd	gp,24(sp)
    4a0c:	03a0f025 	move	s8,sp
    4a10:	3c1c0002 	lui	gp,0x2
    4a14:	0399e02d 	daddu	gp,gp,t9
    4a18:	679c3654 	daddiu	gp,gp,13908
    4a1c:	df828058 	ld	v0,-32680(gp)
    4a20:	64456f48 	daddiu	a1,v0,28488
    4a24:	24040002 	li	a0,2
    4a28:	df828210 	ld	v0,-32240(gp)
    4a2c:	0040c825 	move	t9,v0
    4a30:	0320f809 	jalr	t9
    4a34:	00000000 	nop
    4a38:	00401825 	move	v1,v0
    4a3c:	df828178 	ld	v0,-32392(gp)
    4a40:	fc430000 	sd	v1,0(v0)
    4a44:	24050010 	li	a1,16
    4a48:	24040001 	li	a0,1
    4a4c:	df828250 	ld	v0,-32176(gp)
    4a50:	0040c825 	move	t9,v0
    4a54:	0320f809 	jalr	t9
    4a58:	00000000 	nop
    4a5c:	00401825 	move	v1,v0
    4a60:	df8280b8 	ld	v0,-32584(gp)
    4a64:	fc430000 	sd	v1,0(v0)
    4a68:	df828180 	ld	v0,-32384(gp)
    4a6c:	0040c825 	move	t9,v0
    4a70:	0411fe4a 	bal	439c <main+0x2ccc>
    4a74:	00000000 	nop
    4a78:	afc20000 	sw	v0,0(s8)
    4a7c:	8fc20000 	lw	v0,0(s8)
    4a80:	10400003 	beqz	v0,4a90 <main+0x33c0>
    4a84:	00000000 	nop
    4a88:	1000fff7 	b	4a68 <main+0x3398>
    4a8c:	00000000 	nop
    4a90:	00000000 	nop
    4a94:	df828188 	ld	v0,-32376(gp)
    4a98:	0040c825 	move	t9,v0
    4a9c:	0411f960 	bal	3020 <main+0x1950>
    4aa0:	00000000 	nop
    4aa4:	00000000 	nop
    4aa8:	03c0e825 	move	sp,s8
    4aac:	dfbf0028 	ld	ra,40(sp)
    4ab0:	dfbe0020 	ld	s8,32(sp)
    4ab4:	dfbc0018 	ld	gp,24(sp)
    4ab8:	67bd0030 	daddiu	sp,sp,48
    4abc:	03e00008 	jr	ra
    4ac0:	00000000 	nop
	...
    4ad0:	67bdffe0 	daddiu	sp,sp,-32
    4ad4:	ffbe0018 	sd	s8,24(sp)
    4ad8:	03a0f025 	move	s8,sp
    4adc:	ffc40000 	sd	a0,0(s8)
    4ae0:	dfc20000 	ld	v0,0(s8)
    4ae4:	ac400000 	sw	zero,0(v0)
    4ae8:	dfc20000 	ld	v0,0(s8)
    4aec:	ac400004 	sw	zero,4(v0)
    4af0:	dfc20000 	ld	v0,0(s8)
    4af4:	3c036745 	lui	v1,0x6745
    4af8:	34632301 	ori	v1,v1,0x2301
    4afc:	ac430008 	sw	v1,8(v0)
    4b00:	dfc20000 	ld	v0,0(s8)
    4b04:	3c03efcd 	lui	v1,0xefcd
    4b08:	3463ab89 	ori	v1,v1,0xab89
    4b0c:	ac43000c 	sw	v1,12(v0)
    4b10:	dfc20000 	ld	v0,0(s8)
    4b14:	3c0398ba 	lui	v1,0x98ba
    4b18:	3463dcfe 	ori	v1,v1,0xdcfe
    4b1c:	ac430010 	sw	v1,16(v0)
    4b20:	dfc20000 	ld	v0,0(s8)
    4b24:	3c031032 	lui	v1,0x1032
    4b28:	34635476 	ori	v1,v1,0x5476
    4b2c:	ac430014 	sw	v1,20(v0)
    4b30:	00000000 	nop
    4b34:	03c0e825 	move	sp,s8
    4b38:	dfbe0018 	ld	s8,24(sp)
    4b3c:	67bd0020 	daddiu	sp,sp,32
    4b40:	03e00008 	jr	ra
    4b44:	00000000 	nop
    4b48:	67bdffb0 	daddiu	sp,sp,-80
    4b4c:	ffbf0048 	sd	ra,72(sp)
    4b50:	ffbe0040 	sd	s8,64(sp)
    4b54:	ffbc0038 	sd	gp,56(sp)
    4b58:	03a0f025 	move	s8,sp
    4b5c:	3c1c0002 	lui	gp,0x2
    4b60:	0399e02d 	daddu	gp,gp,t9
    4b64:	679c3508 	daddiu	gp,gp,13576
    4b68:	ffc40010 	sd	a0,16(s8)
    4b6c:	ffc50018 	sd	a1,24(s8)
    4b70:	00c01025 	move	v0,a2
    4b74:	00021000 	sll	v0,v0,0x0
    4b78:	afc20020 	sw	v0,32(s8)
    4b7c:	afc00000 	sw	zero,0(s8)
    4b80:	afc00004 	sw	zero,4(s8)
    4b84:	afc00008 	sw	zero,8(s8)
    4b88:	dfc20010 	ld	v0,16(s8)
    4b8c:	8c420000 	lw	v0,0(v0)
    4b90:	000210c2 	srl	v0,v0,0x3
    4b94:	3042003f 	andi	v0,v0,0x3f
    4b98:	afc20004 	sw	v0,4(s8)
    4b9c:	24030040 	li	v1,64
    4ba0:	8fc20004 	lw	v0,4(s8)
    4ba4:	00621023 	subu	v0,v1,v0
    4ba8:	afc20008 	sw	v0,8(s8)
    4bac:	dfc20010 	ld	v0,16(s8)
    4bb0:	8c430000 	lw	v1,0(v0)
    4bb4:	8fc20020 	lw	v0,32(s8)
    4bb8:	000210c0 	sll	v0,v0,0x3
    4bbc:	00621021 	addu	v0,v1,v0
    4bc0:	00401825 	move	v1,v0
    4bc4:	dfc20010 	ld	v0,16(s8)
    4bc8:	ac430000 	sw	v1,0(v0)
    4bcc:	dfc20010 	ld	v0,16(s8)
    4bd0:	8c430000 	lw	v1,0(v0)
    4bd4:	8fc20020 	lw	v0,32(s8)
    4bd8:	000210c0 	sll	v0,v0,0x3
    4bdc:	0062102b 	sltu	v0,v1,v0
    4be0:	10400007 	beqz	v0,4c00 <main+0x3530>
    4be4:	00000000 	nop
    4be8:	dfc20010 	ld	v0,16(s8)
    4bec:	8c420004 	lw	v0,4(v0)
    4bf0:	24420001 	addiu	v0,v0,1
    4bf4:	00401825 	move	v1,v0
    4bf8:	dfc20010 	ld	v0,16(s8)
    4bfc:	ac430004 	sw	v1,4(v0)
    4c00:	dfc20010 	ld	v0,16(s8)
    4c04:	8c430004 	lw	v1,4(v0)
    4c08:	8fc20020 	lw	v0,32(s8)
    4c0c:	00021742 	srl	v0,v0,0x1d
    4c10:	00621021 	addu	v0,v1,v0
    4c14:	00401825 	move	v1,v0
    4c18:	dfc20010 	ld	v0,16(s8)
    4c1c:	ac430004 	sw	v1,4(v0)
    4c20:	8fc30020 	lw	v1,32(s8)
    4c24:	8fc20008 	lw	v0,8(s8)
    4c28:	0062102b 	sltu	v0,v1,v0
    4c2c:	14400032 	bnez	v0,4cf8 <main+0x3628>
    4c30:	00000000 	nop
    4c34:	9fc20004 	lwu	v0,4(s8)
    4c38:	64420010 	daddiu	v0,v0,16
    4c3c:	dfc30010 	ld	v1,16(s8)
    4c40:	0062102d 	daddu	v0,v1,v0
    4c44:	64420008 	daddiu	v0,v0,8
    4c48:	9fc30008 	lwu	v1,8(s8)
    4c4c:	00603025 	move	a2,v1
    4c50:	dfc50018 	ld	a1,24(s8)
    4c54:	00402025 	move	a0,v0
    4c58:	df828280 	ld	v0,-32128(gp)
    4c5c:	0040c825 	move	t9,v0
    4c60:	0320f809 	jalr	t9
    4c64:	00000000 	nop
    4c68:	dfc20010 	ld	v0,16(s8)
    4c6c:	64430008 	daddiu	v1,v0,8
    4c70:	dfc20010 	ld	v0,16(s8)
    4c74:	64420018 	daddiu	v0,v0,24
    4c78:	00402825 	move	a1,v0
    4c7c:	00602025 	move	a0,v1
    4c80:	df828190 	ld	v0,-32368(gp)
    4c84:	0040c825 	move	t9,v0
    4c88:	0411011f 	bal	5108 <main+0x3a38>
    4c8c:	00000000 	nop
    4c90:	8fc20008 	lw	v0,8(s8)
    4c94:	afc20000 	sw	v0,0(s8)
    4c98:	1000000e 	b	4cd4 <main+0x3604>
    4c9c:	00000000 	nop
    4ca0:	dfc20010 	ld	v0,16(s8)
    4ca4:	64440008 	daddiu	a0,v0,8
    4ca8:	9fc20000 	lwu	v0,0(s8)
    4cac:	dfc30018 	ld	v1,24(s8)
    4cb0:	0062102d 	daddu	v0,v1,v0
    4cb4:	00402825 	move	a1,v0
    4cb8:	df828190 	ld	v0,-32368(gp)
    4cbc:	0040c825 	move	t9,v0
    4cc0:	04110111 	bal	5108 <main+0x3a38>
    4cc4:	00000000 	nop
    4cc8:	8fc20000 	lw	v0,0(s8)
    4ccc:	24420040 	addiu	v0,v0,64
    4cd0:	afc20000 	sw	v0,0(s8)
    4cd4:	8fc20000 	lw	v0,0(s8)
    4cd8:	24420040 	addiu	v0,v0,64
    4cdc:	8fc30020 	lw	v1,32(s8)
    4ce0:	0062102b 	sltu	v0,v1,v0
    4ce4:	1040ffee 	beqz	v0,4ca0 <main+0x35d0>
    4ce8:	00000000 	nop
    4cec:	afc00004 	sw	zero,4(s8)
    4cf0:	10000002 	b	4cfc <main+0x362c>
    4cf4:	00000000 	nop
    4cf8:	afc00000 	sw	zero,0(s8)
    4cfc:	9fc20004 	lwu	v0,4(s8)
    4d00:	64420010 	daddiu	v0,v0,16
    4d04:	dfc30010 	ld	v1,16(s8)
    4d08:	0062102d 	daddu	v0,v1,v0
    4d0c:	64440008 	daddiu	a0,v0,8
    4d10:	9fc20000 	lwu	v0,0(s8)
    4d14:	dfc30018 	ld	v1,24(s8)
    4d18:	0062282d 	daddu	a1,v1,v0
    4d1c:	8fc30020 	lw	v1,32(s8)
    4d20:	8fc20000 	lw	v0,0(s8)
    4d24:	00621023 	subu	v0,v1,v0
    4d28:	0002103c 	dsll32	v0,v0,0x0
    4d2c:	0002103e 	dsrl32	v0,v0,0x0
    4d30:	00403025 	move	a2,v0
    4d34:	df828280 	ld	v0,-32128(gp)
    4d38:	0040c825 	move	t9,v0
    4d3c:	0320f809 	jalr	t9
    4d40:	00000000 	nop
    4d44:	00000000 	nop
    4d48:	03c0e825 	move	sp,s8
    4d4c:	dfbf0048 	ld	ra,72(sp)
    4d50:	dfbe0040 	ld	s8,64(sp)
    4d54:	dfbc0038 	ld	gp,56(sp)
    4d58:	67bd0050 	daddiu	sp,sp,80
    4d5c:	03e00008 	jr	ra
    4d60:	00000000 	nop
    4d64:	67bdffc0 	daddiu	sp,sp,-64
    4d68:	ffbf0038 	sd	ra,56(sp)
    4d6c:	ffbe0030 	sd	s8,48(sp)
    4d70:	ffbc0028 	sd	gp,40(sp)
    4d74:	03a0f025 	move	s8,sp
    4d78:	3c1c0002 	lui	gp,0x2
    4d7c:	0399e02d 	daddu	gp,gp,t9
    4d80:	679c32ec 	daddiu	gp,gp,13036
    4d84:	ffc40010 	sd	a0,16(s8)
    4d88:	ffc50018 	sd	a1,24(s8)
    4d8c:	afc00000 	sw	zero,0(s8)
    4d90:	afc00004 	sw	zero,4(s8)
    4d94:	dfc20010 	ld	v0,16(s8)
    4d98:	8c420000 	lw	v0,0(v0)
    4d9c:	000210c2 	srl	v0,v0,0x3
    4da0:	3042003f 	andi	v0,v0,0x3f
    4da4:	afc20000 	sw	v0,0(s8)
    4da8:	8fc20000 	lw	v0,0(s8)
    4dac:	2c420038 	sltiu	v0,v0,56
    4db0:	10400006 	beqz	v0,4dcc <main+0x36fc>
    4db4:	00000000 	nop
    4db8:	24030038 	li	v1,56
    4dbc:	8fc20000 	lw	v0,0(s8)
    4dc0:	00621023 	subu	v0,v1,v0
    4dc4:	10000004 	b	4dd8 <main+0x3708>
    4dc8:	00000000 	nop
    4dcc:	24030078 	li	v1,120
    4dd0:	8fc20000 	lw	v0,0(s8)
    4dd4:	00621023 	subu	v0,v1,v0
    4dd8:	afc20004 	sw	v0,4(s8)
    4ddc:	dfc20010 	ld	v0,16(s8)
    4de0:	67c30008 	daddiu	v1,s8,8
    4de4:	24060008 	li	a2,8
    4de8:	00402825 	move	a1,v0
    4dec:	00602025 	move	a0,v1
    4df0:	df828198 	ld	v0,-32360(gp)
    4df4:	0040c825 	move	t9,v0
    4df8:	04110022 	bal	4e84 <main+0x37b4>
    4dfc:	00000000 	nop
    4e00:	8fc20004 	lw	v0,4(s8)
    4e04:	00403025 	move	a2,v0
    4e08:	df8581a0 	ld	a1,-32352(gp)
    4e0c:	dfc40010 	ld	a0,16(s8)
    4e10:	df8280e8 	ld	v0,-32536(gp)
    4e14:	0040c825 	move	t9,v0
    4e18:	0411ff4b 	bal	4b48 <main+0x3478>
    4e1c:	00000000 	nop
    4e20:	67c20008 	daddiu	v0,s8,8
    4e24:	24060008 	li	a2,8
    4e28:	00402825 	move	a1,v0
    4e2c:	dfc40010 	ld	a0,16(s8)
    4e30:	df8280e8 	ld	v0,-32536(gp)
    4e34:	0040c825 	move	t9,v0
    4e38:	0411ff43 	bal	4b48 <main+0x3478>
    4e3c:	00000000 	nop
    4e40:	dfc20010 	ld	v0,16(s8)
    4e44:	64420008 	daddiu	v0,v0,8
    4e48:	24060010 	li	a2,16
    4e4c:	00402825 	move	a1,v0
    4e50:	dfc40018 	ld	a0,24(s8)
    4e54:	df828198 	ld	v0,-32360(gp)
    4e58:	0040c825 	move	t9,v0
    4e5c:	04110009 	bal	4e84 <main+0x37b4>
    4e60:	00000000 	nop
    4e64:	00000000 	nop
    4e68:	03c0e825 	move	sp,s8
    4e6c:	dfbf0038 	ld	ra,56(sp)
    4e70:	dfbe0030 	ld	s8,48(sp)
    4e74:	dfbc0028 	ld	gp,40(sp)
    4e78:	67bd0040 	daddiu	sp,sp,64
    4e7c:	03e00008 	jr	ra
    4e80:	00000000 	nop
    4e84:	67bdffc0 	daddiu	sp,sp,-64
    4e88:	ffbe0038 	sd	s8,56(sp)
    4e8c:	03a0f025 	move	s8,sp
    4e90:	ffc40010 	sd	a0,16(s8)
    4e94:	ffc50018 	sd	a1,24(s8)
    4e98:	00c01025 	move	v0,a2
    4e9c:	00021000 	sll	v0,v0,0x0
    4ea0:	afc20020 	sw	v0,32(s8)
    4ea4:	afc00000 	sw	zero,0(s8)
    4ea8:	afc00004 	sw	zero,4(s8)
    4eac:	10000042 	b	4fb8 <main+0x38e8>
    4eb0:	00000000 	nop
    4eb4:	9fc20000 	lwu	v0,0(s8)
    4eb8:	000210b8 	dsll	v0,v0,0x2
    4ebc:	dfc30018 	ld	v1,24(s8)
    4ec0:	0062102d 	daddu	v0,v1,v0
    4ec4:	8c440000 	lw	a0,0(v0)
    4ec8:	9fc20004 	lwu	v0,4(s8)
    4ecc:	dfc30010 	ld	v1,16(s8)
    4ed0:	0062102d 	daddu	v0,v1,v0
    4ed4:	00801825 	move	v1,a0
    4ed8:	306300ff 	andi	v1,v1,0xff
    4edc:	a0430000 	sb	v1,0(v0)
    4ee0:	9fc20000 	lwu	v0,0(s8)
    4ee4:	000210b8 	dsll	v0,v0,0x2
    4ee8:	dfc30018 	ld	v1,24(s8)
    4eec:	0062102d 	daddu	v0,v1,v0
    4ef0:	8c420000 	lw	v0,0(v0)
    4ef4:	00021202 	srl	v0,v0,0x8
    4ef8:	00402025 	move	a0,v0
    4efc:	8fc20004 	lw	v0,4(s8)
    4f00:	24420001 	addiu	v0,v0,1
    4f04:	0002103c 	dsll32	v0,v0,0x0
    4f08:	0002103e 	dsrl32	v0,v0,0x0
    4f0c:	dfc30010 	ld	v1,16(s8)
    4f10:	0062102d 	daddu	v0,v1,v0
    4f14:	00801825 	move	v1,a0
    4f18:	306300ff 	andi	v1,v1,0xff
    4f1c:	a0430000 	sb	v1,0(v0)
    4f20:	9fc20000 	lwu	v0,0(s8)
    4f24:	000210b8 	dsll	v0,v0,0x2
    4f28:	dfc30018 	ld	v1,24(s8)
    4f2c:	0062102d 	daddu	v0,v1,v0
    4f30:	8c420000 	lw	v0,0(v0)
    4f34:	00021402 	srl	v0,v0,0x10
    4f38:	00402025 	move	a0,v0
    4f3c:	8fc20004 	lw	v0,4(s8)
    4f40:	24420002 	addiu	v0,v0,2
    4f44:	0002103c 	dsll32	v0,v0,0x0
    4f48:	0002103e 	dsrl32	v0,v0,0x0
    4f4c:	dfc30010 	ld	v1,16(s8)
    4f50:	0062102d 	daddu	v0,v1,v0
    4f54:	00801825 	move	v1,a0
    4f58:	306300ff 	andi	v1,v1,0xff
    4f5c:	a0430000 	sb	v1,0(v0)
    4f60:	9fc20000 	lwu	v0,0(s8)
    4f64:	000210b8 	dsll	v0,v0,0x2
    4f68:	dfc30018 	ld	v1,24(s8)
    4f6c:	0062102d 	daddu	v0,v1,v0
    4f70:	8c420000 	lw	v0,0(v0)
    4f74:	00021602 	srl	v0,v0,0x18
    4f78:	00402025 	move	a0,v0
    4f7c:	8fc20004 	lw	v0,4(s8)
    4f80:	24420003 	addiu	v0,v0,3
    4f84:	0002103c 	dsll32	v0,v0,0x0
    4f88:	0002103e 	dsrl32	v0,v0,0x0
    4f8c:	dfc30010 	ld	v1,16(s8)
    4f90:	0062102d 	daddu	v0,v1,v0
    4f94:	00801825 	move	v1,a0
    4f98:	306300ff 	andi	v1,v1,0xff
    4f9c:	a0430000 	sb	v1,0(v0)
    4fa0:	8fc20000 	lw	v0,0(s8)
    4fa4:	24420001 	addiu	v0,v0,1
    4fa8:	afc20000 	sw	v0,0(s8)
    4fac:	8fc20004 	lw	v0,4(s8)
    4fb0:	24420004 	addiu	v0,v0,4
    4fb4:	afc20004 	sw	v0,4(s8)
    4fb8:	8fc30004 	lw	v1,4(s8)
    4fbc:	8fc20020 	lw	v0,32(s8)
    4fc0:	0062102b 	sltu	v0,v1,v0
    4fc4:	1440ffbb 	bnez	v0,4eb4 <main+0x37e4>
    4fc8:	00000000 	nop
	...
    4fd4:	03c0e825 	move	sp,s8
    4fd8:	dfbe0038 	ld	s8,56(sp)
    4fdc:	67bd0040 	daddiu	sp,sp,64
    4fe0:	03e00008 	jr	ra
    4fe4:	00000000 	nop
    4fe8:	67bdffc0 	daddiu	sp,sp,-64
    4fec:	ffbe0038 	sd	s8,56(sp)
    4ff0:	03a0f025 	move	s8,sp
    4ff4:	ffc40010 	sd	a0,16(s8)
    4ff8:	ffc50018 	sd	a1,24(s8)
    4ffc:	00c01025 	move	v0,a2
    5000:	00021000 	sll	v0,v0,0x0
    5004:	afc20020 	sw	v0,32(s8)
    5008:	afc00000 	sw	zero,0(s8)
    500c:	afc00004 	sw	zero,4(s8)
    5010:	10000031 	b	50d8 <main+0x3a08>
    5014:	00000000 	nop
    5018:	9fc20004 	lwu	v0,4(s8)
    501c:	dfc30018 	ld	v1,24(s8)
    5020:	0062102d 	daddu	v0,v1,v0
    5024:	90420000 	lbu	v0,0(v0)
    5028:	00401825 	move	v1,v0
    502c:	8fc20004 	lw	v0,4(s8)
    5030:	24420001 	addiu	v0,v0,1
    5034:	0002103c 	dsll32	v0,v0,0x0
    5038:	0002103e 	dsrl32	v0,v0,0x0
    503c:	dfc40018 	ld	a0,24(s8)
    5040:	0082102d 	daddu	v0,a0,v0
    5044:	90420000 	lbu	v0,0(v0)
    5048:	00021200 	sll	v0,v0,0x8
    504c:	00621025 	or	v0,v1,v0
    5050:	00401825 	move	v1,v0
    5054:	8fc20004 	lw	v0,4(s8)
    5058:	24420002 	addiu	v0,v0,2
    505c:	0002103c 	dsll32	v0,v0,0x0
    5060:	0002103e 	dsrl32	v0,v0,0x0
    5064:	dfc40018 	ld	a0,24(s8)
    5068:	0082102d 	daddu	v0,a0,v0
    506c:	90420000 	lbu	v0,0(v0)
    5070:	00021400 	sll	v0,v0,0x10
    5074:	00621025 	or	v0,v1,v0
    5078:	00401825 	move	v1,v0
    507c:	8fc20004 	lw	v0,4(s8)
    5080:	24420003 	addiu	v0,v0,3
    5084:	0002103c 	dsll32	v0,v0,0x0
    5088:	0002103e 	dsrl32	v0,v0,0x0
    508c:	dfc40018 	ld	a0,24(s8)
    5090:	0082102d 	daddu	v0,a0,v0
    5094:	90420000 	lbu	v0,0(v0)
    5098:	00021600 	sll	v0,v0,0x18
    509c:	00621025 	or	v0,v1,v0
    50a0:	00401825 	move	v1,v0
    50a4:	00600013 	mtlo	v1
    50a8:	9fc20000 	lwu	v0,0(s8)
    50ac:	000210b8 	dsll	v0,v0,0x2
    50b0:	dfc30010 	ld	v1,16(s8)
    50b4:	0062102d 	daddu	v0,v1,v0
    50b8:	00001812 	mflo	v1
    50bc:	ac430000 	sw	v1,0(v0)
    50c0:	8fc20000 	lw	v0,0(s8)
    50c4:	24420001 	addiu	v0,v0,1
    50c8:	afc20000 	sw	v0,0(s8)
    50cc:	8fc20004 	lw	v0,4(s8)
    50d0:	24420004 	addiu	v0,v0,4
    50d4:	afc20004 	sw	v0,4(s8)
    50d8:	8fc30004 	lw	v1,4(s8)
    50dc:	8fc20020 	lw	v0,32(s8)
    50e0:	0062102b 	sltu	v0,v1,v0
    50e4:	1440ffcc 	bnez	v0,5018 <main+0x3948>
    50e8:	00000000 	nop
	...
    50f4:	03c0e825 	move	sp,s8
    50f8:	dfbe0038 	ld	s8,56(sp)
    50fc:	67bd0040 	daddiu	sp,sp,64
    5100:	03e00008 	jr	ra
    5104:	00000000 	nop
    5108:	67bdfec0 	daddiu	sp,sp,-320
    510c:	ffbf0138 	sd	ra,312(sp)
    5110:	ffbe0130 	sd	s8,304(sp)
    5114:	ffbc0128 	sd	gp,296(sp)
    5118:	03a0f025 	move	s8,sp
    511c:	3c1c0002 	lui	gp,0x2
    5120:	0399e02d 	daddu	gp,gp,t9
    5124:	679c2f48 	daddiu	gp,gp,12104
    5128:	ffc40110 	sd	a0,272(s8)
    512c:	ffc50118 	sd	a1,280(s8)
    5130:	dfc20110 	ld	v0,272(s8)
    5134:	8c420000 	lw	v0,0(v0)
    5138:	afc20000 	sw	v0,0(s8)
    513c:	dfc20110 	ld	v0,272(s8)
    5140:	8c420004 	lw	v0,4(v0)
    5144:	afc20004 	sw	v0,4(s8)
    5148:	dfc20110 	ld	v0,272(s8)
    514c:	8c420008 	lw	v0,8(v0)
    5150:	afc20008 	sw	v0,8(s8)
    5154:	dfc20110 	ld	v0,272(s8)
    5158:	8c42000c 	lw	v0,12(v0)
    515c:	afc2000c 	sw	v0,12(s8)
    5160:	67c20010 	daddiu	v0,s8,16
    5164:	24060040 	li	a2,64
    5168:	dfc50118 	ld	a1,280(s8)
    516c:	00402025 	move	a0,v0
    5170:	df8281a8 	ld	v0,-32344(gp)
    5174:	0040c825 	move	t9,v0
    5178:	0411ff9b 	bal	4fe8 <main+0x3918>
    517c:	00000000 	nop
    5180:	8fc30004 	lw	v1,4(s8)
    5184:	8fc20008 	lw	v0,8(s8)
    5188:	00621024 	and	v0,v1,v0
    518c:	00401825 	move	v1,v0
    5190:	8fc20004 	lw	v0,4(s8)
    5194:	00021027 	nor	v0,zero,v0
    5198:	8fc4000c 	lw	a0,12(s8)
    519c:	00821024 	and	v0,a0,v0
    51a0:	00621025 	or	v0,v1,v0
    51a4:	00401825 	move	v1,v0
    51a8:	8fc20010 	lw	v0,16(s8)
    51ac:	00621021 	addu	v0,v1,v0
    51b0:	8fc30000 	lw	v1,0(s8)
    51b4:	00621021 	addu	v0,v1,v0
    51b8:	00401825 	move	v1,v0
    51bc:	3c02d76a 	lui	v0,0xd76a
    51c0:	3442a478 	ori	v0,v0,0xa478
    51c4:	00621021 	addu	v0,v1,v0
    51c8:	afc20000 	sw	v0,0(s8)
    51cc:	8fc20000 	lw	v0,0(s8)
    51d0:	000219c0 	sll	v1,v0,0x7
    51d4:	00021642 	srl	v0,v0,0x19
    51d8:	00621025 	or	v0,v1,v0
    51dc:	afc20000 	sw	v0,0(s8)
    51e0:	8fc30000 	lw	v1,0(s8)
    51e4:	8fc20004 	lw	v0,4(s8)
    51e8:	00621021 	addu	v0,v1,v0
    51ec:	afc20000 	sw	v0,0(s8)
    51f0:	8fc30000 	lw	v1,0(s8)
    51f4:	8fc20004 	lw	v0,4(s8)
    51f8:	00621024 	and	v0,v1,v0
    51fc:	00401825 	move	v1,v0
    5200:	8fc20000 	lw	v0,0(s8)
    5204:	00021027 	nor	v0,zero,v0
    5208:	8fc40008 	lw	a0,8(s8)
    520c:	00821024 	and	v0,a0,v0
    5210:	00621025 	or	v0,v1,v0
    5214:	00401825 	move	v1,v0
    5218:	8fc20014 	lw	v0,20(s8)
    521c:	00621021 	addu	v0,v1,v0
    5220:	8fc3000c 	lw	v1,12(s8)
    5224:	00621021 	addu	v0,v1,v0
    5228:	00401825 	move	v1,v0
    522c:	3c02e8c7 	lui	v0,0xe8c7
    5230:	3442b756 	ori	v0,v0,0xb756
    5234:	00621021 	addu	v0,v1,v0
    5238:	afc2000c 	sw	v0,12(s8)
    523c:	8fc2000c 	lw	v0,12(s8)
    5240:	00021b00 	sll	v1,v0,0xc
    5244:	00021502 	srl	v0,v0,0x14
    5248:	00621025 	or	v0,v1,v0
    524c:	afc2000c 	sw	v0,12(s8)
    5250:	8fc3000c 	lw	v1,12(s8)
    5254:	8fc20000 	lw	v0,0(s8)
    5258:	00621021 	addu	v0,v1,v0
    525c:	afc2000c 	sw	v0,12(s8)
    5260:	8fc3000c 	lw	v1,12(s8)
    5264:	8fc20000 	lw	v0,0(s8)
    5268:	00621024 	and	v0,v1,v0
    526c:	00401825 	move	v1,v0
    5270:	8fc2000c 	lw	v0,12(s8)
    5274:	00021027 	nor	v0,zero,v0
    5278:	8fc40004 	lw	a0,4(s8)
    527c:	00821024 	and	v0,a0,v0
    5280:	00621025 	or	v0,v1,v0
    5284:	00401825 	move	v1,v0
    5288:	8fc20018 	lw	v0,24(s8)
    528c:	00621021 	addu	v0,v1,v0
    5290:	8fc30008 	lw	v1,8(s8)
    5294:	00621021 	addu	v0,v1,v0
    5298:	00401825 	move	v1,v0
    529c:	3c022420 	lui	v0,0x2420
    52a0:	344270db 	ori	v0,v0,0x70db
    52a4:	00621021 	addu	v0,v1,v0
    52a8:	afc20008 	sw	v0,8(s8)
    52ac:	8fc20008 	lw	v0,8(s8)
    52b0:	00021bc2 	srl	v1,v0,0xf
    52b4:	00021440 	sll	v0,v0,0x11
    52b8:	00621025 	or	v0,v1,v0
    52bc:	afc20008 	sw	v0,8(s8)
    52c0:	8fc30008 	lw	v1,8(s8)
    52c4:	8fc2000c 	lw	v0,12(s8)
    52c8:	00621021 	addu	v0,v1,v0
    52cc:	afc20008 	sw	v0,8(s8)
    52d0:	8fc30008 	lw	v1,8(s8)
    52d4:	8fc2000c 	lw	v0,12(s8)
    52d8:	00621024 	and	v0,v1,v0
    52dc:	00401825 	move	v1,v0
    52e0:	8fc20008 	lw	v0,8(s8)
    52e4:	00021027 	nor	v0,zero,v0
    52e8:	8fc40000 	lw	a0,0(s8)
    52ec:	00821024 	and	v0,a0,v0
    52f0:	00621025 	or	v0,v1,v0
    52f4:	00401825 	move	v1,v0
    52f8:	8fc2001c 	lw	v0,28(s8)
    52fc:	00621021 	addu	v0,v1,v0
    5300:	8fc30004 	lw	v1,4(s8)
    5304:	00621021 	addu	v0,v1,v0
    5308:	00401825 	move	v1,v0
    530c:	3c02c1bd 	lui	v0,0xc1bd
    5310:	3442ceee 	ori	v0,v0,0xceee
    5314:	00621021 	addu	v0,v1,v0
    5318:	afc20004 	sw	v0,4(s8)
    531c:	8fc20004 	lw	v0,4(s8)
    5320:	00021a82 	srl	v1,v0,0xa
    5324:	00021580 	sll	v0,v0,0x16
    5328:	00621025 	or	v0,v1,v0
    532c:	afc20004 	sw	v0,4(s8)
    5330:	8fc30004 	lw	v1,4(s8)
    5334:	8fc20008 	lw	v0,8(s8)
    5338:	00621021 	addu	v0,v1,v0
    533c:	afc20004 	sw	v0,4(s8)
    5340:	8fc30004 	lw	v1,4(s8)
    5344:	8fc20008 	lw	v0,8(s8)
    5348:	00621024 	and	v0,v1,v0
    534c:	00401825 	move	v1,v0
    5350:	8fc20004 	lw	v0,4(s8)
    5354:	00021027 	nor	v0,zero,v0
    5358:	8fc4000c 	lw	a0,12(s8)
    535c:	00821024 	and	v0,a0,v0
    5360:	00621025 	or	v0,v1,v0
    5364:	00401825 	move	v1,v0
    5368:	8fc20020 	lw	v0,32(s8)
    536c:	00621021 	addu	v0,v1,v0
    5370:	8fc30000 	lw	v1,0(s8)
    5374:	00621021 	addu	v0,v1,v0
    5378:	00401825 	move	v1,v0
    537c:	3c02f57c 	lui	v0,0xf57c
    5380:	34420faf 	ori	v0,v0,0xfaf
    5384:	00621021 	addu	v0,v1,v0
    5388:	afc20000 	sw	v0,0(s8)
    538c:	8fc20000 	lw	v0,0(s8)
    5390:	000219c0 	sll	v1,v0,0x7
    5394:	00021642 	srl	v0,v0,0x19
    5398:	00621025 	or	v0,v1,v0
    539c:	afc20000 	sw	v0,0(s8)
    53a0:	8fc30000 	lw	v1,0(s8)
    53a4:	8fc20004 	lw	v0,4(s8)
    53a8:	00621021 	addu	v0,v1,v0
    53ac:	afc20000 	sw	v0,0(s8)
    53b0:	8fc30000 	lw	v1,0(s8)
    53b4:	8fc20004 	lw	v0,4(s8)
    53b8:	00621024 	and	v0,v1,v0
    53bc:	00401825 	move	v1,v0
    53c0:	8fc20000 	lw	v0,0(s8)
    53c4:	00021027 	nor	v0,zero,v0
    53c8:	8fc40008 	lw	a0,8(s8)
    53cc:	00821024 	and	v0,a0,v0
    53d0:	00621025 	or	v0,v1,v0
    53d4:	00401825 	move	v1,v0
    53d8:	8fc20024 	lw	v0,36(s8)
    53dc:	00621021 	addu	v0,v1,v0
    53e0:	8fc3000c 	lw	v1,12(s8)
    53e4:	00621021 	addu	v0,v1,v0
    53e8:	00401825 	move	v1,v0
    53ec:	3c024787 	lui	v0,0x4787
    53f0:	3442c62a 	ori	v0,v0,0xc62a
    53f4:	00621021 	addu	v0,v1,v0
    53f8:	afc2000c 	sw	v0,12(s8)
    53fc:	8fc2000c 	lw	v0,12(s8)
    5400:	00021b00 	sll	v1,v0,0xc
    5404:	00021502 	srl	v0,v0,0x14
    5408:	00621025 	or	v0,v1,v0
    540c:	afc2000c 	sw	v0,12(s8)
    5410:	8fc3000c 	lw	v1,12(s8)
    5414:	8fc20000 	lw	v0,0(s8)
    5418:	00621021 	addu	v0,v1,v0
    541c:	afc2000c 	sw	v0,12(s8)
    5420:	8fc3000c 	lw	v1,12(s8)
    5424:	8fc20000 	lw	v0,0(s8)
    5428:	00621024 	and	v0,v1,v0
    542c:	00401825 	move	v1,v0
    5430:	8fc2000c 	lw	v0,12(s8)
    5434:	00021027 	nor	v0,zero,v0
    5438:	8fc40004 	lw	a0,4(s8)
    543c:	00821024 	and	v0,a0,v0
    5440:	00621025 	or	v0,v1,v0
    5444:	00401825 	move	v1,v0
    5448:	8fc20028 	lw	v0,40(s8)
    544c:	00621021 	addu	v0,v1,v0
    5450:	8fc30008 	lw	v1,8(s8)
    5454:	00621021 	addu	v0,v1,v0
    5458:	00401825 	move	v1,v0
    545c:	3c02a830 	lui	v0,0xa830
    5460:	34424613 	ori	v0,v0,0x4613
    5464:	00621021 	addu	v0,v1,v0
    5468:	afc20008 	sw	v0,8(s8)
    546c:	8fc20008 	lw	v0,8(s8)
    5470:	00021bc2 	srl	v1,v0,0xf
    5474:	00021440 	sll	v0,v0,0x11
    5478:	00621025 	or	v0,v1,v0
    547c:	afc20008 	sw	v0,8(s8)
    5480:	8fc30008 	lw	v1,8(s8)
    5484:	8fc2000c 	lw	v0,12(s8)
    5488:	00621021 	addu	v0,v1,v0
    548c:	afc20008 	sw	v0,8(s8)
    5490:	8fc30008 	lw	v1,8(s8)
    5494:	8fc2000c 	lw	v0,12(s8)
    5498:	00621024 	and	v0,v1,v0
    549c:	00401825 	move	v1,v0
    54a0:	8fc20008 	lw	v0,8(s8)
    54a4:	00021027 	nor	v0,zero,v0
    54a8:	8fc40000 	lw	a0,0(s8)
    54ac:	00821024 	and	v0,a0,v0
    54b0:	00621025 	or	v0,v1,v0
    54b4:	00401825 	move	v1,v0
    54b8:	8fc2002c 	lw	v0,44(s8)
    54bc:	00621021 	addu	v0,v1,v0
    54c0:	8fc30004 	lw	v1,4(s8)
    54c4:	00621021 	addu	v0,v1,v0
    54c8:	00401825 	move	v1,v0
    54cc:	3c02fd46 	lui	v0,0xfd46
    54d0:	34429501 	ori	v0,v0,0x9501
    54d4:	00621021 	addu	v0,v1,v0
    54d8:	afc20004 	sw	v0,4(s8)
    54dc:	8fc20004 	lw	v0,4(s8)
    54e0:	00021a82 	srl	v1,v0,0xa
    54e4:	00021580 	sll	v0,v0,0x16
    54e8:	00621025 	or	v0,v1,v0
    54ec:	afc20004 	sw	v0,4(s8)
    54f0:	8fc30004 	lw	v1,4(s8)
    54f4:	8fc20008 	lw	v0,8(s8)
    54f8:	00621021 	addu	v0,v1,v0
    54fc:	afc20004 	sw	v0,4(s8)
    5500:	8fc30004 	lw	v1,4(s8)
    5504:	8fc20008 	lw	v0,8(s8)
    5508:	00621024 	and	v0,v1,v0
    550c:	00401825 	move	v1,v0
    5510:	8fc20004 	lw	v0,4(s8)
    5514:	00021027 	nor	v0,zero,v0
    5518:	8fc4000c 	lw	a0,12(s8)
    551c:	00821024 	and	v0,a0,v0
    5520:	00621025 	or	v0,v1,v0
    5524:	00401825 	move	v1,v0
    5528:	8fc20030 	lw	v0,48(s8)
    552c:	00621021 	addu	v0,v1,v0
    5530:	8fc30000 	lw	v1,0(s8)
    5534:	00621021 	addu	v0,v1,v0
    5538:	00401825 	move	v1,v0
    553c:	3c026980 	lui	v0,0x6980
    5540:	344298d8 	ori	v0,v0,0x98d8
    5544:	00621021 	addu	v0,v1,v0
    5548:	afc20000 	sw	v0,0(s8)
    554c:	8fc20000 	lw	v0,0(s8)
    5550:	000219c0 	sll	v1,v0,0x7
    5554:	00021642 	srl	v0,v0,0x19
    5558:	00621025 	or	v0,v1,v0
    555c:	afc20000 	sw	v0,0(s8)
    5560:	8fc30000 	lw	v1,0(s8)
    5564:	8fc20004 	lw	v0,4(s8)
    5568:	00621021 	addu	v0,v1,v0
    556c:	afc20000 	sw	v0,0(s8)
    5570:	8fc30000 	lw	v1,0(s8)
    5574:	8fc20004 	lw	v0,4(s8)
    5578:	00621024 	and	v0,v1,v0
    557c:	00401825 	move	v1,v0
    5580:	8fc20000 	lw	v0,0(s8)
    5584:	00021027 	nor	v0,zero,v0
    5588:	8fc40008 	lw	a0,8(s8)
    558c:	00821024 	and	v0,a0,v0
    5590:	00621025 	or	v0,v1,v0
    5594:	00401825 	move	v1,v0
    5598:	8fc20034 	lw	v0,52(s8)
    559c:	00621021 	addu	v0,v1,v0
    55a0:	8fc3000c 	lw	v1,12(s8)
    55a4:	00621021 	addu	v0,v1,v0
    55a8:	00401825 	move	v1,v0
    55ac:	3c028b44 	lui	v0,0x8b44
    55b0:	3442f7af 	ori	v0,v0,0xf7af
    55b4:	00621021 	addu	v0,v1,v0
    55b8:	afc2000c 	sw	v0,12(s8)
    55bc:	8fc2000c 	lw	v0,12(s8)
    55c0:	00021b00 	sll	v1,v0,0xc
    55c4:	00021502 	srl	v0,v0,0x14
    55c8:	00621025 	or	v0,v1,v0
    55cc:	afc2000c 	sw	v0,12(s8)
    55d0:	8fc3000c 	lw	v1,12(s8)
    55d4:	8fc20000 	lw	v0,0(s8)
    55d8:	00621021 	addu	v0,v1,v0
    55dc:	afc2000c 	sw	v0,12(s8)
    55e0:	8fc3000c 	lw	v1,12(s8)
    55e4:	8fc20000 	lw	v0,0(s8)
    55e8:	00621024 	and	v0,v1,v0
    55ec:	00401825 	move	v1,v0
    55f0:	8fc2000c 	lw	v0,12(s8)
    55f4:	00021027 	nor	v0,zero,v0
    55f8:	8fc40004 	lw	a0,4(s8)
    55fc:	00821024 	and	v0,a0,v0
    5600:	00621025 	or	v0,v1,v0
    5604:	00401825 	move	v1,v0
    5608:	8fc20038 	lw	v0,56(s8)
    560c:	00621021 	addu	v0,v1,v0
    5610:	8fc30008 	lw	v1,8(s8)
    5614:	00621021 	addu	v0,v1,v0
    5618:	00401825 	move	v1,v0
    561c:	3c02ffff 	lui	v0,0xffff
    5620:	34425bb1 	ori	v0,v0,0x5bb1
    5624:	00621021 	addu	v0,v1,v0
    5628:	afc20008 	sw	v0,8(s8)
    562c:	8fc20008 	lw	v0,8(s8)
    5630:	00021bc2 	srl	v1,v0,0xf
    5634:	00021440 	sll	v0,v0,0x11
    5638:	00621025 	or	v0,v1,v0
    563c:	afc20008 	sw	v0,8(s8)
    5640:	8fc30008 	lw	v1,8(s8)
    5644:	8fc2000c 	lw	v0,12(s8)
    5648:	00621021 	addu	v0,v1,v0
    564c:	afc20008 	sw	v0,8(s8)
    5650:	8fc30008 	lw	v1,8(s8)
    5654:	8fc2000c 	lw	v0,12(s8)
    5658:	00621024 	and	v0,v1,v0
    565c:	00401825 	move	v1,v0
    5660:	8fc20008 	lw	v0,8(s8)
    5664:	00021027 	nor	v0,zero,v0
    5668:	8fc40000 	lw	a0,0(s8)
    566c:	00821024 	and	v0,a0,v0
    5670:	00621025 	or	v0,v1,v0
    5674:	00401825 	move	v1,v0
    5678:	8fc2003c 	lw	v0,60(s8)
    567c:	00621021 	addu	v0,v1,v0
    5680:	8fc30004 	lw	v1,4(s8)
    5684:	00621021 	addu	v0,v1,v0
    5688:	00401825 	move	v1,v0
    568c:	3c02895c 	lui	v0,0x895c
    5690:	3442d7be 	ori	v0,v0,0xd7be
    5694:	00621021 	addu	v0,v1,v0
    5698:	afc20004 	sw	v0,4(s8)
    569c:	8fc20004 	lw	v0,4(s8)
    56a0:	00021a82 	srl	v1,v0,0xa
    56a4:	00021580 	sll	v0,v0,0x16
    56a8:	00621025 	or	v0,v1,v0
    56ac:	afc20004 	sw	v0,4(s8)
    56b0:	8fc30004 	lw	v1,4(s8)
    56b4:	8fc20008 	lw	v0,8(s8)
    56b8:	00621021 	addu	v0,v1,v0
    56bc:	afc20004 	sw	v0,4(s8)
    56c0:	8fc30004 	lw	v1,4(s8)
    56c4:	8fc20008 	lw	v0,8(s8)
    56c8:	00621024 	and	v0,v1,v0
    56cc:	00401825 	move	v1,v0
    56d0:	8fc20004 	lw	v0,4(s8)
    56d4:	00021027 	nor	v0,zero,v0
    56d8:	8fc4000c 	lw	a0,12(s8)
    56dc:	00821024 	and	v0,a0,v0
    56e0:	00621025 	or	v0,v1,v0
    56e4:	00401825 	move	v1,v0
    56e8:	8fc20040 	lw	v0,64(s8)
    56ec:	00621021 	addu	v0,v1,v0
    56f0:	8fc30000 	lw	v1,0(s8)
    56f4:	00621021 	addu	v0,v1,v0
    56f8:	00401825 	move	v1,v0
    56fc:	3c026b90 	lui	v0,0x6b90
    5700:	34421122 	ori	v0,v0,0x1122
    5704:	00621021 	addu	v0,v1,v0
    5708:	afc20000 	sw	v0,0(s8)
    570c:	8fc20000 	lw	v0,0(s8)
    5710:	000219c0 	sll	v1,v0,0x7
    5714:	00021642 	srl	v0,v0,0x19
    5718:	00621025 	or	v0,v1,v0
    571c:	afc20000 	sw	v0,0(s8)
    5720:	8fc30000 	lw	v1,0(s8)
    5724:	8fc20004 	lw	v0,4(s8)
    5728:	00621021 	addu	v0,v1,v0
    572c:	afc20000 	sw	v0,0(s8)
    5730:	8fc30000 	lw	v1,0(s8)
    5734:	8fc20004 	lw	v0,4(s8)
    5738:	00621024 	and	v0,v1,v0
    573c:	00401825 	move	v1,v0
    5740:	8fc20000 	lw	v0,0(s8)
    5744:	00021027 	nor	v0,zero,v0
    5748:	8fc40008 	lw	a0,8(s8)
    574c:	00821024 	and	v0,a0,v0
    5750:	00621025 	or	v0,v1,v0
    5754:	00401825 	move	v1,v0
    5758:	8fc20044 	lw	v0,68(s8)
    575c:	00621021 	addu	v0,v1,v0
    5760:	8fc3000c 	lw	v1,12(s8)
    5764:	00621021 	addu	v0,v1,v0
    5768:	00401825 	move	v1,v0
    576c:	3c02fd98 	lui	v0,0xfd98
    5770:	34427193 	ori	v0,v0,0x7193
    5774:	00621021 	addu	v0,v1,v0
    5778:	afc2000c 	sw	v0,12(s8)
    577c:	8fc2000c 	lw	v0,12(s8)
    5780:	00021b00 	sll	v1,v0,0xc
    5784:	00021502 	srl	v0,v0,0x14
    5788:	00621025 	or	v0,v1,v0
    578c:	afc2000c 	sw	v0,12(s8)
    5790:	8fc3000c 	lw	v1,12(s8)
    5794:	8fc20000 	lw	v0,0(s8)
    5798:	00621021 	addu	v0,v1,v0
    579c:	afc2000c 	sw	v0,12(s8)
    57a0:	8fc3000c 	lw	v1,12(s8)
    57a4:	8fc20000 	lw	v0,0(s8)
    57a8:	00621024 	and	v0,v1,v0
    57ac:	00401825 	move	v1,v0
    57b0:	8fc2000c 	lw	v0,12(s8)
    57b4:	00021027 	nor	v0,zero,v0
    57b8:	8fc40004 	lw	a0,4(s8)
    57bc:	00821024 	and	v0,a0,v0
    57c0:	00621025 	or	v0,v1,v0
    57c4:	00401825 	move	v1,v0
    57c8:	8fc20048 	lw	v0,72(s8)
    57cc:	00621021 	addu	v0,v1,v0
    57d0:	8fc30008 	lw	v1,8(s8)
    57d4:	00621021 	addu	v0,v1,v0
    57d8:	00401825 	move	v1,v0
    57dc:	3c02a679 	lui	v0,0xa679
    57e0:	3442438e 	ori	v0,v0,0x438e
    57e4:	00621021 	addu	v0,v1,v0
    57e8:	afc20008 	sw	v0,8(s8)
    57ec:	8fc20008 	lw	v0,8(s8)
    57f0:	00021bc2 	srl	v1,v0,0xf
    57f4:	00021440 	sll	v0,v0,0x11
    57f8:	00621025 	or	v0,v1,v0
    57fc:	afc20008 	sw	v0,8(s8)
    5800:	8fc30008 	lw	v1,8(s8)
    5804:	8fc2000c 	lw	v0,12(s8)
    5808:	00621021 	addu	v0,v1,v0
    580c:	afc20008 	sw	v0,8(s8)
    5810:	8fc30008 	lw	v1,8(s8)
    5814:	8fc2000c 	lw	v0,12(s8)
    5818:	00621024 	and	v0,v1,v0
    581c:	00401825 	move	v1,v0
    5820:	8fc20008 	lw	v0,8(s8)
    5824:	00021027 	nor	v0,zero,v0
    5828:	8fc40000 	lw	a0,0(s8)
    582c:	00821024 	and	v0,a0,v0
    5830:	00621025 	or	v0,v1,v0
    5834:	00401825 	move	v1,v0
    5838:	8fc2004c 	lw	v0,76(s8)
    583c:	00621021 	addu	v0,v1,v0
    5840:	8fc30004 	lw	v1,4(s8)
    5844:	00621021 	addu	v0,v1,v0
    5848:	00401825 	move	v1,v0
    584c:	3c0249b4 	lui	v0,0x49b4
    5850:	34420821 	ori	v0,v0,0x821
    5854:	00621021 	addu	v0,v1,v0
    5858:	afc20004 	sw	v0,4(s8)
    585c:	8fc20004 	lw	v0,4(s8)
    5860:	00021a82 	srl	v1,v0,0xa
    5864:	00021580 	sll	v0,v0,0x16
    5868:	00621025 	or	v0,v1,v0
    586c:	afc20004 	sw	v0,4(s8)
    5870:	8fc30004 	lw	v1,4(s8)
    5874:	8fc20008 	lw	v0,8(s8)
    5878:	00621021 	addu	v0,v1,v0
    587c:	afc20004 	sw	v0,4(s8)
    5880:	8fc30004 	lw	v1,4(s8)
    5884:	8fc2000c 	lw	v0,12(s8)
    5888:	00621024 	and	v0,v1,v0
    588c:	00401825 	move	v1,v0
    5890:	8fc2000c 	lw	v0,12(s8)
    5894:	00021027 	nor	v0,zero,v0
    5898:	8fc40008 	lw	a0,8(s8)
    589c:	00821024 	and	v0,a0,v0
    58a0:	00621025 	or	v0,v1,v0
    58a4:	00401825 	move	v1,v0
    58a8:	8fc20014 	lw	v0,20(s8)
    58ac:	00621021 	addu	v0,v1,v0
    58b0:	8fc30000 	lw	v1,0(s8)
    58b4:	00621021 	addu	v0,v1,v0
    58b8:	00401825 	move	v1,v0
    58bc:	3c02f61e 	lui	v0,0xf61e
    58c0:	34422562 	ori	v0,v0,0x2562
    58c4:	00621021 	addu	v0,v1,v0
    58c8:	afc20000 	sw	v0,0(s8)
    58cc:	8fc20000 	lw	v0,0(s8)
    58d0:	00021940 	sll	v1,v0,0x5
    58d4:	000216c2 	srl	v0,v0,0x1b
    58d8:	00621025 	or	v0,v1,v0
    58dc:	afc20000 	sw	v0,0(s8)
    58e0:	8fc30000 	lw	v1,0(s8)
    58e4:	8fc20004 	lw	v0,4(s8)
    58e8:	00621021 	addu	v0,v1,v0
    58ec:	afc20000 	sw	v0,0(s8)
    58f0:	8fc30000 	lw	v1,0(s8)
    58f4:	8fc20008 	lw	v0,8(s8)
    58f8:	00621024 	and	v0,v1,v0
    58fc:	00401825 	move	v1,v0
    5900:	8fc20008 	lw	v0,8(s8)
    5904:	00021027 	nor	v0,zero,v0
    5908:	8fc40004 	lw	a0,4(s8)
    590c:	00821024 	and	v0,a0,v0
    5910:	00621025 	or	v0,v1,v0
    5914:	00401825 	move	v1,v0
    5918:	8fc20028 	lw	v0,40(s8)
    591c:	00621021 	addu	v0,v1,v0
    5920:	8fc3000c 	lw	v1,12(s8)
    5924:	00621021 	addu	v0,v1,v0
    5928:	00401825 	move	v1,v0
    592c:	3c02c040 	lui	v0,0xc040
    5930:	3442b340 	ori	v0,v0,0xb340
    5934:	00621021 	addu	v0,v1,v0
    5938:	afc2000c 	sw	v0,12(s8)
    593c:	8fc2000c 	lw	v0,12(s8)
    5940:	00021a40 	sll	v1,v0,0x9
    5944:	000215c2 	srl	v0,v0,0x17
    5948:	00621025 	or	v0,v1,v0
    594c:	afc2000c 	sw	v0,12(s8)
    5950:	8fc3000c 	lw	v1,12(s8)
    5954:	8fc20000 	lw	v0,0(s8)
    5958:	00621021 	addu	v0,v1,v0
    595c:	afc2000c 	sw	v0,12(s8)
    5960:	8fc3000c 	lw	v1,12(s8)
    5964:	8fc20004 	lw	v0,4(s8)
    5968:	00621024 	and	v0,v1,v0
    596c:	00401825 	move	v1,v0
    5970:	8fc20004 	lw	v0,4(s8)
    5974:	00021027 	nor	v0,zero,v0
    5978:	8fc40000 	lw	a0,0(s8)
    597c:	00821024 	and	v0,a0,v0
    5980:	00621025 	or	v0,v1,v0
    5984:	00401825 	move	v1,v0
    5988:	8fc2003c 	lw	v0,60(s8)
    598c:	00621021 	addu	v0,v1,v0
    5990:	8fc30008 	lw	v1,8(s8)
    5994:	00621021 	addu	v0,v1,v0
    5998:	00401825 	move	v1,v0
    599c:	3c02265e 	lui	v0,0x265e
    59a0:	34425a51 	ori	v0,v0,0x5a51
    59a4:	00621021 	addu	v0,v1,v0
    59a8:	afc20008 	sw	v0,8(s8)
    59ac:	8fc20008 	lw	v0,8(s8)
    59b0:	00021b80 	sll	v1,v0,0xe
    59b4:	00021482 	srl	v0,v0,0x12
    59b8:	00621025 	or	v0,v1,v0
    59bc:	afc20008 	sw	v0,8(s8)
    59c0:	8fc30008 	lw	v1,8(s8)
    59c4:	8fc2000c 	lw	v0,12(s8)
    59c8:	00621021 	addu	v0,v1,v0
    59cc:	afc20008 	sw	v0,8(s8)
    59d0:	8fc30008 	lw	v1,8(s8)
    59d4:	8fc20000 	lw	v0,0(s8)
    59d8:	00621024 	and	v0,v1,v0
    59dc:	00401825 	move	v1,v0
    59e0:	8fc20000 	lw	v0,0(s8)
    59e4:	00021027 	nor	v0,zero,v0
    59e8:	8fc4000c 	lw	a0,12(s8)
    59ec:	00821024 	and	v0,a0,v0
    59f0:	00621025 	or	v0,v1,v0
    59f4:	00401825 	move	v1,v0
    59f8:	8fc20010 	lw	v0,16(s8)
    59fc:	00621021 	addu	v0,v1,v0
    5a00:	8fc30004 	lw	v1,4(s8)
    5a04:	00621021 	addu	v0,v1,v0
    5a08:	00401825 	move	v1,v0
    5a0c:	3c02e9b6 	lui	v0,0xe9b6
    5a10:	3442c7aa 	ori	v0,v0,0xc7aa
    5a14:	00621021 	addu	v0,v1,v0
    5a18:	afc20004 	sw	v0,4(s8)
    5a1c:	8fc20004 	lw	v0,4(s8)
    5a20:	00021b02 	srl	v1,v0,0xc
    5a24:	00021500 	sll	v0,v0,0x14
    5a28:	00621025 	or	v0,v1,v0
    5a2c:	afc20004 	sw	v0,4(s8)
    5a30:	8fc30004 	lw	v1,4(s8)
    5a34:	8fc20008 	lw	v0,8(s8)
    5a38:	00621021 	addu	v0,v1,v0
    5a3c:	afc20004 	sw	v0,4(s8)
    5a40:	8fc30004 	lw	v1,4(s8)
    5a44:	8fc2000c 	lw	v0,12(s8)
    5a48:	00621024 	and	v0,v1,v0
    5a4c:	00401825 	move	v1,v0
    5a50:	8fc2000c 	lw	v0,12(s8)
    5a54:	00021027 	nor	v0,zero,v0
    5a58:	8fc40008 	lw	a0,8(s8)
    5a5c:	00821024 	and	v0,a0,v0
    5a60:	00621025 	or	v0,v1,v0
    5a64:	00401825 	move	v1,v0
    5a68:	8fc20024 	lw	v0,36(s8)
    5a6c:	00621021 	addu	v0,v1,v0
    5a70:	8fc30000 	lw	v1,0(s8)
    5a74:	00621021 	addu	v0,v1,v0
    5a78:	00401825 	move	v1,v0
    5a7c:	3c02d62f 	lui	v0,0xd62f
    5a80:	3442105d 	ori	v0,v0,0x105d
    5a84:	00621021 	addu	v0,v1,v0
    5a88:	afc20000 	sw	v0,0(s8)
    5a8c:	8fc20000 	lw	v0,0(s8)
    5a90:	00021940 	sll	v1,v0,0x5
    5a94:	000216c2 	srl	v0,v0,0x1b
    5a98:	00621025 	or	v0,v1,v0
    5a9c:	afc20000 	sw	v0,0(s8)
    5aa0:	8fc30000 	lw	v1,0(s8)
    5aa4:	8fc20004 	lw	v0,4(s8)
    5aa8:	00621021 	addu	v0,v1,v0
    5aac:	afc20000 	sw	v0,0(s8)
    5ab0:	8fc30000 	lw	v1,0(s8)
    5ab4:	8fc20008 	lw	v0,8(s8)
    5ab8:	00621024 	and	v0,v1,v0
    5abc:	00401825 	move	v1,v0
    5ac0:	8fc20008 	lw	v0,8(s8)
    5ac4:	00021027 	nor	v0,zero,v0
    5ac8:	8fc40004 	lw	a0,4(s8)
    5acc:	00821024 	and	v0,a0,v0
    5ad0:	00621025 	or	v0,v1,v0
    5ad4:	00401825 	move	v1,v0
    5ad8:	8fc20038 	lw	v0,56(s8)
    5adc:	00621021 	addu	v0,v1,v0
    5ae0:	8fc3000c 	lw	v1,12(s8)
    5ae4:	00621021 	addu	v0,v1,v0
    5ae8:	00401825 	move	v1,v0
    5aec:	3c020244 	lui	v0,0x244
    5af0:	34421453 	ori	v0,v0,0x1453
    5af4:	00621021 	addu	v0,v1,v0
    5af8:	afc2000c 	sw	v0,12(s8)
    5afc:	8fc2000c 	lw	v0,12(s8)
    5b00:	00021a40 	sll	v1,v0,0x9
    5b04:	000215c2 	srl	v0,v0,0x17
    5b08:	00621025 	or	v0,v1,v0
    5b0c:	afc2000c 	sw	v0,12(s8)
    5b10:	8fc3000c 	lw	v1,12(s8)
    5b14:	8fc20000 	lw	v0,0(s8)
    5b18:	00621021 	addu	v0,v1,v0
    5b1c:	afc2000c 	sw	v0,12(s8)
    5b20:	8fc3000c 	lw	v1,12(s8)
    5b24:	8fc20004 	lw	v0,4(s8)
    5b28:	00621024 	and	v0,v1,v0
    5b2c:	00401825 	move	v1,v0
    5b30:	8fc20004 	lw	v0,4(s8)
    5b34:	00021027 	nor	v0,zero,v0
    5b38:	8fc40000 	lw	a0,0(s8)
    5b3c:	00821024 	and	v0,a0,v0
    5b40:	00621025 	or	v0,v1,v0
    5b44:	00401825 	move	v1,v0
    5b48:	8fc2004c 	lw	v0,76(s8)
    5b4c:	00621021 	addu	v0,v1,v0
    5b50:	8fc30008 	lw	v1,8(s8)
    5b54:	00621021 	addu	v0,v1,v0
    5b58:	00401825 	move	v1,v0
    5b5c:	3c02d8a1 	lui	v0,0xd8a1
    5b60:	3442e681 	ori	v0,v0,0xe681
    5b64:	00621021 	addu	v0,v1,v0
    5b68:	afc20008 	sw	v0,8(s8)
    5b6c:	8fc20008 	lw	v0,8(s8)
    5b70:	00021b80 	sll	v1,v0,0xe
    5b74:	00021482 	srl	v0,v0,0x12
    5b78:	00621025 	or	v0,v1,v0
    5b7c:	afc20008 	sw	v0,8(s8)
    5b80:	8fc30008 	lw	v1,8(s8)
    5b84:	8fc2000c 	lw	v0,12(s8)
    5b88:	00621021 	addu	v0,v1,v0
    5b8c:	afc20008 	sw	v0,8(s8)
    5b90:	8fc30008 	lw	v1,8(s8)
    5b94:	8fc20000 	lw	v0,0(s8)
    5b98:	00621024 	and	v0,v1,v0
    5b9c:	00401825 	move	v1,v0
    5ba0:	8fc20000 	lw	v0,0(s8)
    5ba4:	00021027 	nor	v0,zero,v0
    5ba8:	8fc4000c 	lw	a0,12(s8)
    5bac:	00821024 	and	v0,a0,v0
    5bb0:	00621025 	or	v0,v1,v0
    5bb4:	00401825 	move	v1,v0
    5bb8:	8fc20020 	lw	v0,32(s8)
    5bbc:	00621021 	addu	v0,v1,v0
    5bc0:	8fc30004 	lw	v1,4(s8)
    5bc4:	00621021 	addu	v0,v1,v0
    5bc8:	00401825 	move	v1,v0
    5bcc:	3c02e7d3 	lui	v0,0xe7d3
    5bd0:	3442fbc8 	ori	v0,v0,0xfbc8
    5bd4:	00621021 	addu	v0,v1,v0
    5bd8:	afc20004 	sw	v0,4(s8)
    5bdc:	8fc20004 	lw	v0,4(s8)
    5be0:	00021b02 	srl	v1,v0,0xc
    5be4:	00021500 	sll	v0,v0,0x14
    5be8:	00621025 	or	v0,v1,v0
    5bec:	afc20004 	sw	v0,4(s8)
    5bf0:	8fc30004 	lw	v1,4(s8)
    5bf4:	8fc20008 	lw	v0,8(s8)
    5bf8:	00621021 	addu	v0,v1,v0
    5bfc:	afc20004 	sw	v0,4(s8)
    5c00:	8fc30004 	lw	v1,4(s8)
    5c04:	8fc2000c 	lw	v0,12(s8)
    5c08:	00621024 	and	v0,v1,v0
    5c0c:	00401825 	move	v1,v0
    5c10:	8fc2000c 	lw	v0,12(s8)
    5c14:	00021027 	nor	v0,zero,v0
    5c18:	8fc40008 	lw	a0,8(s8)
    5c1c:	00821024 	and	v0,a0,v0
    5c20:	00621025 	or	v0,v1,v0
    5c24:	00401825 	move	v1,v0
    5c28:	8fc20034 	lw	v0,52(s8)
    5c2c:	00621021 	addu	v0,v1,v0
    5c30:	8fc30000 	lw	v1,0(s8)
    5c34:	00621021 	addu	v0,v1,v0
    5c38:	00401825 	move	v1,v0
    5c3c:	3c0221e1 	lui	v0,0x21e1
    5c40:	3442cde6 	ori	v0,v0,0xcde6
    5c44:	00621021 	addu	v0,v1,v0
    5c48:	afc20000 	sw	v0,0(s8)
    5c4c:	8fc20000 	lw	v0,0(s8)
    5c50:	00021940 	sll	v1,v0,0x5
    5c54:	000216c2 	srl	v0,v0,0x1b
    5c58:	00621025 	or	v0,v1,v0
    5c5c:	afc20000 	sw	v0,0(s8)
    5c60:	8fc30000 	lw	v1,0(s8)
    5c64:	8fc20004 	lw	v0,4(s8)
    5c68:	00621021 	addu	v0,v1,v0
    5c6c:	afc20000 	sw	v0,0(s8)
    5c70:	8fc30000 	lw	v1,0(s8)
    5c74:	8fc20008 	lw	v0,8(s8)
    5c78:	00621024 	and	v0,v1,v0
    5c7c:	00401825 	move	v1,v0
    5c80:	8fc20008 	lw	v0,8(s8)
    5c84:	00021027 	nor	v0,zero,v0
    5c88:	8fc40004 	lw	a0,4(s8)
    5c8c:	00821024 	and	v0,a0,v0
    5c90:	00621025 	or	v0,v1,v0
    5c94:	00401825 	move	v1,v0
    5c98:	8fc20048 	lw	v0,72(s8)
    5c9c:	00621021 	addu	v0,v1,v0
    5ca0:	8fc3000c 	lw	v1,12(s8)
    5ca4:	00621021 	addu	v0,v1,v0
    5ca8:	00401825 	move	v1,v0
    5cac:	3c02c337 	lui	v0,0xc337
    5cb0:	344207d6 	ori	v0,v0,0x7d6
    5cb4:	00621021 	addu	v0,v1,v0
    5cb8:	afc2000c 	sw	v0,12(s8)
    5cbc:	8fc2000c 	lw	v0,12(s8)
    5cc0:	00021a40 	sll	v1,v0,0x9
    5cc4:	000215c2 	srl	v0,v0,0x17
    5cc8:	00621025 	or	v0,v1,v0
    5ccc:	afc2000c 	sw	v0,12(s8)
    5cd0:	8fc3000c 	lw	v1,12(s8)
    5cd4:	8fc20000 	lw	v0,0(s8)
    5cd8:	00621021 	addu	v0,v1,v0
    5cdc:	afc2000c 	sw	v0,12(s8)
    5ce0:	8fc3000c 	lw	v1,12(s8)
    5ce4:	8fc20004 	lw	v0,4(s8)
    5ce8:	00621024 	and	v0,v1,v0
    5cec:	00401825 	move	v1,v0
    5cf0:	8fc20004 	lw	v0,4(s8)
    5cf4:	00021027 	nor	v0,zero,v0
    5cf8:	8fc40000 	lw	a0,0(s8)
    5cfc:	00821024 	and	v0,a0,v0
    5d00:	00621025 	or	v0,v1,v0
    5d04:	00401825 	move	v1,v0
    5d08:	8fc2001c 	lw	v0,28(s8)
    5d0c:	00621021 	addu	v0,v1,v0
    5d10:	8fc30008 	lw	v1,8(s8)
    5d14:	00621021 	addu	v0,v1,v0
    5d18:	00401825 	move	v1,v0
    5d1c:	3c02f4d5 	lui	v0,0xf4d5
    5d20:	34420d87 	ori	v0,v0,0xd87
    5d24:	00621021 	addu	v0,v1,v0
    5d28:	afc20008 	sw	v0,8(s8)
    5d2c:	8fc20008 	lw	v0,8(s8)
    5d30:	00021b80 	sll	v1,v0,0xe
    5d34:	00021482 	srl	v0,v0,0x12
    5d38:	00621025 	or	v0,v1,v0
    5d3c:	afc20008 	sw	v0,8(s8)
    5d40:	8fc30008 	lw	v1,8(s8)
    5d44:	8fc2000c 	lw	v0,12(s8)
    5d48:	00621021 	addu	v0,v1,v0
    5d4c:	afc20008 	sw	v0,8(s8)
    5d50:	8fc30008 	lw	v1,8(s8)
    5d54:	8fc20000 	lw	v0,0(s8)
    5d58:	00621024 	and	v0,v1,v0
    5d5c:	00401825 	move	v1,v0
    5d60:	8fc20000 	lw	v0,0(s8)
    5d64:	00021027 	nor	v0,zero,v0
    5d68:	8fc4000c 	lw	a0,12(s8)
    5d6c:	00821024 	and	v0,a0,v0
    5d70:	00621025 	or	v0,v1,v0
    5d74:	00401825 	move	v1,v0
    5d78:	8fc20030 	lw	v0,48(s8)
    5d7c:	00621021 	addu	v0,v1,v0
    5d80:	8fc30004 	lw	v1,4(s8)
    5d84:	00621021 	addu	v0,v1,v0
    5d88:	00401825 	move	v1,v0
    5d8c:	3c02455a 	lui	v0,0x455a
    5d90:	344214ed 	ori	v0,v0,0x14ed
    5d94:	00621021 	addu	v0,v1,v0
    5d98:	afc20004 	sw	v0,4(s8)
    5d9c:	8fc20004 	lw	v0,4(s8)
    5da0:	00021b02 	srl	v1,v0,0xc
    5da4:	00021500 	sll	v0,v0,0x14
    5da8:	00621025 	or	v0,v1,v0
    5dac:	afc20004 	sw	v0,4(s8)
    5db0:	8fc30004 	lw	v1,4(s8)
    5db4:	8fc20008 	lw	v0,8(s8)
    5db8:	00621021 	addu	v0,v1,v0
    5dbc:	afc20004 	sw	v0,4(s8)
    5dc0:	8fc30004 	lw	v1,4(s8)
    5dc4:	8fc2000c 	lw	v0,12(s8)
    5dc8:	00621024 	and	v0,v1,v0
    5dcc:	00401825 	move	v1,v0
    5dd0:	8fc2000c 	lw	v0,12(s8)
    5dd4:	00021027 	nor	v0,zero,v0
    5dd8:	8fc40008 	lw	a0,8(s8)
    5ddc:	00821024 	and	v0,a0,v0
    5de0:	00621025 	or	v0,v1,v0
    5de4:	00401825 	move	v1,v0
    5de8:	8fc20044 	lw	v0,68(s8)
    5dec:	00621021 	addu	v0,v1,v0
    5df0:	8fc30000 	lw	v1,0(s8)
    5df4:	00621021 	addu	v0,v1,v0
    5df8:	00401825 	move	v1,v0
    5dfc:	3c02a9e3 	lui	v0,0xa9e3
    5e00:	3442e905 	ori	v0,v0,0xe905
    5e04:	00621021 	addu	v0,v1,v0
    5e08:	afc20000 	sw	v0,0(s8)
    5e0c:	8fc20000 	lw	v0,0(s8)
    5e10:	00021940 	sll	v1,v0,0x5
    5e14:	000216c2 	srl	v0,v0,0x1b
    5e18:	00621025 	or	v0,v1,v0
    5e1c:	afc20000 	sw	v0,0(s8)
    5e20:	8fc30000 	lw	v1,0(s8)
    5e24:	8fc20004 	lw	v0,4(s8)
    5e28:	00621021 	addu	v0,v1,v0
    5e2c:	afc20000 	sw	v0,0(s8)
    5e30:	8fc30000 	lw	v1,0(s8)
    5e34:	8fc20008 	lw	v0,8(s8)
    5e38:	00621024 	and	v0,v1,v0
    5e3c:	00401825 	move	v1,v0
    5e40:	8fc20008 	lw	v0,8(s8)
    5e44:	00021027 	nor	v0,zero,v0
    5e48:	8fc40004 	lw	a0,4(s8)
    5e4c:	00821024 	and	v0,a0,v0
    5e50:	00621025 	or	v0,v1,v0
    5e54:	00401825 	move	v1,v0
    5e58:	8fc20018 	lw	v0,24(s8)
    5e5c:	00621021 	addu	v0,v1,v0
    5e60:	8fc3000c 	lw	v1,12(s8)
    5e64:	00621021 	addu	v0,v1,v0
    5e68:	00401825 	move	v1,v0
    5e6c:	3c02fcef 	lui	v0,0xfcef
    5e70:	3442a3f8 	ori	v0,v0,0xa3f8
    5e74:	00621021 	addu	v0,v1,v0
    5e78:	afc2000c 	sw	v0,12(s8)
    5e7c:	8fc2000c 	lw	v0,12(s8)
    5e80:	00021a40 	sll	v1,v0,0x9
    5e84:	000215c2 	srl	v0,v0,0x17
    5e88:	00621025 	or	v0,v1,v0
    5e8c:	afc2000c 	sw	v0,12(s8)
    5e90:	8fc3000c 	lw	v1,12(s8)
    5e94:	8fc20000 	lw	v0,0(s8)
    5e98:	00621021 	addu	v0,v1,v0
    5e9c:	afc2000c 	sw	v0,12(s8)
    5ea0:	8fc3000c 	lw	v1,12(s8)
    5ea4:	8fc20004 	lw	v0,4(s8)
    5ea8:	00621024 	and	v0,v1,v0
    5eac:	00401825 	move	v1,v0
    5eb0:	8fc20004 	lw	v0,4(s8)
    5eb4:	00021027 	nor	v0,zero,v0
    5eb8:	8fc40000 	lw	a0,0(s8)
    5ebc:	00821024 	and	v0,a0,v0
    5ec0:	00621025 	or	v0,v1,v0
    5ec4:	00401825 	move	v1,v0
    5ec8:	8fc2002c 	lw	v0,44(s8)
    5ecc:	00621021 	addu	v0,v1,v0
    5ed0:	8fc30008 	lw	v1,8(s8)
    5ed4:	00621021 	addu	v0,v1,v0
    5ed8:	00401825 	move	v1,v0
    5edc:	3c02676f 	lui	v0,0x676f
    5ee0:	344202d9 	ori	v0,v0,0x2d9
    5ee4:	00621021 	addu	v0,v1,v0
    5ee8:	afc20008 	sw	v0,8(s8)
    5eec:	8fc20008 	lw	v0,8(s8)
    5ef0:	00021b80 	sll	v1,v0,0xe
    5ef4:	00021482 	srl	v0,v0,0x12
    5ef8:	00621025 	or	v0,v1,v0
    5efc:	afc20008 	sw	v0,8(s8)
    5f00:	8fc30008 	lw	v1,8(s8)
    5f04:	8fc2000c 	lw	v0,12(s8)
    5f08:	00621021 	addu	v0,v1,v0
    5f0c:	afc20008 	sw	v0,8(s8)
    5f10:	8fc30008 	lw	v1,8(s8)
    5f14:	8fc20000 	lw	v0,0(s8)
    5f18:	00621024 	and	v0,v1,v0
    5f1c:	00401825 	move	v1,v0
    5f20:	8fc20000 	lw	v0,0(s8)
    5f24:	00021027 	nor	v0,zero,v0
    5f28:	8fc4000c 	lw	a0,12(s8)
    5f2c:	00821024 	and	v0,a0,v0
    5f30:	00621025 	or	v0,v1,v0
    5f34:	00401825 	move	v1,v0
    5f38:	8fc20040 	lw	v0,64(s8)
    5f3c:	00621021 	addu	v0,v1,v0
    5f40:	8fc30004 	lw	v1,4(s8)
    5f44:	00621021 	addu	v0,v1,v0
    5f48:	00401825 	move	v1,v0
    5f4c:	3c028d2a 	lui	v0,0x8d2a
    5f50:	34424c8a 	ori	v0,v0,0x4c8a
    5f54:	00621021 	addu	v0,v1,v0
    5f58:	afc20004 	sw	v0,4(s8)
    5f5c:	8fc20004 	lw	v0,4(s8)
    5f60:	00021b02 	srl	v1,v0,0xc
    5f64:	00021500 	sll	v0,v0,0x14
    5f68:	00621025 	or	v0,v1,v0
    5f6c:	afc20004 	sw	v0,4(s8)
    5f70:	8fc30004 	lw	v1,4(s8)
    5f74:	8fc20008 	lw	v0,8(s8)
    5f78:	00621021 	addu	v0,v1,v0
    5f7c:	afc20004 	sw	v0,4(s8)
    5f80:	8fc30004 	lw	v1,4(s8)
    5f84:	8fc20008 	lw	v0,8(s8)
    5f88:	00621026 	xor	v0,v1,v0
    5f8c:	8fc3000c 	lw	v1,12(s8)
    5f90:	00621026 	xor	v0,v1,v0
    5f94:	00401825 	move	v1,v0
    5f98:	8fc20024 	lw	v0,36(s8)
    5f9c:	00621021 	addu	v0,v1,v0
    5fa0:	8fc30000 	lw	v1,0(s8)
    5fa4:	00621021 	addu	v0,v1,v0
    5fa8:	00401825 	move	v1,v0
    5fac:	3c02fffa 	lui	v0,0xfffa
    5fb0:	34423942 	ori	v0,v0,0x3942
    5fb4:	00621021 	addu	v0,v1,v0
    5fb8:	afc20000 	sw	v0,0(s8)
    5fbc:	8fc20000 	lw	v0,0(s8)
    5fc0:	00021900 	sll	v1,v0,0x4
    5fc4:	00021702 	srl	v0,v0,0x1c
    5fc8:	00621025 	or	v0,v1,v0
    5fcc:	afc20000 	sw	v0,0(s8)
    5fd0:	8fc30000 	lw	v1,0(s8)
    5fd4:	8fc20004 	lw	v0,4(s8)
    5fd8:	00621021 	addu	v0,v1,v0
    5fdc:	afc20000 	sw	v0,0(s8)
    5fe0:	8fc30000 	lw	v1,0(s8)
    5fe4:	8fc20004 	lw	v0,4(s8)
    5fe8:	00621026 	xor	v0,v1,v0
    5fec:	8fc30008 	lw	v1,8(s8)
    5ff0:	00621026 	xor	v0,v1,v0
    5ff4:	00401825 	move	v1,v0
    5ff8:	8fc20030 	lw	v0,48(s8)
    5ffc:	00621021 	addu	v0,v1,v0
    6000:	8fc3000c 	lw	v1,12(s8)
    6004:	00621021 	addu	v0,v1,v0
    6008:	00401825 	move	v1,v0
    600c:	3c028771 	lui	v0,0x8771
    6010:	3442f681 	ori	v0,v0,0xf681
    6014:	00621021 	addu	v0,v1,v0
    6018:	afc2000c 	sw	v0,12(s8)
    601c:	8fc2000c 	lw	v0,12(s8)
    6020:	00021ac0 	sll	v1,v0,0xb
    6024:	00021542 	srl	v0,v0,0x15
    6028:	00621025 	or	v0,v1,v0
    602c:	afc2000c 	sw	v0,12(s8)
    6030:	8fc3000c 	lw	v1,12(s8)
    6034:	8fc20000 	lw	v0,0(s8)
    6038:	00621021 	addu	v0,v1,v0
    603c:	afc2000c 	sw	v0,12(s8)
    6040:	8fc3000c 	lw	v1,12(s8)
    6044:	8fc20000 	lw	v0,0(s8)
    6048:	00621026 	xor	v0,v1,v0
    604c:	8fc30004 	lw	v1,4(s8)
    6050:	00621026 	xor	v0,v1,v0
    6054:	00401825 	move	v1,v0
    6058:	8fc2003c 	lw	v0,60(s8)
    605c:	00621021 	addu	v0,v1,v0
    6060:	8fc30008 	lw	v1,8(s8)
    6064:	00621021 	addu	v0,v1,v0
    6068:	00401825 	move	v1,v0
    606c:	3c026d9d 	lui	v0,0x6d9d
    6070:	34426122 	ori	v0,v0,0x6122
    6074:	00621021 	addu	v0,v1,v0
    6078:	afc20008 	sw	v0,8(s8)
    607c:	8fc20008 	lw	v0,8(s8)
    6080:	00021c00 	sll	v1,v0,0x10
    6084:	00021402 	srl	v0,v0,0x10
    6088:	00621025 	or	v0,v1,v0
    608c:	afc20008 	sw	v0,8(s8)
    6090:	8fc30008 	lw	v1,8(s8)
    6094:	8fc2000c 	lw	v0,12(s8)
    6098:	00621021 	addu	v0,v1,v0
    609c:	afc20008 	sw	v0,8(s8)
    60a0:	8fc30008 	lw	v1,8(s8)
    60a4:	8fc2000c 	lw	v0,12(s8)
    60a8:	00621026 	xor	v0,v1,v0
    60ac:	8fc30000 	lw	v1,0(s8)
    60b0:	00621026 	xor	v0,v1,v0
    60b4:	00401825 	move	v1,v0
    60b8:	8fc20048 	lw	v0,72(s8)
    60bc:	00621021 	addu	v0,v1,v0
    60c0:	8fc30004 	lw	v1,4(s8)
    60c4:	00621021 	addu	v0,v1,v0
    60c8:	00401825 	move	v1,v0
    60cc:	3c02fde5 	lui	v0,0xfde5
    60d0:	3442380c 	ori	v0,v0,0x380c
    60d4:	00621021 	addu	v0,v1,v0
    60d8:	afc20004 	sw	v0,4(s8)
    60dc:	8fc20004 	lw	v0,4(s8)
    60e0:	00021a42 	srl	v1,v0,0x9
    60e4:	000215c0 	sll	v0,v0,0x17
    60e8:	00621025 	or	v0,v1,v0
    60ec:	afc20004 	sw	v0,4(s8)
    60f0:	8fc30004 	lw	v1,4(s8)
    60f4:	8fc20008 	lw	v0,8(s8)
    60f8:	00621021 	addu	v0,v1,v0
    60fc:	afc20004 	sw	v0,4(s8)
    6100:	8fc30004 	lw	v1,4(s8)
    6104:	8fc20008 	lw	v0,8(s8)
    6108:	00621026 	xor	v0,v1,v0
    610c:	8fc3000c 	lw	v1,12(s8)
    6110:	00621026 	xor	v0,v1,v0
    6114:	00401825 	move	v1,v0
    6118:	8fc20014 	lw	v0,20(s8)
    611c:	00621021 	addu	v0,v1,v0
    6120:	8fc30000 	lw	v1,0(s8)
    6124:	00621021 	addu	v0,v1,v0
    6128:	00401825 	move	v1,v0
    612c:	3c02a4be 	lui	v0,0xa4be
    6130:	3442ea44 	ori	v0,v0,0xea44
    6134:	00621021 	addu	v0,v1,v0
    6138:	afc20000 	sw	v0,0(s8)
    613c:	8fc20000 	lw	v0,0(s8)
    6140:	00021900 	sll	v1,v0,0x4
    6144:	00021702 	srl	v0,v0,0x1c
    6148:	00621025 	or	v0,v1,v0
    614c:	afc20000 	sw	v0,0(s8)
    6150:	8fc30000 	lw	v1,0(s8)
    6154:	8fc20004 	lw	v0,4(s8)
    6158:	00621021 	addu	v0,v1,v0
    615c:	afc20000 	sw	v0,0(s8)
    6160:	8fc30000 	lw	v1,0(s8)
    6164:	8fc20004 	lw	v0,4(s8)
    6168:	00621026 	xor	v0,v1,v0
    616c:	8fc30008 	lw	v1,8(s8)
    6170:	00621026 	xor	v0,v1,v0
    6174:	00401825 	move	v1,v0
    6178:	8fc20020 	lw	v0,32(s8)
    617c:	00621021 	addu	v0,v1,v0
    6180:	8fc3000c 	lw	v1,12(s8)
    6184:	00621021 	addu	v0,v1,v0
    6188:	00401825 	move	v1,v0
    618c:	3c024bde 	lui	v0,0x4bde
    6190:	3442cfa9 	ori	v0,v0,0xcfa9
    6194:	00621021 	addu	v0,v1,v0
    6198:	afc2000c 	sw	v0,12(s8)
    619c:	8fc2000c 	lw	v0,12(s8)
    61a0:	00021ac0 	sll	v1,v0,0xb
    61a4:	00021542 	srl	v0,v0,0x15
    61a8:	00621025 	or	v0,v1,v0
    61ac:	afc2000c 	sw	v0,12(s8)
    61b0:	8fc3000c 	lw	v1,12(s8)
    61b4:	8fc20000 	lw	v0,0(s8)
    61b8:	00621021 	addu	v0,v1,v0
    61bc:	afc2000c 	sw	v0,12(s8)
    61c0:	8fc3000c 	lw	v1,12(s8)
    61c4:	8fc20000 	lw	v0,0(s8)
    61c8:	00621026 	xor	v0,v1,v0
    61cc:	8fc30004 	lw	v1,4(s8)
    61d0:	00621026 	xor	v0,v1,v0
    61d4:	00401825 	move	v1,v0
    61d8:	8fc2002c 	lw	v0,44(s8)
    61dc:	00621021 	addu	v0,v1,v0
    61e0:	8fc30008 	lw	v1,8(s8)
    61e4:	00621021 	addu	v0,v1,v0
    61e8:	00401825 	move	v1,v0
    61ec:	3c02f6bb 	lui	v0,0xf6bb
    61f0:	34424b60 	ori	v0,v0,0x4b60
    61f4:	00621021 	addu	v0,v1,v0
    61f8:	afc20008 	sw	v0,8(s8)
    61fc:	8fc20008 	lw	v0,8(s8)
    6200:	00021c00 	sll	v1,v0,0x10
    6204:	00021402 	srl	v0,v0,0x10
    6208:	00621025 	or	v0,v1,v0
    620c:	afc20008 	sw	v0,8(s8)
    6210:	8fc30008 	lw	v1,8(s8)
    6214:	8fc2000c 	lw	v0,12(s8)
    6218:	00621021 	addu	v0,v1,v0
    621c:	afc20008 	sw	v0,8(s8)
    6220:	8fc30008 	lw	v1,8(s8)
    6224:	8fc2000c 	lw	v0,12(s8)
    6228:	00621026 	xor	v0,v1,v0
    622c:	8fc30000 	lw	v1,0(s8)
    6230:	00621026 	xor	v0,v1,v0
    6234:	00401825 	move	v1,v0
    6238:	8fc20038 	lw	v0,56(s8)
    623c:	00621021 	addu	v0,v1,v0
    6240:	8fc30004 	lw	v1,4(s8)
    6244:	00621021 	addu	v0,v1,v0
    6248:	00401825 	move	v1,v0
    624c:	3c02bebf 	lui	v0,0xbebf
    6250:	3442bc70 	ori	v0,v0,0xbc70
    6254:	00621021 	addu	v0,v1,v0
    6258:	afc20004 	sw	v0,4(s8)
    625c:	8fc20004 	lw	v0,4(s8)
    6260:	00021a42 	srl	v1,v0,0x9
    6264:	000215c0 	sll	v0,v0,0x17
    6268:	00621025 	or	v0,v1,v0
    626c:	afc20004 	sw	v0,4(s8)
    6270:	8fc30004 	lw	v1,4(s8)
    6274:	8fc20008 	lw	v0,8(s8)
    6278:	00621021 	addu	v0,v1,v0
    627c:	afc20004 	sw	v0,4(s8)
    6280:	8fc30004 	lw	v1,4(s8)
    6284:	8fc20008 	lw	v0,8(s8)
    6288:	00621026 	xor	v0,v1,v0
    628c:	8fc3000c 	lw	v1,12(s8)
    6290:	00621026 	xor	v0,v1,v0
    6294:	00401825 	move	v1,v0
    6298:	8fc20044 	lw	v0,68(s8)
    629c:	00621021 	addu	v0,v1,v0
    62a0:	8fc30000 	lw	v1,0(s8)
    62a4:	00621021 	addu	v0,v1,v0
    62a8:	00401825 	move	v1,v0
    62ac:	3c02289b 	lui	v0,0x289b
    62b0:	34427ec6 	ori	v0,v0,0x7ec6
    62b4:	00621021 	addu	v0,v1,v0
    62b8:	afc20000 	sw	v0,0(s8)
    62bc:	8fc20000 	lw	v0,0(s8)
    62c0:	00021900 	sll	v1,v0,0x4
    62c4:	00021702 	srl	v0,v0,0x1c
    62c8:	00621025 	or	v0,v1,v0
    62cc:	afc20000 	sw	v0,0(s8)
    62d0:	8fc30000 	lw	v1,0(s8)
    62d4:	8fc20004 	lw	v0,4(s8)
    62d8:	00621021 	addu	v0,v1,v0
    62dc:	afc20000 	sw	v0,0(s8)
    62e0:	8fc30000 	lw	v1,0(s8)
    62e4:	8fc20004 	lw	v0,4(s8)
    62e8:	00621026 	xor	v0,v1,v0
    62ec:	8fc30008 	lw	v1,8(s8)
    62f0:	00621026 	xor	v0,v1,v0
    62f4:	00401825 	move	v1,v0
    62f8:	8fc20010 	lw	v0,16(s8)
    62fc:	00621021 	addu	v0,v1,v0
    6300:	8fc3000c 	lw	v1,12(s8)
    6304:	00621021 	addu	v0,v1,v0
    6308:	00401825 	move	v1,v0
    630c:	3c02eaa1 	lui	v0,0xeaa1
    6310:	344227fa 	ori	v0,v0,0x27fa
    6314:	00621021 	addu	v0,v1,v0
    6318:	afc2000c 	sw	v0,12(s8)
    631c:	8fc2000c 	lw	v0,12(s8)
    6320:	00021ac0 	sll	v1,v0,0xb
    6324:	00021542 	srl	v0,v0,0x15
    6328:	00621025 	or	v0,v1,v0
    632c:	afc2000c 	sw	v0,12(s8)
    6330:	8fc3000c 	lw	v1,12(s8)
    6334:	8fc20000 	lw	v0,0(s8)
    6338:	00621021 	addu	v0,v1,v0
    633c:	afc2000c 	sw	v0,12(s8)
    6340:	8fc3000c 	lw	v1,12(s8)
    6344:	8fc20000 	lw	v0,0(s8)
    6348:	00621026 	xor	v0,v1,v0
    634c:	8fc30004 	lw	v1,4(s8)
    6350:	00621026 	xor	v0,v1,v0
    6354:	00401825 	move	v1,v0
    6358:	8fc2001c 	lw	v0,28(s8)
    635c:	00621021 	addu	v0,v1,v0
    6360:	8fc30008 	lw	v1,8(s8)
    6364:	00621021 	addu	v0,v1,v0
    6368:	00401825 	move	v1,v0
    636c:	3c02d4ef 	lui	v0,0xd4ef
    6370:	34423085 	ori	v0,v0,0x3085
    6374:	00621021 	addu	v0,v1,v0
    6378:	afc20008 	sw	v0,8(s8)
    637c:	8fc20008 	lw	v0,8(s8)
    6380:	00021c00 	sll	v1,v0,0x10
    6384:	00021402 	srl	v0,v0,0x10
    6388:	00621025 	or	v0,v1,v0
    638c:	afc20008 	sw	v0,8(s8)
    6390:	8fc30008 	lw	v1,8(s8)
    6394:	8fc2000c 	lw	v0,12(s8)
    6398:	00621021 	addu	v0,v1,v0
    639c:	afc20008 	sw	v0,8(s8)
    63a0:	8fc30008 	lw	v1,8(s8)
    63a4:	8fc2000c 	lw	v0,12(s8)
    63a8:	00621026 	xor	v0,v1,v0
    63ac:	8fc30000 	lw	v1,0(s8)
    63b0:	00621026 	xor	v0,v1,v0
    63b4:	00401825 	move	v1,v0
    63b8:	8fc20028 	lw	v0,40(s8)
    63bc:	00621021 	addu	v0,v1,v0
    63c0:	8fc30004 	lw	v1,4(s8)
    63c4:	00621021 	addu	v0,v1,v0
    63c8:	00401825 	move	v1,v0
    63cc:	3c020488 	lui	v0,0x488
    63d0:	34421d05 	ori	v0,v0,0x1d05
    63d4:	00621021 	addu	v0,v1,v0
    63d8:	afc20004 	sw	v0,4(s8)
    63dc:	8fc20004 	lw	v0,4(s8)
    63e0:	00021a42 	srl	v1,v0,0x9
    63e4:	000215c0 	sll	v0,v0,0x17
    63e8:	00621025 	or	v0,v1,v0
    63ec:	afc20004 	sw	v0,4(s8)
    63f0:	8fc30004 	lw	v1,4(s8)
    63f4:	8fc20008 	lw	v0,8(s8)
    63f8:	00621021 	addu	v0,v1,v0
    63fc:	afc20004 	sw	v0,4(s8)
    6400:	8fc30004 	lw	v1,4(s8)
    6404:	8fc20008 	lw	v0,8(s8)
    6408:	00621026 	xor	v0,v1,v0
    640c:	8fc3000c 	lw	v1,12(s8)
    6410:	00621026 	xor	v0,v1,v0
    6414:	00401825 	move	v1,v0
    6418:	8fc20034 	lw	v0,52(s8)
    641c:	00621021 	addu	v0,v1,v0
    6420:	8fc30000 	lw	v1,0(s8)
    6424:	00621021 	addu	v0,v1,v0
    6428:	00401825 	move	v1,v0
    642c:	3c02d9d4 	lui	v0,0xd9d4
    6430:	3442d039 	ori	v0,v0,0xd039
    6434:	00621021 	addu	v0,v1,v0
    6438:	afc20000 	sw	v0,0(s8)
    643c:	8fc20000 	lw	v0,0(s8)
    6440:	00021900 	sll	v1,v0,0x4
    6444:	00021702 	srl	v0,v0,0x1c
    6448:	00621025 	or	v0,v1,v0
    644c:	afc20000 	sw	v0,0(s8)
    6450:	8fc30000 	lw	v1,0(s8)
    6454:	8fc20004 	lw	v0,4(s8)
    6458:	00621021 	addu	v0,v1,v0
    645c:	afc20000 	sw	v0,0(s8)
    6460:	8fc30000 	lw	v1,0(s8)
    6464:	8fc20004 	lw	v0,4(s8)
    6468:	00621026 	xor	v0,v1,v0
    646c:	8fc30008 	lw	v1,8(s8)
    6470:	00621026 	xor	v0,v1,v0
    6474:	00401825 	move	v1,v0
    6478:	8fc20040 	lw	v0,64(s8)
    647c:	00621021 	addu	v0,v1,v0
    6480:	8fc3000c 	lw	v1,12(s8)
    6484:	00621021 	addu	v0,v1,v0
    6488:	00401825 	move	v1,v0
    648c:	3c02e6db 	lui	v0,0xe6db
    6490:	344299e5 	ori	v0,v0,0x99e5
    6494:	00621021 	addu	v0,v1,v0
    6498:	afc2000c 	sw	v0,12(s8)
    649c:	8fc2000c 	lw	v0,12(s8)
    64a0:	00021ac0 	sll	v1,v0,0xb
    64a4:	00021542 	srl	v0,v0,0x15
    64a8:	00621025 	or	v0,v1,v0
    64ac:	afc2000c 	sw	v0,12(s8)
    64b0:	8fc3000c 	lw	v1,12(s8)
    64b4:	8fc20000 	lw	v0,0(s8)
    64b8:	00621021 	addu	v0,v1,v0
    64bc:	afc2000c 	sw	v0,12(s8)
    64c0:	8fc3000c 	lw	v1,12(s8)
    64c4:	8fc20000 	lw	v0,0(s8)
    64c8:	00621026 	xor	v0,v1,v0
    64cc:	8fc30004 	lw	v1,4(s8)
    64d0:	00621026 	xor	v0,v1,v0
    64d4:	00401825 	move	v1,v0
    64d8:	8fc2004c 	lw	v0,76(s8)
    64dc:	00621021 	addu	v0,v1,v0
    64e0:	8fc30008 	lw	v1,8(s8)
    64e4:	00621021 	addu	v0,v1,v0
    64e8:	00401825 	move	v1,v0
    64ec:	3c021fa2 	lui	v0,0x1fa2
    64f0:	34427cf8 	ori	v0,v0,0x7cf8
    64f4:	00621021 	addu	v0,v1,v0
    64f8:	afc20008 	sw	v0,8(s8)
    64fc:	8fc20008 	lw	v0,8(s8)
    6500:	00021c00 	sll	v1,v0,0x10
    6504:	00021402 	srl	v0,v0,0x10
    6508:	00621025 	or	v0,v1,v0
    650c:	afc20008 	sw	v0,8(s8)
    6510:	8fc30008 	lw	v1,8(s8)
    6514:	8fc2000c 	lw	v0,12(s8)
    6518:	00621021 	addu	v0,v1,v0
    651c:	afc20008 	sw	v0,8(s8)
    6520:	8fc30008 	lw	v1,8(s8)
    6524:	8fc2000c 	lw	v0,12(s8)
    6528:	00621026 	xor	v0,v1,v0
    652c:	8fc30000 	lw	v1,0(s8)
    6530:	00621026 	xor	v0,v1,v0
    6534:	00401825 	move	v1,v0
    6538:	8fc20018 	lw	v0,24(s8)
    653c:	00621021 	addu	v0,v1,v0
    6540:	8fc30004 	lw	v1,4(s8)
    6544:	00621021 	addu	v0,v1,v0
    6548:	00401825 	move	v1,v0
    654c:	3c02c4ac 	lui	v0,0xc4ac
    6550:	34425665 	ori	v0,v0,0x5665
    6554:	00621021 	addu	v0,v1,v0
    6558:	afc20004 	sw	v0,4(s8)
    655c:	8fc20004 	lw	v0,4(s8)
    6560:	00021a42 	srl	v1,v0,0x9
    6564:	000215c0 	sll	v0,v0,0x17
    6568:	00621025 	or	v0,v1,v0
    656c:	afc20004 	sw	v0,4(s8)
    6570:	8fc30004 	lw	v1,4(s8)
    6574:	8fc20008 	lw	v0,8(s8)
    6578:	00621021 	addu	v0,v1,v0
    657c:	afc20004 	sw	v0,4(s8)
    6580:	8fc2000c 	lw	v0,12(s8)
    6584:	00021027 	nor	v0,zero,v0
    6588:	8fc30004 	lw	v1,4(s8)
    658c:	00621025 	or	v0,v1,v0
    6590:	8fc30008 	lw	v1,8(s8)
    6594:	00621026 	xor	v0,v1,v0
    6598:	00401825 	move	v1,v0
    659c:	8fc20010 	lw	v0,16(s8)
    65a0:	00621021 	addu	v0,v1,v0
    65a4:	8fc30000 	lw	v1,0(s8)
    65a8:	00621021 	addu	v0,v1,v0
    65ac:	00401825 	move	v1,v0
    65b0:	3c02f429 	lui	v0,0xf429
    65b4:	34422244 	ori	v0,v0,0x2244
    65b8:	00621021 	addu	v0,v1,v0
    65bc:	afc20000 	sw	v0,0(s8)
    65c0:	8fc20000 	lw	v0,0(s8)
    65c4:	00021980 	sll	v1,v0,0x6
    65c8:	00021682 	srl	v0,v0,0x1a
    65cc:	00621025 	or	v0,v1,v0
    65d0:	afc20000 	sw	v0,0(s8)
    65d4:	8fc30000 	lw	v1,0(s8)
    65d8:	8fc20004 	lw	v0,4(s8)
    65dc:	00621021 	addu	v0,v1,v0
    65e0:	afc20000 	sw	v0,0(s8)
    65e4:	8fc20008 	lw	v0,8(s8)
    65e8:	00021027 	nor	v0,zero,v0
    65ec:	8fc30000 	lw	v1,0(s8)
    65f0:	00621025 	or	v0,v1,v0
    65f4:	8fc30004 	lw	v1,4(s8)
    65f8:	00621026 	xor	v0,v1,v0
    65fc:	00401825 	move	v1,v0
    6600:	8fc2002c 	lw	v0,44(s8)
    6604:	00621021 	addu	v0,v1,v0
    6608:	8fc3000c 	lw	v1,12(s8)
    660c:	00621021 	addu	v0,v1,v0
    6610:	00401825 	move	v1,v0
    6614:	3c02432a 	lui	v0,0x432a
    6618:	3442ff97 	ori	v0,v0,0xff97
    661c:	00621021 	addu	v0,v1,v0
    6620:	afc2000c 	sw	v0,12(s8)
    6624:	8fc2000c 	lw	v0,12(s8)
    6628:	00021a80 	sll	v1,v0,0xa
    662c:	00021582 	srl	v0,v0,0x16
    6630:	00621025 	or	v0,v1,v0
    6634:	afc2000c 	sw	v0,12(s8)
    6638:	8fc3000c 	lw	v1,12(s8)
    663c:	8fc20000 	lw	v0,0(s8)
    6640:	00621021 	addu	v0,v1,v0
    6644:	afc2000c 	sw	v0,12(s8)
    6648:	8fc20004 	lw	v0,4(s8)
    664c:	00021027 	nor	v0,zero,v0
    6650:	8fc3000c 	lw	v1,12(s8)
    6654:	00621025 	or	v0,v1,v0
    6658:	8fc30000 	lw	v1,0(s8)
    665c:	00621026 	xor	v0,v1,v0
    6660:	00401825 	move	v1,v0
    6664:	8fc20048 	lw	v0,72(s8)
    6668:	00621021 	addu	v0,v1,v0
    666c:	8fc30008 	lw	v1,8(s8)
    6670:	00621021 	addu	v0,v1,v0
    6674:	00401825 	move	v1,v0
    6678:	3c02ab94 	lui	v0,0xab94
    667c:	344223a7 	ori	v0,v0,0x23a7
    6680:	00621021 	addu	v0,v1,v0
    6684:	afc20008 	sw	v0,8(s8)
    6688:	8fc20008 	lw	v0,8(s8)
    668c:	00021bc0 	sll	v1,v0,0xf
    6690:	00021442 	srl	v0,v0,0x11
    6694:	00621025 	or	v0,v1,v0
    6698:	afc20008 	sw	v0,8(s8)
    669c:	8fc30008 	lw	v1,8(s8)
    66a0:	8fc2000c 	lw	v0,12(s8)
    66a4:	00621021 	addu	v0,v1,v0
    66a8:	afc20008 	sw	v0,8(s8)
    66ac:	8fc20000 	lw	v0,0(s8)
    66b0:	00021027 	nor	v0,zero,v0
    66b4:	8fc30008 	lw	v1,8(s8)
    66b8:	00621025 	or	v0,v1,v0
    66bc:	8fc3000c 	lw	v1,12(s8)
    66c0:	00621026 	xor	v0,v1,v0
    66c4:	00401825 	move	v1,v0
    66c8:	8fc20024 	lw	v0,36(s8)
    66cc:	00621021 	addu	v0,v1,v0
    66d0:	8fc30004 	lw	v1,4(s8)
    66d4:	00621021 	addu	v0,v1,v0
    66d8:	00401825 	move	v1,v0
    66dc:	3c02fc93 	lui	v0,0xfc93
    66e0:	3442a039 	ori	v0,v0,0xa039
    66e4:	00621021 	addu	v0,v1,v0
    66e8:	afc20004 	sw	v0,4(s8)
    66ec:	8fc20004 	lw	v0,4(s8)
    66f0:	00021ac2 	srl	v1,v0,0xb
    66f4:	00021540 	sll	v0,v0,0x15
    66f8:	00621025 	or	v0,v1,v0
    66fc:	afc20004 	sw	v0,4(s8)
    6700:	8fc30004 	lw	v1,4(s8)
    6704:	8fc20008 	lw	v0,8(s8)
    6708:	00621021 	addu	v0,v1,v0
    670c:	afc20004 	sw	v0,4(s8)
    6710:	8fc2000c 	lw	v0,12(s8)
    6714:	00021027 	nor	v0,zero,v0
    6718:	8fc30004 	lw	v1,4(s8)
    671c:	00621025 	or	v0,v1,v0
    6720:	8fc30008 	lw	v1,8(s8)
    6724:	00621026 	xor	v0,v1,v0
    6728:	00401825 	move	v1,v0
    672c:	8fc20040 	lw	v0,64(s8)
    6730:	00621021 	addu	v0,v1,v0
    6734:	8fc30000 	lw	v1,0(s8)
    6738:	00621021 	addu	v0,v1,v0
    673c:	00401825 	move	v1,v0
    6740:	3c02655b 	lui	v0,0x655b
    6744:	344259c3 	ori	v0,v0,0x59c3
    6748:	00621021 	addu	v0,v1,v0
    674c:	afc20000 	sw	v0,0(s8)
    6750:	8fc20000 	lw	v0,0(s8)
    6754:	00021980 	sll	v1,v0,0x6
    6758:	00021682 	srl	v0,v0,0x1a
    675c:	00621025 	or	v0,v1,v0
    6760:	afc20000 	sw	v0,0(s8)
    6764:	8fc30000 	lw	v1,0(s8)
    6768:	8fc20004 	lw	v0,4(s8)
    676c:	00621021 	addu	v0,v1,v0
    6770:	afc20000 	sw	v0,0(s8)
    6774:	8fc20008 	lw	v0,8(s8)
    6778:	00021027 	nor	v0,zero,v0
    677c:	8fc30000 	lw	v1,0(s8)
    6780:	00621025 	or	v0,v1,v0
    6784:	8fc30004 	lw	v1,4(s8)
    6788:	00621026 	xor	v0,v1,v0
    678c:	00401825 	move	v1,v0
    6790:	8fc2001c 	lw	v0,28(s8)
    6794:	00621021 	addu	v0,v1,v0
    6798:	8fc3000c 	lw	v1,12(s8)
    679c:	00621021 	addu	v0,v1,v0
    67a0:	00401825 	move	v1,v0
    67a4:	3c028f0c 	lui	v0,0x8f0c
    67a8:	3442cc92 	ori	v0,v0,0xcc92
    67ac:	00621021 	addu	v0,v1,v0
    67b0:	afc2000c 	sw	v0,12(s8)
    67b4:	8fc2000c 	lw	v0,12(s8)
    67b8:	00021a80 	sll	v1,v0,0xa
    67bc:	00021582 	srl	v0,v0,0x16
    67c0:	00621025 	or	v0,v1,v0
    67c4:	afc2000c 	sw	v0,12(s8)
    67c8:	8fc3000c 	lw	v1,12(s8)
    67cc:	8fc20000 	lw	v0,0(s8)
    67d0:	00621021 	addu	v0,v1,v0
    67d4:	afc2000c 	sw	v0,12(s8)
    67d8:	8fc20004 	lw	v0,4(s8)
    67dc:	00021027 	nor	v0,zero,v0
    67e0:	8fc3000c 	lw	v1,12(s8)
    67e4:	00621025 	or	v0,v1,v0
    67e8:	8fc30000 	lw	v1,0(s8)
    67ec:	00621026 	xor	v0,v1,v0
    67f0:	00401825 	move	v1,v0
    67f4:	8fc20038 	lw	v0,56(s8)
    67f8:	00621021 	addu	v0,v1,v0
    67fc:	8fc30008 	lw	v1,8(s8)
    6800:	00621021 	addu	v0,v1,v0
    6804:	00401825 	move	v1,v0
    6808:	3c02ffef 	lui	v0,0xffef
    680c:	3442f47d 	ori	v0,v0,0xf47d
    6810:	00621021 	addu	v0,v1,v0
    6814:	afc20008 	sw	v0,8(s8)
    6818:	8fc20008 	lw	v0,8(s8)
    681c:	00021bc0 	sll	v1,v0,0xf
    6820:	00021442 	srl	v0,v0,0x11
    6824:	00621025 	or	v0,v1,v0
    6828:	afc20008 	sw	v0,8(s8)
    682c:	8fc30008 	lw	v1,8(s8)
    6830:	8fc2000c 	lw	v0,12(s8)
    6834:	00621021 	addu	v0,v1,v0
    6838:	afc20008 	sw	v0,8(s8)
    683c:	8fc20000 	lw	v0,0(s8)
    6840:	00021027 	nor	v0,zero,v0
    6844:	8fc30008 	lw	v1,8(s8)
    6848:	00621025 	or	v0,v1,v0
    684c:	8fc3000c 	lw	v1,12(s8)
    6850:	00621026 	xor	v0,v1,v0
    6854:	00401825 	move	v1,v0
    6858:	8fc20014 	lw	v0,20(s8)
    685c:	00621021 	addu	v0,v1,v0
    6860:	8fc30004 	lw	v1,4(s8)
    6864:	00621021 	addu	v0,v1,v0
    6868:	00401825 	move	v1,v0
    686c:	3c028584 	lui	v0,0x8584
    6870:	34425dd1 	ori	v0,v0,0x5dd1
    6874:	00621021 	addu	v0,v1,v0
    6878:	afc20004 	sw	v0,4(s8)
    687c:	8fc20004 	lw	v0,4(s8)
    6880:	00021ac2 	srl	v1,v0,0xb
    6884:	00021540 	sll	v0,v0,0x15
    6888:	00621025 	or	v0,v1,v0
    688c:	afc20004 	sw	v0,4(s8)
    6890:	8fc30004 	lw	v1,4(s8)
    6894:	8fc20008 	lw	v0,8(s8)
    6898:	00621021 	addu	v0,v1,v0
    689c:	afc20004 	sw	v0,4(s8)
    68a0:	8fc2000c 	lw	v0,12(s8)
    68a4:	00021027 	nor	v0,zero,v0
    68a8:	8fc30004 	lw	v1,4(s8)
    68ac:	00621025 	or	v0,v1,v0
    68b0:	8fc30008 	lw	v1,8(s8)
    68b4:	00621026 	xor	v0,v1,v0
    68b8:	00401825 	move	v1,v0
    68bc:	8fc20030 	lw	v0,48(s8)
    68c0:	00621021 	addu	v0,v1,v0
    68c4:	8fc30000 	lw	v1,0(s8)
    68c8:	00621021 	addu	v0,v1,v0
    68cc:	00401825 	move	v1,v0
    68d0:	3c026fa8 	lui	v0,0x6fa8
    68d4:	34427e4f 	ori	v0,v0,0x7e4f
    68d8:	00621021 	addu	v0,v1,v0
    68dc:	afc20000 	sw	v0,0(s8)
    68e0:	8fc20000 	lw	v0,0(s8)
    68e4:	00021980 	sll	v1,v0,0x6
    68e8:	00021682 	srl	v0,v0,0x1a
    68ec:	00621025 	or	v0,v1,v0
    68f0:	afc20000 	sw	v0,0(s8)
    68f4:	8fc30000 	lw	v1,0(s8)
    68f8:	8fc20004 	lw	v0,4(s8)
    68fc:	00621021 	addu	v0,v1,v0
    6900:	afc20000 	sw	v0,0(s8)
    6904:	8fc20008 	lw	v0,8(s8)
    6908:	00021027 	nor	v0,zero,v0
    690c:	8fc30000 	lw	v1,0(s8)
    6910:	00621025 	or	v0,v1,v0
    6914:	8fc30004 	lw	v1,4(s8)
    6918:	00621026 	xor	v0,v1,v0
    691c:	00401825 	move	v1,v0
    6920:	8fc2004c 	lw	v0,76(s8)
    6924:	00621021 	addu	v0,v1,v0
    6928:	8fc3000c 	lw	v1,12(s8)
    692c:	00621021 	addu	v0,v1,v0
    6930:	00401825 	move	v1,v0
    6934:	3c02fe2c 	lui	v0,0xfe2c
    6938:	3442e6e0 	ori	v0,v0,0xe6e0
    693c:	00621021 	addu	v0,v1,v0
    6940:	afc2000c 	sw	v0,12(s8)
    6944:	8fc2000c 	lw	v0,12(s8)
    6948:	00021a80 	sll	v1,v0,0xa
    694c:	00021582 	srl	v0,v0,0x16
    6950:	00621025 	or	v0,v1,v0
    6954:	afc2000c 	sw	v0,12(s8)
    6958:	8fc3000c 	lw	v1,12(s8)
    695c:	8fc20000 	lw	v0,0(s8)
    6960:	00621021 	addu	v0,v1,v0
    6964:	afc2000c 	sw	v0,12(s8)
    6968:	8fc20004 	lw	v0,4(s8)
    696c:	00021027 	nor	v0,zero,v0
    6970:	8fc3000c 	lw	v1,12(s8)
    6974:	00621025 	or	v0,v1,v0
    6978:	8fc30000 	lw	v1,0(s8)
    697c:	00621026 	xor	v0,v1,v0
    6980:	00401825 	move	v1,v0
    6984:	8fc20028 	lw	v0,40(s8)
    6988:	00621021 	addu	v0,v1,v0
    698c:	8fc30008 	lw	v1,8(s8)
    6990:	00621021 	addu	v0,v1,v0
    6994:	00401825 	move	v1,v0
    6998:	3c02a301 	lui	v0,0xa301
    699c:	34424314 	ori	v0,v0,0x4314
    69a0:	00621021 	addu	v0,v1,v0
    69a4:	afc20008 	sw	v0,8(s8)
    69a8:	8fc20008 	lw	v0,8(s8)
    69ac:	00021bc0 	sll	v1,v0,0xf
    69b0:	00021442 	srl	v0,v0,0x11
    69b4:	00621025 	or	v0,v1,v0
    69b8:	afc20008 	sw	v0,8(s8)
    69bc:	8fc30008 	lw	v1,8(s8)
    69c0:	8fc2000c 	lw	v0,12(s8)
    69c4:	00621021 	addu	v0,v1,v0
    69c8:	afc20008 	sw	v0,8(s8)
    69cc:	8fc20000 	lw	v0,0(s8)
    69d0:	00021027 	nor	v0,zero,v0
    69d4:	8fc30008 	lw	v1,8(s8)
    69d8:	00621025 	or	v0,v1,v0
    69dc:	8fc3000c 	lw	v1,12(s8)
    69e0:	00621026 	xor	v0,v1,v0
    69e4:	00401825 	move	v1,v0
    69e8:	8fc20044 	lw	v0,68(s8)
    69ec:	00621021 	addu	v0,v1,v0
    69f0:	8fc30004 	lw	v1,4(s8)
    69f4:	00621021 	addu	v0,v1,v0
    69f8:	00401825 	move	v1,v0
    69fc:	3c024e08 	lui	v0,0x4e08
    6a00:	344211a1 	ori	v0,v0,0x11a1
    6a04:	00621021 	addu	v0,v1,v0
    6a08:	afc20004 	sw	v0,4(s8)
    6a0c:	8fc20004 	lw	v0,4(s8)
    6a10:	00021ac2 	srl	v1,v0,0xb
    6a14:	00021540 	sll	v0,v0,0x15
    6a18:	00621025 	or	v0,v1,v0
    6a1c:	afc20004 	sw	v0,4(s8)
    6a20:	8fc30004 	lw	v1,4(s8)
    6a24:	8fc20008 	lw	v0,8(s8)
    6a28:	00621021 	addu	v0,v1,v0
    6a2c:	afc20004 	sw	v0,4(s8)
    6a30:	8fc2000c 	lw	v0,12(s8)
    6a34:	00021027 	nor	v0,zero,v0
    6a38:	8fc30004 	lw	v1,4(s8)
    6a3c:	00621025 	or	v0,v1,v0
    6a40:	8fc30008 	lw	v1,8(s8)
    6a44:	00621026 	xor	v0,v1,v0
    6a48:	00401825 	move	v1,v0
    6a4c:	8fc20020 	lw	v0,32(s8)
    6a50:	00621021 	addu	v0,v1,v0
    6a54:	8fc30000 	lw	v1,0(s8)
    6a58:	00621021 	addu	v0,v1,v0
    6a5c:	00401825 	move	v1,v0
    6a60:	3c02f753 	lui	v0,0xf753
    6a64:	34427e82 	ori	v0,v0,0x7e82
    6a68:	00621021 	addu	v0,v1,v0
    6a6c:	afc20000 	sw	v0,0(s8)
    6a70:	8fc20000 	lw	v0,0(s8)
    6a74:	00021980 	sll	v1,v0,0x6
    6a78:	00021682 	srl	v0,v0,0x1a
    6a7c:	00621025 	or	v0,v1,v0
    6a80:	afc20000 	sw	v0,0(s8)
    6a84:	8fc30000 	lw	v1,0(s8)
    6a88:	8fc20004 	lw	v0,4(s8)
    6a8c:	00621021 	addu	v0,v1,v0
    6a90:	afc20000 	sw	v0,0(s8)
    6a94:	8fc20008 	lw	v0,8(s8)
    6a98:	00021027 	nor	v0,zero,v0
    6a9c:	8fc30000 	lw	v1,0(s8)
    6aa0:	00621025 	or	v0,v1,v0
    6aa4:	8fc30004 	lw	v1,4(s8)
    6aa8:	00621026 	xor	v0,v1,v0
    6aac:	00401825 	move	v1,v0
    6ab0:	8fc2003c 	lw	v0,60(s8)
    6ab4:	00621021 	addu	v0,v1,v0
    6ab8:	8fc3000c 	lw	v1,12(s8)
    6abc:	00621021 	addu	v0,v1,v0
    6ac0:	00401825 	move	v1,v0
    6ac4:	3c02bd3a 	lui	v0,0xbd3a
    6ac8:	3442f235 	ori	v0,v0,0xf235
    6acc:	00621021 	addu	v0,v1,v0
    6ad0:	afc2000c 	sw	v0,12(s8)
    6ad4:	8fc2000c 	lw	v0,12(s8)
    6ad8:	00021a80 	sll	v1,v0,0xa
    6adc:	00021582 	srl	v0,v0,0x16
    6ae0:	00621025 	or	v0,v1,v0
    6ae4:	afc2000c 	sw	v0,12(s8)
    6ae8:	8fc3000c 	lw	v1,12(s8)
    6aec:	8fc20000 	lw	v0,0(s8)
    6af0:	00621021 	addu	v0,v1,v0
    6af4:	afc2000c 	sw	v0,12(s8)
    6af8:	8fc20004 	lw	v0,4(s8)
    6afc:	00021027 	nor	v0,zero,v0
    6b00:	8fc3000c 	lw	v1,12(s8)
    6b04:	00621025 	or	v0,v1,v0
    6b08:	8fc30000 	lw	v1,0(s8)
    6b0c:	00621026 	xor	v0,v1,v0
    6b10:	00401825 	move	v1,v0
    6b14:	8fc20018 	lw	v0,24(s8)
    6b18:	00621021 	addu	v0,v1,v0
    6b1c:	8fc30008 	lw	v1,8(s8)
    6b20:	00621021 	addu	v0,v1,v0
    6b24:	00401825 	move	v1,v0
    6b28:	3c022ad7 	lui	v0,0x2ad7
    6b2c:	3442d2bb 	ori	v0,v0,0xd2bb
    6b30:	00621021 	addu	v0,v1,v0
    6b34:	afc20008 	sw	v0,8(s8)
    6b38:	8fc20008 	lw	v0,8(s8)
    6b3c:	00021bc0 	sll	v1,v0,0xf
    6b40:	00021442 	srl	v0,v0,0x11
    6b44:	00621025 	or	v0,v1,v0
    6b48:	afc20008 	sw	v0,8(s8)
    6b4c:	8fc30008 	lw	v1,8(s8)
    6b50:	8fc2000c 	lw	v0,12(s8)
    6b54:	00621021 	addu	v0,v1,v0
    6b58:	afc20008 	sw	v0,8(s8)
    6b5c:	8fc20000 	lw	v0,0(s8)
    6b60:	00021027 	nor	v0,zero,v0
    6b64:	8fc30008 	lw	v1,8(s8)
    6b68:	00621025 	or	v0,v1,v0
    6b6c:	8fc3000c 	lw	v1,12(s8)
    6b70:	00621026 	xor	v0,v1,v0
    6b74:	00401825 	move	v1,v0
    6b78:	8fc20034 	lw	v0,52(s8)
    6b7c:	00621021 	addu	v0,v1,v0
    6b80:	8fc30004 	lw	v1,4(s8)
    6b84:	00621021 	addu	v0,v1,v0
    6b88:	00401825 	move	v1,v0
    6b8c:	3c02eb86 	lui	v0,0xeb86
    6b90:	3442d391 	ori	v0,v0,0xd391
    6b94:	00621021 	addu	v0,v1,v0
    6b98:	afc20004 	sw	v0,4(s8)
    6b9c:	8fc20004 	lw	v0,4(s8)
    6ba0:	00021ac2 	srl	v1,v0,0xb
    6ba4:	00021540 	sll	v0,v0,0x15
    6ba8:	00621025 	or	v0,v1,v0
    6bac:	afc20004 	sw	v0,4(s8)
    6bb0:	8fc30004 	lw	v1,4(s8)
    6bb4:	8fc20008 	lw	v0,8(s8)
    6bb8:	00621021 	addu	v0,v1,v0
    6bbc:	afc20004 	sw	v0,4(s8)
    6bc0:	dfc20110 	ld	v0,272(s8)
    6bc4:	8c420000 	lw	v0,0(v0)
    6bc8:	8fc30000 	lw	v1,0(s8)
    6bcc:	00621021 	addu	v0,v1,v0
    6bd0:	00401825 	move	v1,v0
    6bd4:	dfc20110 	ld	v0,272(s8)
    6bd8:	ac430000 	sw	v1,0(v0)
    6bdc:	dfc20110 	ld	v0,272(s8)
    6be0:	64420004 	daddiu	v0,v0,4
    6be4:	8c430000 	lw	v1,0(v0)
    6be8:	dfc20110 	ld	v0,272(s8)
    6bec:	64420004 	daddiu	v0,v0,4
    6bf0:	8fc40004 	lw	a0,4(s8)
    6bf4:	00831821 	addu	v1,a0,v1
    6bf8:	ac430000 	sw	v1,0(v0)
    6bfc:	dfc20110 	ld	v0,272(s8)
    6c00:	64420008 	daddiu	v0,v0,8
    6c04:	8c430000 	lw	v1,0(v0)
    6c08:	dfc20110 	ld	v0,272(s8)
    6c0c:	64420008 	daddiu	v0,v0,8
    6c10:	8fc40008 	lw	a0,8(s8)
    6c14:	00831821 	addu	v1,a0,v1
    6c18:	ac430000 	sw	v1,0(v0)
    6c1c:	dfc20110 	ld	v0,272(s8)
    6c20:	6442000c 	daddiu	v0,v0,12
    6c24:	8c430000 	lw	v1,0(v0)
    6c28:	dfc20110 	ld	v0,272(s8)
    6c2c:	6442000c 	daddiu	v0,v0,12
    6c30:	8fc4000c 	lw	a0,12(s8)
    6c34:	00831821 	addu	v1,a0,v1
    6c38:	ac430000 	sw	v1,0(v0)
    6c3c:	00000000 	nop
    6c40:	03c0e825 	move	sp,s8
    6c44:	dfbf0138 	ld	ra,312(sp)
    6c48:	dfbe0130 	ld	s8,304(sp)
    6c4c:	dfbc0128 	ld	gp,296(sp)
    6c50:	67bd0140 	daddiu	sp,sp,320
    6c54:	03e00008 	jr	ra
    6c58:	00000000 	nop
    6c5c:	00000000 	nop
    6c60:	67bdffe0 	daddiu	sp,sp,-32
    6c64:	ffbc0010 	sd	gp,16(sp)
    6c68:	3c1c0002 	lui	gp,0x2
    6c6c:	0399e02d 	daddu	gp,gp,t9
    6c70:	679c13f0 	daddiu	gp,gp,5104
    6c74:	df838038 	ld	v1,-32712(gp)
    6c78:	2402ffff 	li	v0,-1
    6c7c:	dc79ffe0 	ld	t9,-32(v1)
    6c80:	ffbf0018 	sd	ra,24(sp)
    6c84:	ffb10008 	sd	s1,8(sp)
    6c88:	13220008 	beq	t9,v0,6cac <main+0x55dc>
    6c8c:	ffb00000 	sd	s0,0(sp)
    6c90:	2411ffff 	li	s1,-1
    6c94:	6470ffe0 	daddiu	s0,v1,-32
    6c98:	0320f809 	jalr	t9
    6c9c:	00000000 	nop
    6ca0:	de19fff8 	ld	t9,-8(s0)
    6ca4:	1731fffc 	bne	t9,s1,6c98 <main+0x55c8>
    6ca8:	6610fff8 	daddiu	s0,s0,-8
    6cac:	dfbf0018 	ld	ra,24(sp)
    6cb0:	dfbc0010 	ld	gp,16(sp)
    6cb4:	dfb10008 	ld	s1,8(sp)
    6cb8:	dfb00000 	ld	s0,0(sp)
    6cbc:	03e00008 	jr	ra
    6cc0:	67bd0020 	daddiu	sp,sp,32
	...

Disassembly of section .MIPS.stubs:

0000000000006cd0 <.MIPS.stubs>:
    6cd0:	df998010 	ld	t9,-32752(gp)
    6cd4:	03e07825 	move	t3,ra
    6cd8:	0320f809 	jalr	t9
    6cdc:	64180046 	daddiu	t8,zero,70
    6ce0:	df998010 	ld	t9,-32752(gp)
    6ce4:	03e07825 	move	t3,ra
    6ce8:	0320f809 	jalr	t9
    6cec:	64180045 	daddiu	t8,zero,69
    6cf0:	df998010 	ld	t9,-32752(gp)
    6cf4:	03e07825 	move	t3,ra
    6cf8:	0320f809 	jalr	t9
    6cfc:	64180044 	daddiu	t8,zero,68
    6d00:	df998010 	ld	t9,-32752(gp)
    6d04:	03e07825 	move	t3,ra
    6d08:	0320f809 	jalr	t9
    6d0c:	64180043 	daddiu	t8,zero,67
    6d10:	df998010 	ld	t9,-32752(gp)
    6d14:	03e07825 	move	t3,ra
    6d18:	0320f809 	jalr	t9
    6d1c:	64180041 	daddiu	t8,zero,65
    6d20:	df998010 	ld	t9,-32752(gp)
    6d24:	03e07825 	move	t3,ra
    6d28:	0320f809 	jalr	t9
    6d2c:	64180040 	daddiu	t8,zero,64
    6d30:	df998010 	ld	t9,-32752(gp)
    6d34:	03e07825 	move	t3,ra
    6d38:	0320f809 	jalr	t9
    6d3c:	6418003f 	daddiu	t8,zero,63
    6d40:	df998010 	ld	t9,-32752(gp)
    6d44:	03e07825 	move	t3,ra
    6d48:	0320f809 	jalr	t9
    6d4c:	6418003e 	daddiu	t8,zero,62
    6d50:	df998010 	ld	t9,-32752(gp)
    6d54:	03e07825 	move	t3,ra
    6d58:	0320f809 	jalr	t9
    6d5c:	6418003a 	daddiu	t8,zero,58
    6d60:	df998010 	ld	t9,-32752(gp)
    6d64:	03e07825 	move	t3,ra
    6d68:	0320f809 	jalr	t9
    6d6c:	64180039 	daddiu	t8,zero,57
    6d70:	df998010 	ld	t9,-32752(gp)
    6d74:	03e07825 	move	t3,ra
    6d78:	0320f809 	jalr	t9
    6d7c:	64180038 	daddiu	t8,zero,56
    6d80:	df998010 	ld	t9,-32752(gp)
    6d84:	03e07825 	move	t3,ra
    6d88:	0320f809 	jalr	t9
    6d8c:	64180037 	daddiu	t8,zero,55
    6d90:	df998010 	ld	t9,-32752(gp)
    6d94:	03e07825 	move	t3,ra
    6d98:	0320f809 	jalr	t9
    6d9c:	64180035 	daddiu	t8,zero,53
    6da0:	df998010 	ld	t9,-32752(gp)
    6da4:	03e07825 	move	t3,ra
    6da8:	0320f809 	jalr	t9
    6dac:	64180034 	daddiu	t8,zero,52
    6db0:	df998010 	ld	t9,-32752(gp)
    6db4:	03e07825 	move	t3,ra
    6db8:	0320f809 	jalr	t9
    6dbc:	64180032 	daddiu	t8,zero,50
    6dc0:	df998010 	ld	t9,-32752(gp)
    6dc4:	03e07825 	move	t3,ra
    6dc8:	0320f809 	jalr	t9
    6dcc:	64180031 	daddiu	t8,zero,49
    6dd0:	df998010 	ld	t9,-32752(gp)
    6dd4:	03e07825 	move	t3,ra
    6dd8:	0320f809 	jalr	t9
    6ddc:	6418002f 	daddiu	t8,zero,47
	...

Disassembly of section .fini:

0000000000006df0 <_fini>:
    6df0:	67bdffe0 	daddiu	sp,sp,-32
    6df4:	ffbf0018 	sd	ra,24(sp)
    6df8:	ffbc0010 	sd	gp,16(sp)
    6dfc:	3c010002 	lui	at,0x2
    6e00:	24211260 	addiu	at,at,4704
    6e04:	0039e02d 	daddu	gp,at,t9
    6e08:	04110001 	bal	6e10 <_fini+0x20>
    6e0c:	00000000 	nop
    6e10:	03801025 	move	v0,gp
    6e14:	3c1c0002 	lui	gp,0x2
    6e18:	279c1240 	addiu	gp,gp,4672
    6e1c:	039fe02d 	daddu	gp,gp,ra
    6e20:	df998060 	ld	t9,-32672(gp)
    6e24:	0320f809 	jalr	t9
    6e28:	00000000 	nop
    6e2c:	dfbf0018 	ld	ra,24(sp)
    6e30:	dfbc0010 	ld	gp,16(sp)
    6e34:	03e00008 	jr	ra
    6e38:	67bd0020 	daddiu	sp,sp,32
