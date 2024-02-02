import ChessBot.BoardModel.chessBoard
from ChessBot.MoveGeneration import bestMoveGeneration
from ChessBot.MoveGeneration.bestMoveGeneration import evaluate_position

state = ChessBot.BoardModel.chessBoard.BoardState()
state.create_initial_board()

for i in range(15):
    move = bestMoveGeneration.calculate_best_move(3, state)
    state.execute_move(move)
    for row in state.board:
        print(row)
    print("")


# talk()
