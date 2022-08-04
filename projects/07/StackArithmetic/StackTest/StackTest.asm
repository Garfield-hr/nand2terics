// push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_0
D;JEQ
@LOGICAL_OP_OUTSIDE_0
D=0;JMP
(LOGICAL_OP_TRUE_0)
D=-1
(LOGICAL_OP_OUTSIDE_0)
@SP
A=M
M=D
@SP
M=M+1
// push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16

@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_1
D;JEQ
@LOGICAL_OP_OUTSIDE_1
D=0;JMP
(LOGICAL_OP_TRUE_1)
D=-1
(LOGICAL_OP_OUTSIDE_1)
@SP
A=M
M=D
@SP
M=M+1
// push constant 16

@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17

@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_2
D;JEQ
@LOGICAL_OP_OUTSIDE_2
D=0;JMP
(LOGICAL_OP_TRUE_2)
D=-1
(LOGICAL_OP_OUTSIDE_2)
@SP
A=M
M=D
@SP
M=M+1
// push constant 892

@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_3
D;JLT
@LOGICAL_OP_OUTSIDE_3
D=0;JMP
(LOGICAL_OP_TRUE_3)
D=-1
(LOGICAL_OP_OUTSIDE_3)
@SP
A=M
M=D
@SP
M=M+1
// push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892

@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_4
D;JLT
@LOGICAL_OP_OUTSIDE_4
D=0;JMP
(LOGICAL_OP_TRUE_4)
D=-1
(LOGICAL_OP_OUTSIDE_4)
@SP
A=M
M=D
@SP
M=M+1
// push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891

@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_5
D;JLT
@LOGICAL_OP_OUTSIDE_5
D=0;JMP
(LOGICAL_OP_TRUE_5)
D=-1
(LOGICAL_OP_OUTSIDE_5)
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_6
D;JGT
@LOGICAL_OP_OUTSIDE_6
D=0;JMP
(LOGICAL_OP_TRUE_6)
D=-1
(LOGICAL_OP_OUTSIDE_6)
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767

@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_7
D;JGT
@LOGICAL_OP_OUTSIDE_7
D=0;JMP
(LOGICAL_OP_TRUE_7)
D=-1
(LOGICAL_OP_OUTSIDE_7)
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766

@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@LOGICAL_OP_TRUE_8
D;JGT
@LOGICAL_OP_OUTSIDE_8
D=0;JMP
(LOGICAL_OP_TRUE_8)
D=-1
(LOGICAL_OP_OUTSIDE_8)
@SP
A=M
M=D
@SP
M=M+1
// push constant 57

@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31

@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53

@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D+M
@SP
A=M
M=D
@SP
M=M+1
// push constant 112

@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D-M
@SP
A=M
M=D
@SP
M=M+1
// neg

@SP
AM=M-1
D=M
D=-D
@SP
A=M
M=D
@SP
M=M+1
// and

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D&M
@SP
A=M
M=D
@SP
M=M+1
// push constant 82

@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or

@SP
AM=M-1
D=M
@13
M=D
@SP
AM=M-1
D=M
@13
D=D|M
@SP
A=M
M=D
@SP
M=M+1
// not

@SP
AM=M-1
D=M
D=!D
@SP
A=M
M=D
@SP
M=M+1
