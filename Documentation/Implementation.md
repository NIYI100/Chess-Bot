# Implementation Document
This document describes the implementation of my project, a UCI chess engine.

## General Structure of the program
The programm is parted into different parts. The program is started via [main.py](/Application/main.py)
which calls [communication.py](/Application/communication.py).

### Application

[BoardModel](/Application/BoardModel) contains the code that describes the state of the chess game as well as
methods to convert the BoardState object to FEN strings and the other way around.

[Constants](/Application/Constants) contains the constants used in the project. This includes constants for
the different pieces and colors.

[MoveGeneration](/Application/MoveGeneration) contains the methods used for generating the legal moves
and calculating the best move in the current state.

[TranspositionTable](/Application/TranspositionTable) contains the code for the transposition table as well as
the Zobrist key calculations.

[communication.py](/Application/communication.py) is the main loop for the uci engine. In this the program
listens to the inputs and executes the resulting methods.

### Tests
The [Tests](/Tests) contains the Unit tests. The [tests.py](/Tests/test.py) file executes all the tests.
The Tests folder follows the same structure as the Application folder.


## Features and implementation details
I use the negaMax algorithm with some optimizations to calculate the best move:

### NegaMax Algorithm with Alpha-Beta pruning
The main way of searching for the best move is the NegaMax algorithm. It´s a version of the MiniMax algorithm
that combines the maximizing and minimzing part of the MiniMax algorithm into one method.
In addidtion to that we use Alpha-Beta pruning to cut-off sub trees where we know they cant lead to a
better result. This works because the best result of the one player is the worst result of the other player.

### Iterative deepening
Iterative deepening defines a technique where iteratively the searched depth is increased. This works very
well in combination with a [transposition table](#Transposition-table) and [LMR](#late-move-reduction-lmr).
The techniques are used to order the moves with the evaluation calculated in the previous iteration.
The idea behind that is that a move that is good in a previous iteration is probaply also good in a later iteration
and will lead to a lot of cut-offs.

### Transposition table
A transposition table is a hash table in which information about a corresponding BoardState and most importantly
the evaluation corresponding to this BoardState is saved.
In the [NegaMax](#negamax-algorithm-with-alpha-beta-pruning) algorithm before going more in depth a lookup
in the transposition table is used. If there is an evaluation and the result can be used no further search has to be
done for that position

### Late Move Reduction (LMR)
LMR describes a technique which roots on the idea of good move ordering. In our case it harmonizes with
[Iterative deepening](#iterative-deepening) and the [Transposition table](#transposition-table). The idea is
that after move ordering the first moves should have more time to get calculated in depth in comparison to moves that are
later in the sorted moves list. This is because the earlier moves are probaply better. LMR cuts the searched depth of later
moves.

Of course, if any of the later moves is find to be better than expected a full search for that state will be
done.

### Quiescence Search
Quiescence Search describes a technique to counter the [Horizon effect (Wikipedia)](https://en.wikipedia.org/wiki/Horizon_effect).
This effect describes a state of the board where we have search to full depth and return a (as it seems) favorable
positon (As an example: lets say our last move was a queen move that captured a pawn, so we are up in material). The
problem: As we stopped the search the next counter move could lead to a worse state for us (In the example: An enemy piece
can capture our queen. So we didnt capture a pawn, but blundered our queen). To counteract this we do a furth search
from the leaf nodes where we only look at possible capture-chains. If at the end of the capture chain the
evaluation is still positive then we can do this move.

## Time and space complexity
The time complexity of the algorithm is O(b^n) where b is the amount of branches (legal moves) in the MiniMax algorithm
and n is the depth of the search. Even with alpha-beta pruning and the other optimizations in the O-notation it doesn't change.
Still the speed up of over the basic algorithm is very high.

The space is O(b * n) for the default algorithm. The use of a transposition table doesn't change that, as we are using a static sized table


## Shortcomings / suggested improvements
A few improvements that could be made:
* Refactoring of the BoardState object to not use lists but a smaller representation of the board.
Maybe a bitmap or even using the FEN string directly
* Further optimizations on the search methods to make them faster. An example could be to use a better move ordering
method to have more cut-offs
* A better evaluation function. The function only evaluates the board in a very basic way. Especially in
the endgame this evaluation function doesnt work that good.
* Opening / endgame book - To speed up the opening / endgame.

## Use of Chat-GPT and other LLM´s
I used Chat-GPT 3.5 for general informations regarding chess programming, different evaluation functions, optimization methods
and so on. I generated code for that, but didnt directly use it. It was only used to get a feeling of the
pseudocode.

## References
* [Building an own Chess AI (Accessed: 05.03.2024)](https://healeycodes.com/building-my-own-chess-engine)
* [Mediocre chess - Transposition tables (Accessed: 05.03.2024)](https://mediocrechess.sourceforge.net/guides/transpositiontables.html)
* [Chess programming wiki (Accessed: 05.03.2024)](https://www.chessprogramming.org/Main_Page)