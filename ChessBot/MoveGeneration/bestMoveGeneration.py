import math
import ChessBot.MoveGeneration.legalMovesGeneration as chess
from ChessBot.Constants.pieceConstants import *
from ChessBot.Constants import evaluation_tables


# This script will later execute the MiniMax algorithm to find the best move
# At this time it only choses a random move

# Do MiniMax / NegaMax with optimizations
# Check if trough move, the enemy King is in check -> bool = true
def calculate_best_move(depth, state):
    color = state.color
    best_eval = - math.inf
    best_move = None
    for move in chess.get_legal_moves(state):
        state.push(move)
        board_evaluation = - nega_max(depth, state)
        state.pop()
        if board_evaluation > best_eval:
            best_eval = board_evaluation
            best_move = move
    state.color = color
    state.switch_color()
    return best_move


def nega_max(depth, state):
    if depth == 0:
        return evaluate_position(state)


    max_eval = - math.inf
    for move in chess.get_legal_moves(state):
        state.push(move)
        board_evaluation = - nega_max(depth - 1, state)
        state.pop()
        max_eval = max(board_evaluation, max_eval)

    return max_eval


def evaluate_position(state):
    score = 0
    for x in range(8):
        for y in range(8):
            piece = state.board[x][y]
            if state.color == COLOR_WHITE and piece.isupper():
                score += evaluation_tables.piece_values[piece]
                evaluation_table = evaluation_tables.evaluation_for_piece[piece]
                score += evaluation_table[x][y]
            if state.color == COLOR_BLACK and piece.islower():
                score -= evaluation_tables.piece_values[piece]
                evaluation_table = evaluation_tables.evaluation_for_piece[piece]
                score -= evaluation_table[x][y]
    return score
