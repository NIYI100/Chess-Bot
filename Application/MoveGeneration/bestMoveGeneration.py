import time

import Application.MoveGeneration.legalMovesGeneration as chess
from Application.BoardModel.chessBoard import BoardState
from Application.Constants import evaluation_tables
from Application.Constants.pieceConstants import COLOR_WHITE
from Application.MoveGeneration.moveChecks import find_king, check_if_king_is_in_check, not_check_after_move
from Application.TranspositionTable.TranspostionTable import *


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

    while depth <= max_depth and time.time() <= startTime + time_to_run:
        best_move = calculate_best_move(depth, state)
        depth += 1
    return best_move


def calculate_best_move(depth, state):
    """
    Calculates the best move for a given BoardState and depth. For every move the move will be pushed
    and the negaMax algorithm will be used to find the best move.
    If there is no best move, because there is a stalemate or checkmate "0000" will be returned
    :param depth: The depth to search the BoardState to
    :param state: The BoardState to be searched
    """
    best_evaluation = - math.inf
    captures, advances = chess.get_legal_moves(state)
    best_move = None
    sorted_moves = sort_for_transpos_table(state, captures) + sort_for_transpos_table(state, advances)

    for move in sorted_moves:
        state.push(move)
        board_evaluation = - nega_max(depth, state, - math.inf, math.inf)
        state.pop()

        if board_evaluation >= best_evaluation:
            best_evaluation = board_evaluation
            best_move = move
    if best_move is None:
        best_move = "0000"
    return best_move


def nega_max(depth, state, alpha, beta):
    """
    The negaMax algorithm is used to recursively find the best move for a give BopardState. For already looked
    at states a transposition table is used to speed up the search. For depth 0 a quiescence search is performed
    to counter the horizon effect. Furthermore, Late Move Reduction (LMR) is used for later moves for further speed up.

    :param depth: The depth to which the algorithm should search
    :param state: The momentary BoardState
    :param alpha: The alpha value
    :param beta: The beta value
    :return
    """
    # Is there already an entry in the transposition table for the postion?
    if check_transpos_table_if_useable(state, depth, alpha, beta):
        return get_eval_of_transpos_table(state)

    # Evaluate board because we are at leaf node
    if depth == 0:
        evaluation, searched_depth = quiescenceSearch(state, alpha, beta, 5)
        create_entry_in_transpos_table_if_better(state, depth, HASH_EXACT, evaluation)
        return evaluation

    orginal_alpha = alpha
    captures, advances = chess.get_legal_moves(state)
    sorted_moves = sort_for_transpos_table(state, captures) + sort_for_transpos_table(state, advances)

    # Checkmate or stalemate
    if len(sorted_moves) == 0:
        king_row, king_col = find_king(state)
        # Checkmate because active player is in check and has no moves left
        if check_if_king_is_in_check(state, king_row, king_col):
            return - math.inf
        # Stalemate
        else:
            return 0

    for num_moves_looked_at, next_move in enumerate(sorted_moves):
        state.push(next_move)

        # LMR
        if num_moves_looked_at >= 7 and depth >= 3:
            reduced_depth = depth - 2
            board_evaluation = - nega_max(reduced_depth, state, -beta, -alpha)
            # Found checkmate
            if board_evaluation == math.inf or board_evaluation == - math.inf:
                state.pop()
                return board_evaluation
            # The move is better than expected, so we do the full search
            if board_evaluation > alpha:
                board_evaluation = - nega_max(depth - 1, state, -beta, -alpha)

        # First moves should be searched in greater depth
        else:
            board_evaluation = - nega_max(depth - 1, state, -beta, -alpha)
        state.pop()

        # Found checkmate
        if board_evaluation == math.inf or board_evaluation == - math.inf:
            return board_evaluation

        # Beta cutoff - minimizing player will not make this move
        if board_evaluation >= beta:
            create_entry_in_transpos_table_if_better(state, depth, HASH_BETA, beta)
            return beta

        # maximizing players best move at the moment
        if board_evaluation > alpha:
            alpha = board_evaluation

    if alpha > orginal_alpha:
        create_entry_in_transpos_table_if_better(state, depth, HASH_EXACT, alpha)
    else:
        create_entry_in_transpos_table_if_better(state, depth, HASH_ALPHA, alpha)

    return alpha


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
        return beta, 5 - depth
    # We searched to maximum depth
    elif depth == 0:
        return stand_pat, 5 - depth
    if alpha < stand_pat:
        alpha = stand_pat

    captures, advances = chess.get_legal_moves(state)
    sorted_moves = sort_for_transpos_table(state, captures)
    king_row, king_col = find_king(state)

    # We are in check - Only moves allowed that get the king out of check
    if check_if_king_is_in_check(state, king_row, king_col):
        still_possible_moves = []
        for move in sorted_moves:
            if not_check_after_move(state, move, king_row, king_col):
                still_possible_moves.append(move)
        # There are no legal moves to recapture
        if len(still_possible_moves) == 0:
            # There are also no possible advances that prevent checkmate - The state is checkmate
            if len(advances) == 0:
                return - math.inf, 5 - depth
            # There are advances but we dont search it here
            else:
                return stand_pat, 5 - depth
        else:
            sorted_moves = still_possible_moves

    for move in sorted_moves:
        state.push(move)
        evaluation, searched_depth = quiescenceSearch(state, - beta, - alpha, depth - 1)
        evaluation = - evaluation
        state.pop()

        if evaluation >= beta:
            create_entry_in_transpos_table_if_better(state, depth, HASH_BETA, evaluation)
            return beta, 5 - searched_depth
        if evaluation > alpha:
            alpha = evaluation

    create_entry_in_transpos_table_if_better(state, depth, HASH_EXACT, alpha)
    return alpha, 5 - depth


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

    check_bonus = 0
    state.switch_color()
    king_row, king_col = find_king(state)
    if check_if_king_is_in_check(state, king_row, king_col):
        check_bonus = 45
    state.switch_color()

    if state.color == COLOR_WHITE:
        return white_eval - black_eval + check_bonus
    else:
        return black_eval - white_eval + check_bonus
