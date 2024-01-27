# Weekly Report 

## What did I do this week?
Mainly I did three things.

I did a lot of reading regarding the programming of a chess engine. Especially [Chess programming wiki](https://www.chessprogramming.org/Getting_Started)
is quite good as it covers alot of topics. Furthermore, I did some reading regarding the [FEN notation](https://www.chess.com/terms/fen-chess#what-is-fen) as it is very important
for the engine.

In addition to that I tried to read about / how to write the [UCI interface](https://github.com/fsmosca/UCIChessEngineProtocol).
For that at the moment I copied a minimalistic version ([GitHub](https://github.com/healeycodes/andoma/blob/main/communication.py)) which I want to expand later on.

I spent the most time on the actual implementation of the chess rules and the calculation of all the legal moves.

## How has the project progressed?
* I did change the project structure for a more clear structure.
* I did implement the basic rules for legal moves
  * Legal moves for all pieces regarding free spaces / captures / enPassant
  * Still missing:
    * castling
    * checks for check / bindings
* Basic UCI interface


## What did I learn this week?
I did learn alot about FEN Strings, the programming of a UCI interface and how to program the rules for chess. 
I learned that the move generation is not as straight forward as I would have guessed and that I still have to implement
alot and optimize it so that it works as it should.


## What has been unclear or problematic?
I had two problems: The first one was that I didn't really know how to write the UCI interface and how the GUI talks to the engine.
Luckily I found the above linked UCI implementation which I was able to use as a starting point. Now I do understand the
idea of the interface alot more.

The other problem was that I started too early with the implementation of the rules. I think it was a good idea to do the
implementation first before doing the best_move calculation (so instead of using a library for the beginning) as I learned
alot which I think will help me later. But I messed up the creation of the board from the FEN string and because of that
I did have alot of errors and problems with the indexes for my board array. Luckily I was able to fix everything, but I did cost
me much more time than it should have.

## What are my next steps?
My next steps are to implement the missing policies (castling, check detection, ...) so the rules are complete and
write test cases for this.
After that the basic "engine" stands and I can start the best_move generation.

Furthermore, I want to do one last refactoring of the existing files so that the naming and contents of the files are
easy to understand.


## Weekly hours
25h