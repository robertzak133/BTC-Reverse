	.file	1 "patch.c"
	.section .mdebug.abi32
	.previous
	.nan	legacy
	.module	fp=xx
	.module	nooddspreg
	.text
	.rdata
	.align	2
$LC0:
	.ascii	"WBWL:Warning -- digital mode %d not supported in patched"
	.ascii	" firmware\000"
	.align	2
$LC1:
	.ascii	"WBWL:set_digital_effect %d\012\000"
	.text
	.align	2
	.globl	setDigitalEffect
	.set	nomips16
	.set	nomicromips
	.ent	setDigitalEffect
	.type	setDigitalEffect, @function
setDigitalEffect:
	.frame	$fp,24,$31		# vars= 0, regs= 2/0, args= 16, gp= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro
	addiu	$sp,$sp,-24
	sw	$31,20($sp)
	sw	$fp,16($sp)
	move	$fp,$sp
	sw	$4,24($fp)
	sw	$5,28($fp)
	sw	$6,32($fp)
	sw	$7,36($fp)
	lw	$2,24($fp)
	beq	$2,$0,$L2
	nop

	lw	$2,24($fp)
	li	$3,1			# 0x1
	beq	$2,$3,$L2
	nop

	lw	$5,24($fp)
	lui	$2,%hi($LC0)
	addiu	$4,$2,%lo($LC0)
	jal	tty_printf
	nop

	sw	$0,24($fp)
$L2:
	lw	$5,24($fp)
	lui	$2,%hi($LC1)
	addiu	$4,$2,%lo($LC1)
	jal	tty_printf
	nop

	lw	$2,24($fp)
	bne	$2,$0,$L3
	nop

	lui	$2,%hi(BYTE_80439978)
	lb	$2,%lo(BYTE_80439978)($2)
	beq	$2,$0,$L4
	nop

	jal	get_DAT_80357b60_at_global_index
	nop

	sll	$2,$2,24
	sra	$2,$2,24
	lui	$3,%hi(BYTE_80439979)
	sb	$2,%lo(BYTE_80439979)($3)
	lui	$2,%hi(BYTE_80439979)
	lb	$2,%lo(BYTE_80439979)($2)
	andi	$2,$2,0x00ff
	move	$4,$2
	jal	FUN_800d15ec
	nop

	li	$2,131072			# 0x20000
	ori	$7,$2,0x2001
	li	$6,1			# 0x1
	move	$5,$0
	li	$4,35			# 0x23
	jal	FUN_800c3d28
	nop

	lui	$2,%hi(BYTE_80439979)
	lb	$2,%lo(BYTE_80439979)($2)
	andi	$2,$2,0x00ff
	move	$4,$2
	jal	FUN_800d15a0
	nop

$L4:
	move	$5,$0
	li	$2,131072			# 0x20000
	ori	$4,$2,0x2001
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$4,43			# 0x2b
	jal	sp5kIqBlockEnable
	nop

	move	$5,$0
	li	$4,44			# 0x2c
	jal	sp5kIqBlockEnable
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2000
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2001
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2002
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2003
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2004
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2005
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2006
	jal	sp5kIqCfgSet
	nop

	li	$5,1			# 0x1
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2019
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201a
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201b
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201c
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201d
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2007
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2008
	jal	sp5kIqCfgSet
	nop

	li	$5,3			# 0x3
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2009
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x200a
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x200b
	jal	sp5kIqCfgSet
	nop

	li	$5,7			# 0x7
	li	$2,262144			# 0x40000
	ori	$4,$2,0x200c
	jal	sp5kIqCfgSet
	nop

	li	$5,7			# 0x7
	li	$2,262144			# 0x40000
	ori	$4,$2,0x200d
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x200e
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x200f
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2010
	jal	sp5kIqCfgSet
	nop

	li	$5,128			# 0x80
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2011
	jal	sp5kIqCfgSet
	nop

	li	$5,128			# 0x80
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2012
	jal	sp5kIqCfgSet
	nop

	li	$5,128			# 0x80
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2013
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2014
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2015
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2016
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2017
	jal	sp5kIqCfgSet
	nop

	li	$5,255			# 0xff
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2018
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201e
	jal	sp5kIqCfgSet
	nop

	li	$5,1			# 0x1
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201f
	jal	sp5kIqCfgSet
	nop

	li	$5,1			# 0x1
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2020
	jal	sp5kIqCfgSet
	nop

	lui	$2,%hi(DAT_803e7298)
	addiu	$2,$2,%lo(DAT_803e7298)
	move	$5,$2
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2021
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2022
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2023
	jal	sp5kIqCfgSet
	nop

	li	$5,1			# 0x1
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2024
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2025
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2026
	jal	sp5kIqCfgSet
	nop

	b	$L1
	nop

$L3:
	lui	$2,%hi(s_Digital_Effect_BW_803abef7+1)
	addiu	$2,$2,%lo(s_Digital_Effect_BW_803abef7+1)
	move	$4,$2
	jal	debug_printf
	nop

	lui	$2,%hi(BYTE_80439978)
	lb	$2,%lo(BYTE_80439978)($2)
	beq	$2,$0,$L6
	nop

	jal	get_DAT_80357b60_at_global_index
	nop

	sll	$2,$2,24
	sra	$2,$2,24
	lui	$3,%hi(BYTE_80439979)
	sb	$2,%lo(BYTE_80439979)($3)
	lui	$2,%hi(BYTE_80439979)
	lb	$2,%lo(BYTE_80439979)($2)
	andi	$2,$2,0x00ff
	move	$4,$2
	jal	FUN_800d15ec
	nop

	li	$2,131072			# 0x20000
	ori	$7,$2,0x2001
	li	$6,1			# 0x1
	move	$5,$0
	li	$4,35			# 0x23
	jal	FUN_800c3d28
	nop

	lui	$2,%hi(BYTE_80439979)
	lb	$2,%lo(BYTE_80439979)($2)
	andi	$2,$2,0x00ff
	move	$4,$2
	jal	FUN_800d15a0
	nop

$L6:
	lui	$2,%hi(BYTE_80439978)
	sb	$0,%lo(BYTE_80439978)($2)
	move	$5,$0
	li	$2,131072			# 0x20000
	ori	$4,$2,0x2001
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2015
	jal	sp5kIqCfgSet
	nop

	move	$5,$0
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2016
	jal	sp5kIqCfgSet
	nop

	li	$5,1			# 0x1
	li	$2,262144			# 0x40000
	ori	$4,$2,0x201f
	jal	sp5kIqCfgSet
	nop

	lui	$2,%hi(DAT_8043997c)
	addiu	$2,$2,%lo(DAT_8043997c)
	move	$5,$2
	li	$2,262144			# 0x40000
	ori	$4,$2,0x2021
	jal	sp5kIqCfgSet
	nop

	nop
$L1:
	move	$sp,$fp
	lw	$31,20($sp)
	lw	$fp,16($sp)
	addiu	$sp,$sp,24
	jr	$31
	nop

	.set	macro
	.set	reorder
	.end	setDigitalEffect
	.size	setDigitalEffect, .-setDigitalEffect
	.ident	"GCC: (Ubuntu 8.4.0-1ubuntu1~18.04) 8.4.0"
