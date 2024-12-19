// VM: // This file is part of www.nand2tetris.org

// VM: // and the book "The Elements of Computing Systems"

// VM: // by Nisan and Schocken, MIT Press.

// VM: 

// VM: // Executes pop and push commands using the

// VM: // pointer, this, and that segments.

// VM: 

// VM: push constant 3030
@3030
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D

// VM: push constant 3040
@3040
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D

// VM: push constant 32
@32
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop this 2
@THIS
D=M
@2
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

// VM: push constant 46
@46
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop that 6
@THAT
D=M
@6
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

// VM: push pointer 0
@THIS
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push pointer 1
@THAT
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


// VM: push this 2
@THIS
D=M
@2
A=D+A
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


// VM: push that 6
@THAT
D=M
@6
A=D+A
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


