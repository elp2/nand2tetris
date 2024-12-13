@yi

// Initialize offset for drawing. 
// We'll move this manually by the right size without needing underlying x, y.
@SCREEN
D=A
@500
D=D+A
@offset
M=D

// X, Y. At the level of the 
// Unused, since the looping on Y made it was too slow.
@10
D=A
@y
M=D

@10
D=A
@x
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
  // @x
  // M=M-1
  @offset
  M=M-1
  
  @DRAWXY
  0;JMP

(RIGHT)
  // @x
  // M=M+1
  @offset
  M=M+1
  @DRAWXY
  0;JMP

(UP)
  // @y
  // M=M-1
  @32
  D=A
  @offset
  M=M-D

  @DRAWXY
  0;JMP

(DOWN)
  // @y
  // M=M+1
  @32
  D=A
  @offset
  M=D+M

  @DRAWXY
  0;JMP

(DRAWXY)
  @offset
  A=M
  M=-1
  @READKEYBOARD
  0;JMP


(DRAWXYOLD)
  // The (row, col) pixel in the physical screen is represented by
  // the (col % 16)th bit in RAM address SCREEN + 32*row + col/16
  // Offset from Screen = 0
  @0
  D=A
  @offset
  M=D

  // yi = y
  @y
  D=M
  @yi
  M=D

(ADDY) // While y != 0: offset += 32, y --
  @yi
  D=M
  @ADDX
  D;JEQ
  @yi
  M=M-1
  @32
  D=A
  @offset
  M=D+M
  @ADDY
  0;JMP

(ADDX)
//  @x
//  D=A
//  @offset
//  M=D+M

// Draw it
  @offset
  D=M
  @SCREEN
  D=D+M

  A=D
  M=-1

  @READKEYBOARD
  0;JMP