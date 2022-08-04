// push constant 111

@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 333

@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 888

@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8

@SP
AM=M-1
D=M
@sta8
M=D
// pop static 3

@SP
AM=M-1
D=M
@sta3
M=D
// pop static 1

@SP
AM=M-1
D=M
@sta1
M=D
// push static 3

@sta3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1

@sta1
D=M
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
// push static 8

@sta8
D=M
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
