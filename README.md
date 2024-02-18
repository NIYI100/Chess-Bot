# Chess-Bot

This is a chess engine which is based on the uci interface. With that it can be plugged in to many chess GUIs such as
Lichess or Arena.
This project implements the chess rules, the search for the best move as well as the communication in the uci standard

# Getting started
To use the engine you just have to download a uci-compatible GUI and plug the engine into it. The engine is compiled as
a [main.exe](dist/main.exe) file. When loaded in the GUI you can just start a game and play. An easy way is Arena.

Another way to play is via the command line. For that just start the application via your preferred IDE. This is
more complicated as you have to input the uci commands yourself.

Also there is a [requirements.txt](requirements.txt) file if you want to play with the code.

# Structure in detail
## Communication
The communication between engine and GUI happens in [communication.py](communication.py). This is a bare-boned version of
an uci interface which only some of the available features

## ChessBoard and Conversions
The Chessboard State is inside the [BoardModel](BoardModel) directory. The Board saves everything that also is available
in the [FEN String]() (A String representation of a Chess Board used in chess engines) as well a `zobristKey` and a history
which is used for undoing moves in the calculation of the best move.

The [Board Conversion](BoardModel/boardConversion.py) is used for conversions from the `boardState` object to a FEN String
and the other way around. One is used in the GUI the other one in the engine.

## Constants
In Chess there are a lot of Strings and flags used for different things. This ranges from the representation of a piece
`WHITE_KING = "K"` to different flags used for efficient move calculation.
These constants are in the [Constants](Constants) directory.

## Move Generation
The [Move Generation directory](MoveGeneration) is used for everything regarding move generations.

In [legalMovesGeneration](MoveGeneration/legalMovesGeneration.py) all legal moves are calculated. In addition to that
it is also checked if the king is in check and if castling is possible in the situation. In that cases the legal moves
will be adapted.

The calculated legal moves are used in the [bestMoveGeneration](MoveGeneration/bestMoveGeneration.py) to calculate the
best possible move. For that the `negaMax` algorithm (a modification of the `miniMax` algorithm). Here the transposition
table is used to cut the caluclation of nodes that were already calculated. In addition to that Alpha-Beta pruning is
also used.

## Transposition Table
The [Transposition Table](TranspositionTable) directory contains the code for the Transposition table. A Transposition
table is a table / array which contains entries for different board positions. This is usefull as the same position can
be achieved through different moves (`a1a3, a8a6, b1b3` ends in the same position as `b1b3, a8a6, a1a3`. So it is enough
if we calculate one of these positions). This can be used to drastically reduce the amount of search nodes.

The [HashEntry](TranspositionTable/HashEntry.py) class is used for the entries in the transposition table.

To calculate what Board is corresponding to what transposition table entry a hash function is used. In this project we
use the [Zobrist hashing](). In Zobrist hashing we use 64bit numbers that are XORed to create a pseudorandom number
for the state of the board. For that we need different arrays containing random 64bit numbers. These are created in
[ZobristRandomValues](TranspositionTable/ZobristKey/ZobristRandomValues.py). This is only done once and the numbers will be used
throughout the whole game.

The [ZobristKeyCalculations](TranspositionTable/ZobristKey/ZobristKeyCalculations.py) is used to calculate the ZobristKey
or how the ZobristKey changes after a certain move.