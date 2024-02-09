import numpy

import ChessBot.BoardModel.chessBoard
from ChessBot.MoveGeneration import bestMoveGeneration
from ChessBot.MoveGeneration.bestMoveGeneration import evaluate_position
from ChessBot.TranspositionTable.ZobristKey.ZobristRandomValues import ZobristRandomValues

state = ChessBot.BoardModel.chessBoard.BoardState()
ZOBRIST_RANDOM_VALUES = ZobristRandomValues()
state.create_initial_board(ZOBRIST_RANDOM_VALUES)

for i in range(40):
    move = bestMoveGeneration.calculate_best_move(3, state, ZOBRIST_RANDOM_VALUES)
    state.execute_move(move, ZOBRIST_RANDOM_VALUES)
    for row in state.board:
        print(row)
    print("")
    if (i % 10 == 0):
        j = 0
        for entry in ChessBot.MoveGeneration.bestMoveGeneration.TRANSPOSITION_TABLE:
            if entry is not None:
                j += 1
        print(j)

# talk()
