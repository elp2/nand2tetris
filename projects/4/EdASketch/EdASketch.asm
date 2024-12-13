@100
D=A
@x
M=D

@100
D=A
@y
M=D

(READKEYBOARD)
  @KBD
  D=M
  // left arrow 130
  @130
  D=D-A
  @LEFT
  D;JEQ

  // up arrow 131
  D=D-1
  @UP
  D;JEQ

  // right arrow 132
  D=D-1
  @RIGHT
  D;JEQ

  // down arrow 133
  D=D-1
  @DOWN
  D;JEQ

  // Else keep reading input.
  @READKEYBOARD
  0;JMP

(LEFT)
  @x
  M=M-1
  @DRAWXY
  0;JMP

(RIGHT)
  @x
  M=M+1
  @DRAWXY
  0;JMP

(UP)
  @y
  M=M-1
  @DRAWXY
  0;JMP

(DOWN)
  @y
  M=M+1
  @DRAWXY
  0;JMP

(DRAWXY)
  @SCREEN
  D=A
  @x
  D=D+M
  A=D
  M=-1

  @READKEYBOARD
  0;JMP

// TODO: Untested!!!
// R2 = R0 * R1 (overwrites R3), JMP's back to R15
(MULT)
  // R2 = 0
  @2
  M=0

  // R3 = R1
  @1
  D=M
  @3
  M=D

// If R3 == 0, out result should be good in R2
(LOOP)
  // D must be R3 at this point
  @MULTRETURN
  D;JEQ

  // R2 += R0
  @R2
  D=M
  @R0
  D=D+M
  @R2
  M=D

  // R3 -= 1
  @R3
  D=M
  D=D-1
  M=D

  // Go back to the LOOP
  @LOOP
  0;JMP

(MULTRETURN)
@R15
0;JMP