// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.


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
  @RETURN
  D;JEQ

  // R2 += R0
  @2
  D=M
  @0
  D=D+M
  @2
  M=D

  // R3 -= 1
  @3
  D=M
  D=D-1
  M=D

  // Go back to the LOOP
  @LOOP
  0;JMP

(RETURN) // INFINITE LOOP
  @RETURN
  0;JMP

// End
