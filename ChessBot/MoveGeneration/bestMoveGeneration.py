# This class is used to calculate the best move for a given board

import math
import time

import ChessBot.MoveGeneration.legalMovesGeneration as chess
from ChessBot.Constants import evaluation_tables
from ChessBot.Constants.HashEntryFlags import *
from ChessBot.TranspositionTable.HashEntry import HashEntry

TRANSPOSITION_TABLE = [None] * 1048583

# Calculation of the best move for a given starting position using negaMax (a compromized MiniMax Algorithm)
def calculate_best_move(depth, state, zobrist_values):
    color = state.color
    best_eval = - math.inf
    best_move = None
    #timer = time.time()

    for move in chess.get_legal_moves(state):
        state.push(move, zobrist_values)
        board_evaluation = - nega_max(depth, state, - math.inf, math.inf, zobrist_values)
        state.pop(zobrist_values)
        if board_evaluation > best_eval:
            best_eval = board_evaluation
            best_move = move
    state.color = color
    state.switch_color(zobrist_values)
    #print(time.time() - timer)
    #print(best_eval, " for color: ", color)
    return best_move

# The NegaMax Algorithm - it uses Alpha-Bet Pruning, rudimentary move ordering and a transposition table as optimization methods
# Checks if an entry in the transpos_table exists or if the depth is 0 and returns the evaluation. If not
# the moves of one depth higher will be checked (if there are no alpha or beta cutoffs)
# New evaluations will be put into the transposition table
def nega_max(depth, state, alpha, beta, zobrist_values):
    if _check_transpos_table(state, depth, alpha, beta):
        return _get_eval_of_transpos_table(state)

    if depth == 0:
        evaluation = evaluate_position(state)
        _create_entry_in_transpos_table(state, depth, HASH_EXACT, evaluation)
        return evaluation

    original_alpha = alpha
    for move in chess.get_legal_moves(state):
        state.push(move, zobrist_values)
        board_evaluation = - nega_max(depth - 1, state, -beta, -alpha, zobrist_values)
        state.pop(zobrist_values)
        if board_evaluation >= beta:
            _create_entry_in_transpos_table(state, depth, HASH_BETA, beta)
            return beta
        if board_evaluation > alpha:
            alpha = board_evaluation

    if alpha > original_alpha:
        _create_entry_in_transpos_table(state, depth, HASH_EXACT, alpha)
    else:
        _create_entry_in_transpos_table(state, depth, HASH_ALPHA, alpha)

    return alpha


# Evaluates a given position according to the ChessBot/Constants/evaluation_tables.py. A positiv value menas that white is ahead
# a negativ means black is ahead
def evaluate_position(state):
    score = 0
    for x in range(8):
        for y in range(8):
            piece = state.board[x][y]
            if piece.isupper():
                score += evaluation_tables.piece_values[piece]
                evaluation_table = evaluation_tables.evaluation_for_piece[piece]
                score += evaluation_table[x][y]
            if piece.islower():
                score -= evaluation_tables.piece_values[piece]
                evaluation_table = evaluation_tables.evaluation_for_piece[piece]
                score -= evaluation_table[7 - x][7 - y]
    return score

# Creates an entry in the transpostion table
def _create_entry_in_transpos_table(state, depth, flag, evaluation):
    entry = HashEntry(state.zobristKey, depth, flag, evaluation, 0)
    # TODO ancient
    # The ancient var will be used to replace entries later on - In the moment there is no way of replacement if there
    # are hash hits for different positions
    TRANSPOSITION_TABLE[state.zobristKey % len(TRANSPOSITION_TABLE)] = entry

# Checks if a transposition entry is valid and should be used or if the algorithm can not use the entry
# for example if the searched depth of the saved position is 1 but we have to search to a depth of 3
def _check_transpos_table(state, depth, alpha, beta):
    hash_entry = TRANSPOSITION_TABLE[state.zobristKey % len(TRANSPOSITION_TABLE)]
    if hash_entry is not None:
        if hash_entry.depth >= depth:
            if hash_entry.flag == HASH_EXACT:
                return True
            if hash_entry.flag == HASH_BETA and hash_entry.evaluation >= beta:
                return True
            if hash_entry.flag == HASH_ALPHA and hash_entry.evaluation > alpha:
                return True
        return False

# returns the saved evaluation of a position
def _get_eval_of_transpos_table(state):
    return TRANSPOSITION_TABLE[state.zobristKey % len(TRANSPOSITION_TABLE)].evaluation
