// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(START)
@KBD 
D = M
@WHITE
D; JEQ // if not pressed, white screen
@screenVal 
M=-1 //if pressed, black screen
@PAINT_SCREEN
0; JMP //start paint

(WHITE)
@screenVal
M=0 //start paint

(PAINT_SCREEN)
@8192 // else set screen to black
D = A
@rep //repetitions = 8192
M = D

@i
M = 0 //initialize i as 0

(LOOP)
@i 
D = M 
@rep 
D = M - D
@STOP
D; JLE // stop if i >= rep

@i 
D = M
@SCREEN 
D = A + D
@currAdd
M = D //store screen + i in m[currAdd]

@screenVal
D = M //get value to paint
@currAdd
A = M //get address to paint
M = D //paint m[screen + i]

@i 
M = M + 1 // i = i + 1
@LOOP
0; JMP // loop

(STOP)
@START
0; JMP //wait for next key


