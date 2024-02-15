from BoardModel.chessBoard import BoardState
from MoveGeneration import bestMoveGeneration
from TranspositionTable.ZobristKey.ZobristRandomValues import ZobristRandomValues
from communication import talk

ZOBRIST_RANDOM_VALUES = ZobristRandomValues()
state = BoardState()
state.create_initial_board(ZOBRIST_RANDOM_VALUES)
#set_fen_to_board("4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1", state)



for i in range(15):
    move = bestMoveGeneration.calculate_best_move(3, state, ZOBRIST_RANDOM_VALUES)
    state.execute_move(move, ZOBRIST_RANDOM_VALUES)
    print(move)
    for row in state.board:
        print(row)
    print("")

#talk()
