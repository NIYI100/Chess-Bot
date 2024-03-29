# Project Specifications

* Name: Sven Ambrosius
* Programming language: Python
* Language of code / documentation: English
* Degree: Masters of computer science (exchange student)

In this project I´ll create a chess bot engine which can be used
with [Lichess](https://lichess.org/en) as a GUI to play games against.
Furthermore, there will be a interface following the [Universal Chess Interface (UCI)](https://de.wikipedia.org/wiki/Universal_Chess_Interface) standard
so it can be plugged into other chess GUIs too.

The inputs are via "drag & drop" with the help of the existing GUIs.
For testing purposes there might be a command-line version. After each player move, the algorithm
calculates its own move and executes it.


A big problem for chess engines is that for the most part of the game there are a lot of moves
which could be executed. Especially if the engine should do a look ahead the amount of possible
moves grow exponentially. This is not feasible. I´m going to create a chess engine which optimizes the
searched moves so that it can do a look ahead. For that I´ll focus on the evaluation of the positions
and an optimization with regard to the board calculations that have to be calculated each round. 

For that I will use the MiniMax algorithm because chess  is a two-player game with alternating goals.
Because of the high dimensionality that comes from the availability of a huge amount of
legal moves I will implement some optimizations:
* [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha–beta_pruning#)
  * alpha-beta pruning is a very common and efficient way to reduce the size of the searched tree. It is the standard for
  optimizing the runtime of a MiniMax algorithm.
* Move Ordering
  * Move Ordering can speed up the search a lot because with good ordering
  the best moves will be calculated first and the rest doesnt have to be calculated. For a good move order there has to be
  a heuristic to determine which moves could be good or not. Of course this isn´t right everytime, but it should
  be a help in the most cases.
* [Transposition tables](https://www.chessprogramming.org/Transposition_Table)
  * In chess the same board state can be achieved via different moves. In a transposition table the
  states are saved with the corresponding value after they got searched. This reduces the
  search tree a lot because those positions do not have to be searched again and a value
  can be assigned directly
  * The table will be a hash function which takes the board state as input.
* [Killer heuristic](https://en.wikipedia.org/wiki/Killer_heuristic)
  * The idea of the Killer Heuristic is that a very good move on one board might be a very good move on
  a similar board too.

The board itself will be coded as a [FEN String](https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation). 
This is a typical representation of the board.

The expected time complexity of the algorithm is O(b^n) where b is the amount of branches (legal moves) in the MiniMax algorithm
and n is the depth of the search. Even with alpha-beta pruning and the other optimizations in the O-notation it doesn't change.

The expected space is O(b * n) for the default algorithm. The use of a transposition table doesn't change that, if we use a table with
static size and implement replacement strategies.
But it is still important to optimize the size because it has to be in memory and would be too large for every possible board state.
If we use a transposition table per turn then we get extra size of O(b^n). If we even save some turns that happened earlier
then we arrive at O(m * b^n) where m is the amount of moves that will be saved.