import random
import chessRules as chess


# This script will later execute the MiniMax algorithm to find the best move
# At this time it only choses a random move


def calculateMove(depth, board):
    all_moves = chess.get_legal_moves(board)
    best_move = random.choice(all_moves)

    return best_move