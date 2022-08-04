// push constant 7

@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8

@8
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
