// VM: // This file is part of www.nand2tetris.org

// VM: // and the book "The Elements of Computing Systems"

// VM: // by Nisan and Schocken, MIT Press.

// VM: 

// VM: // Pushes and adds two constants.

// VM: 

// VM: push constant 7
@7
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 8
@8
D=A
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


