// VM: // This file is part of www.nand2tetris.org

// VM: // and the book "The Elements of Computing Systems"

// VM: // by Nisan and Schocken, MIT Press.

// VM: 

// VM: // Executes a sequence of arithmetic and logical operations on the stack.

// VM: 

// VM: push constant 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.1
D;JEQ
D=0
@END_COND.1
0;JMP
(TRUE_COND.1)
D=-1
(END_COND.1)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 16
@16
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.2
D;JEQ
D=0
@END_COND.2
0;JMP
(TRUE_COND.2)
D=-1
(END_COND.2)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 16
@16
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 17
@17
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.3
D;JEQ
D=0
@END_COND.3
0;JMP
(TRUE_COND.3)
D=-1
(END_COND.3)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 892
@892
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 891
@891
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.4
D;JLT
D=0
@END_COND.4
0;JMP
(TRUE_COND.4)
D=-1
(END_COND.4)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 891
@891
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 892
@892
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.5
D;JLT
D=0
@END_COND.5
0;JMP
(TRUE_COND.5)
D=-1
(END_COND.5)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 891
@891
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 891
@891
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.6
D;JLT
D=0
@END_COND.6
0;JMP
(TRUE_COND.6)
D=-1
(END_COND.6)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 32767
@32767
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.7
D;JGT
D=0
@END_COND.7
0;JMP
(TRUE_COND.7)
D=-1
(END_COND.7)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 32767
@32767
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.8
D;JGT
D=0
@END_COND.8
0;JMP
(TRUE_COND.8)
D=-1
(END_COND.8)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 32766
@32766
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=M-D
@TRUE_COND.9
D;JGT
D=0
@END_COND.9
0;JMP
(TRUE_COND.9)
D=-1
(END_COND.9)
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 57
@57
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 31
@31
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: push constant 53
@53
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


// VM: push constant 112
@112
D=A
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


// VM: neg
@SP
M=M-1
A=M
D=M

D=-D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=D&M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: push constant 82
@82
D=A
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1

// VM: or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M

D=D|M
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


// VM: not
@SP
M=M-1
A=M
D=M

D=!D
// RAM[SP] = D
@SP
A=M
M=D
// SP++
@SP
M=M+1


