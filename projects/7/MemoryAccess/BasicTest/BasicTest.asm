// VM: // This file is part of www.nand2tetris.org

// VM: // and the book "The Elements of Computing Systems"

// VM: // by Nisan and Schocken, MIT Press.

// VM: 

// VM: // Executes pop and push commands.

// VM: 

// VM: push constant 10
@10
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop local 0
@LCL
D=M
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

// VM: push constant 21
@21
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 22
@22
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop argument 2
@ARG
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

// VM: pop argument 1
@ARG
D=M
@1
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

// VM: push constant 36
@36
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop this 6
@THIS
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

// VM: push constant 42
@42
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 45
@45
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop that 5
@THAT
D=M
@5
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

// VM: pop that 2
@THAT
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

// VM: push constant 510
@510
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: pop temp 6
@5
D=A
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

// VM: push local 0
@LCL
D=M
@0
A=D+A
D=M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push that 5
@THAT
D=M
@5
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


// VM: push argument 1
@ARG
D=M
@1
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


// VM: push this 6
@THIS
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

// VM: push this 6
@THIS
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


// VM: push temp 6
@5

D=A
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


