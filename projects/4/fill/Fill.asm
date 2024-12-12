// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

// Set fill to zero
@fill
M=0

(READKEYBOARD)
  // Read the keyboard
  @KBD
  D=M
  @FILLBLACK
  D;JNE

(FILLWHITE)
  @fill
  M=0
  @FILLSCREENSETUP
  0;JEQ

(FILLBLACK)
  @fill
  M=-1

  // Fill = 0xFF if keyboard pressed, else 0x00
(FILLSCREENSETUP)
  // @pixel = SCREEN
  @SCREEN
  D=A
  @pixel
  M=D

(SCREENLOOP)
  // M[@pixel] = @fill
  @fill
  D=M
  @pixel
  A=M
  M=D
  
  // @pixel += 1
  @pixel
  M=M+1
  D=M

  @KBD
  D=A-D
  @READKEYBOARD
  D;JEQ

  @SCREENLOOP
  0;JEQ
  
  // Otherwise, continue filling loop.
  @READKEYBOARD
  0;JMP