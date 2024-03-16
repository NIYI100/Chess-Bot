import random
import time

import Application.MoveGeneration.legalMovesGeneration as chess
from Application.BoardModel.chessBoard import BoardState
from Application.Constants import evaluation_tables
from Application.Constants.pieceConstants import COLOR_WHITE, COLOR_BLACK
from Application.MoveGeneration.moveChecks import find_king, check_if_king_is_in_check, not_check_after_move
from Application.TranspositionTable.TranspostionTable import *

hash_hits = 0
nodes = 0
def iterative_deepening(max_depth, state, time_to_run):
    """
    This is the entry point to the calculation of the best move. Iterative deepening iteratively deepens the search
    until the maximum depth is reached or the time runs out.
    :param max_depth: The maximal depth to which the BoardState should be searched
    :param state: The BoardState to be searched
    :param time_to_run: The maximum time allocated for the search
    :return:
    """
    startTime = time.time()
    depth = 1
    best_move = ""


    print(f"{state.color} to move")
    print(f"evaluation at the moment: {evaluate_position(state)}")
    while depth <= max_depth and time.time() <= startTime + time_to_run:
        is_max_depth = depth == max_depth
        best_move, best_eval = calculate_best_move(depth, state, is_max_depth)
        print(f"best move: {best_move} for depth: {depth} with evaluation: {best_eval}")
        depth += 1
    global hash_hits, nodes
    print(f"Nodes: {nodes}, Hashhits: {hash_hits}")
    hash_hits = 0
    nodes = 0
    return best_move


def calculate_best_move(depth, state, is_max_depth):
    """
    Calculates the best move for a given BoardState and depth. For every move the move will be pushed
    and the negaMax algorithm will be used to find the best move.
    If there is no best move, because there is a stalemate or checkmate "0000" will be returned
    :param depth: The depth to search the BoardState to
    :param state: The BoardState to be searched
    """
    best_evaluation = - math.inf
    best_move = "0000"
    captures, advances = chess.get_legal_moves(state)
    sorted_moves = sort_for_transpos_table(state, captures + advances)

    for move in sorted_moves:
        state.push(move)
        board_evaluation = - nega_max(depth - 1, state, - math.inf, math.inf, is_max_depth)
        state.pop()

        if board_evaluation >= best_evaluation:
            best_evaluation = board_evaluation
            best_move = move

    return best_move, best_evaluation


def nega_max(depth, state, alpha, beta, is_max_depth):
    """
    The negaMax algorithm is used to recursively find the best move for a give BopardState. For already looked
    at states a transposition table is used to speed up the search. For depth 0 a quiescence search is performed
    to counter the horizon effect. Furthermore, Late Move Reduction (LMR) is used for later moves for further speed up.

    :param depth: The depth to which the algorithm should search
    :param state: The momentary BoardState
    :param alpha: The alpha value
    :param beta: The beta value
    """
    orginal_alpha = alpha
    captures, advances = chess.get_legal_moves(state)
    sorted_moves = sort_for_transpos_table(state, captures) + sort_for_transpos_table(state, advances)
    global hash_hits
    global nodes
    nodes += 1
    # Checkmate or stalemate
    if len(sorted_moves) == 0:
        king_row, king_col = find_king(state)
        # Checkmate because active player is in check and has no moves left
        if check_if_king_is_in_check(state, king_row, king_col):
            return - math.inf
        # Stalemate
        else:
            return 0


    # Is there already an entry in the transposition table for the postion?
    #"""
    entry = TranspositionTable().get_entry(state.zobristKey)
    if entry is not None and entry.depth >= depth:
        hash_evaluation = get_eval_of_transpos_table(state)
        if entry.color != state.color:
            hash_evaluation = - hash_evaluation
        hash_hits += 1
        if entry.flag == HASH_EXACT:
            return hash_evaluation
        elif entry.flag == HASH_ALPHA:
            alpha = max(alpha, hash_evaluation)
        elif entry.flag == HASH_BETA:
            beta = min(beta, hash_evaluation)

        if alpha >= beta:
            return hash_evaluation
