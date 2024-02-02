import math
import time

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
    timer = time.time()
    for move in chess.get_legal_moves(state):
        state.push(move)
        board_evaluation = - nega_max(depth, state, - math.inf, math.inf)
        state.pop()
        if board_evaluation > best_eval:
            best_eval = board_evaluation
            best_move = move
    state.color = color
    state.switch_color()
    print(time.time() - timer)
    return best_move


def nega_max(depth, state, alpha, beta):
    if depth == 0:
        return evaluate_position(state)

    for move in chess.get_legal_moves(state):
        state.push(move)
        board_evaluation = - nega_max(depth - 1, state, -beta, -alpha)
        state.pop()
        if board_evaluation >= beta:
            return beta
        if board_evaluation > alpha:
            alpha = board_evaluation

    return alpha


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
