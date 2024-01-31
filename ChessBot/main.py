from communication import talk
import legalMovesGeneration

import chessBoard

state = chessBoard.BoardState()
state.create_initial_board()
state.execute_move("e1d5")
state.execute_move("a2d7")

state.execute_move("a8a5")
state.execute_move("b 2b5")

state.execute_move("h8h5")
state.execute_move("h2g5")

#state.execute_move("a8a5")
#state.execute_move("a8a5")

print(legalMovesGeneration.calculate_pins(state))
for row in state.board:
    print(row)


#talk()