#"""
    # if check_transpos_table_if_useable(state, depth, alpha, beta):
    #    return get_eval_of_transpos_table(state)

    # Evaluate board because we are at leaf node
    if depth == 0:
        direct_eval = evaluate_position(state)
        #if is_max_depth:
        #    eval_lookahead = quiescenceSearch(state, alpha, beta, 3)
        #    if state.color == COLOR_WHITE:
        #        evaluation = min(direct_eval, eval_lookahead)
        #    else:
        #        evaluation = max(direct_eval, eval_lookahead)
        #else:
        evaluation = direct_eval
        return evaluation * (1 if state.color == COLOR_WHITE else - 1)

    board_evaluation = - math.inf
    for num_moves_looked_at, next_move in enumerate(sorted_moves):
        state.push(next_move)

        # Late Move Reduction (LMR)
        #if num_moves_looked_at >= 7 and depth >= 3:
        #    reduced_depth = depth - 2
        #    board_evaluation = - nega_max(reduced_depth, state, -beta, -alpha)
        #    # Found checkmate
        #    if board_evaluation == math.inf or board_evaluation == - math.inf:
        #        state.pop()
        #        return board_evaluation
        #    # The move is better than expected, so we do the full search
        #    if board_evaluation > alpha:
        #        board_evaluation = - nega_max(depth - 1, state, -beta, -alpha)

        # First moves should be searched in greater depth
        #else:
        board_evaluation = - nega_max(depth - 1, state, -beta, -alpha, is_max_depth)
        state.pop()

        if board_evaluation >= beta:
            return beta

        alpha = max(alpha, board_evaluation)
        if alpha >= beta:
            break

    entry_evaluation = board_evaluation
    if board_evaluation <= orginal_alpha:
        entry_flag = HASH_BETA
    elif board_evaluation >= beta:
        entry_flag = HASH_ALPHA
    else:
        entry_flag = HASH_EXACT
    entry_depth = depth
    hash_color = state.color
    hash_entry = HashEntry(state.zobristKey, entry_depth, entry_flag, entry_evaluation, hash_color)
    index = TranspositionTable().get_index(state.zobristKey)
    table = TranspositionTable().get_transposition_table()
    table[index] = hash_entry

    return alpha


def evaluation_after_counter_capture(state):
    best_evaluation = 0
    captures, _ = chess.get_legal_moves(state)
    for move in captures:
        state.push(move)
        evaluation = evaluate_position(state)
        state.pop()
        if evaluation > best_evaluation:
            best_evaluation = evaluation
    return best_evaluation


def quiescenceSearch(state, alpha, beta, depth):
    """
    quiescenceSearch is used at the leaf nodes to counter the horizon effect.
    :param state: The BoardState
    :param alpha: The alpha value
    :param beta: The beta value
    :param depth: The depth to which shoould be searched
    """

    stand_pat = evaluate_position(state)
    # Move is worse than before
    if stand_pat >= beta:
        return beta
    # We searched to maximum depth
    elif depth == 0:
        return stand_pat
    if alpha < stand_pat:
        alpha = stand_pat

    captures, advances = chess.get_legal_moves(state)
    king_row, king_col = find_king(state)

    # We are in check - Only moves allowed that get the king out of check
    if check_if_king_is_in_check(state, king_row, king_col):
        still_possible_moves = []
        for move in captures:
            if not_check_after_move(state, move, king_row, king_col):
                still_possible_moves.append(move)
        # There are no legal moves to recapture
        if len(still_possible_moves) == 0:
            # There are also no possible advances that prevent checkmate - The state is checkmate
            if len(advances) == 0:
                return - math.inf
            # There are advances but we dont search it here
            else:
                return stand_pat
        else:
            captures = still_possible_moves

    sorted_captures = sort_for_transpos_table(state, captures)
    for move in sorted_captures:
        state.push(move)
        evaluation = - quiescenceSearch(state, - beta, - alpha, depth - 1)
        state.pop()

        if evaluation >= beta:
            return beta
        if evaluation > alpha:
            alpha = evaluation

    return alpha


def evaluate_position(state: BoardState):
    """
    Evaluates the state of the board. At the moment this only includes the position of the pieces + a bonus
    if the enemy king is in check.
    The evaluation is dependent on the active color. A position in which white is ahead by 600 will be returned
    as 600 if white is active at the moment and - 600 if black is active.
    :param state: The BoardState
    """
    white_eval, black_eval = 0, 0
    for row in range(8):
        for col in range(8):
            piece = state.board[row][col]
            if piece.isupper():
                white_eval += evaluation_tables.piece_values[piece]
                evaluation_table = evaluation_tables.evaluation_for_piece[piece]
                white_eval += evaluation_table[row][col]
            if piece.islower():
                black_eval += evaluation_tables.piece_values[piece]
                evaluation_table = evaluation_tables.evaluation_for_piece[piece]
                black_eval += evaluation_table[7 - row][7 - col]

    # check_bonus = 0
    # state.switch_color()
    # king_row, king_col = find_king(state)
    # if check_if_king_is_in_check(state, king_row, king_col):
    #    check_bonus = 45
    # state.switch_color()

    return white_eval - black_eval  # + check_bonus