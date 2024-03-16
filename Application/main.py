import time

from Application.BoardModel.boardConversion import set_fen_to_board
from Application.BoardModel.chessBoard import BoardState
from Application.MoveGeneration.bestMoveGeneration import iterative_deepening
from Application.communication import talk

state = BoardState()
state.create_initial_board()

#set_fen_to_board("3rkb1r/ppp3p1/5p1p/4P3/4p2B/8/PPN2P1P/R3K1R1 b Qk - 1 17", state)
#set_fen_to_board("R7/8/4Q3/P7/8/4K3/8/5k2 b - - 6 74", state)
#set_fen_to_board("R7/8/8/P7/8/8/4QK1k/8 w - - 17 80", state)
"""
for i in range(50):
    timer = time.time()
    move = iterative_deepening(3, state, 50)
    state.execute_move(move)
    for row in state.board:
        print(row)
    print(f"Time taken: {time.time() - timer:.2f} seconds")
    print("")
"""

talk()
