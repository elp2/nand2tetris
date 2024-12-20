// VM: // This file is part of www.nand2tetris.org

// VM: // and the book "The Elements of Computing Systems"

// VM: // by Nisan and Schocken, MIT Press.

// VM: 

// VM: // Executes pop and push commands using the static segment.

// VM: 

// VM: push constant 111
@111
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 333
@333
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 888
@888
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop static 8
@StaticTest.8
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// VM: pop static 3
@StaticTest.3
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// VM: pop static 1
@StaticTest.1
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

// VM: push static 3
@StaticTest.3
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push static 1
@StaticTest.1
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push static 8
@StaticTest.8
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=D+M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


