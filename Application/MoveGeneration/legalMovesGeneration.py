from Application.MoveGeneration.moveChecks import *

def get_legal_moves(state):
    """
    Calculates the legal moves for the given BoardState
    :param state: The BoardState
    """
    advances, captures = [], []
    king_row, king_col = find_king(state)
    if state.color == COLOR_WHITE:
        for row in range(8):
            for col in range(8):
                match state.board[row][col]:
                    case "P":
                        possible_advances, possible_captures = pawn_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "R":
                        possible_advances, possible_captures = rook_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "N":
                        possible_advances, possible_captures = knight_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "B":
                        possible_advances, possible_captures = bishop_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "K":
                        possible_advances, possible_captures = king_moves(state, row, col)
                        advances += possible_advances
                        captures += possible_captures
                    case "Q":
                        possible_advances, possible_captures = queen_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
    else:
        for row in range(8):
            for col in range(8):
                match state.board[row][col]:
                    case "p":
                        possible_advances, possible_captures = pawn_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "r":
                        possible_advances, possible_captures = rook_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "n":
                        possible_advances, possible_captures = knight_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "b":
                        possible_advances, possible_captures = bishop_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures
                    case "k":
                        possible_advances, possible_captures = king_moves(state, row, col)
                        advances += possible_advances
                        captures += possible_captures
                    case "q":
                        possible_advances, possible_captures = queen_moves(state, row, col, king_row, king_col)
                        advances += possible_advances
                        captures += possible_captures

    advances += get_castling_moves(state)
    return captures, advances

def get_castling_moves(state):
    """
    Calculates the castling moves that are legal for the BoardState
    """
    possible_moves = []

    # Checking if color can still castle and if there are no pieces between the king and rook
    # and if there is no check in between
    if state.castle_rights.white_castle_long:
        if state.color == COLOR_WHITE:
            possible = True
            for u in range(1, 4):
                if check_if_king_is_in_check(state, 7, 4 - u) or not check_if_square_is_empty(state, 7, 4 - u):
                    possible = False
            if possible:
                possible_moves.append("e1b1")
    if state.castle_rights.white_castle_short:
        if state.color == COLOR_WHITE:
            possible = True
            for u in range(1, 3):
                if check_if_king_is_in_check(state, 7, 4 + u) or not check_if_square_is_empty(state, 7, 4 + u):
                    possible = False
            if possible:
                possible_moves.append("e1g1")
    if state.castle_rights.black_castle_long:
        if state.color == COLOR_BLACK:
            possible = True
            for u in range(1, 4):
                if check_if_king_is_in_check(state, 0, 4 - u) or not check_if_square_is_empty(state, 0, 4 - u):
                    possible = False
            if possible:
                possible_moves.append("e8b8")
    if state.castle_rights.black_castle_short:
        if state.color == COLOR_BLACK:
            possible = True
            for u in range(1, 3):
                if check_if_king_is_in_check(state, 0, 4 + u) or not check_if_square_is_empty(state, 0,
                                                                                              4 + u):
                    possible = False
            if possible:
                possible_moves.append("e8g8")

    return possible_moves

def pawn_moves(state, row, col, king_row, king_col):
    """
    Generates all possible Pawn moves for the given BoardState and a given Pawn
    :param state: The BoardState
    :param row: The row of the Pawn
    :param col: The column of the Pawn
    :param king_row: The row of the king
    :param king_col: The column of the king
    """
    possible_advances = []
    possible_captures = []
    if state.color == COLOR_WHITE:
        # normal advance
        move = convert_move_to_long_alg_notation(row, col, row - 1, col)
        if check_if_square_is_empty(state, row - 1, col) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
            # move from baseline
            move = convert_move_to_long_alg_notation(row, col, row - 2, col)
            if row == 6 and check_if_square_is_empty(state, row - 2, col) and not_check_after_move(state, move, king_row,  king_col):
                possible_advances.append(move)
        # capture piece
        for u in [-1, 1]:
            move = convert_move_to_long_alg_notation(row, col, row - 1, col + u)
            if check_if_square_is_capturable(state, row - 1, col + u) and not_check_after_move(state, move, king_row, king_col):
                possible_captures.append(move)
            # EnPassant
            if ord(state.en_passant[0]) - 97 == col + u and row == 3 and not_check_after_move(state, move, king_row, king_col):
                possible_captures.append(move)
    else:
        # normal advance
        move = convert_move_to_long_alg_notation(row, col, row + 1, col)
        if check_if_square_is_empty(state, row + 1, col) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
            # move from baseline
            move = convert_move_to_long_alg_notation(row, col, row + 2, col)
            if row == 1 and check_if_square_is_empty(state, row + 2, col) and not_check_after_move(state, move, king_row, king_col):
                possible_advances.append(move)
        # capture piece
        for u in [-1, 1]:
            move = convert_move_to_long_alg_notation(row, col, row + 1, col + u)
            if check_if_square_is_capturable(state, row + 1, col + u) and not_check_after_move(state, move, king_row, king_col):
                possible_captures.append(move)
            # EnPassant
            if ord(state.en_passant[0]) - 97 == col + u and row == 4 and not_check_after_move(state, move, king_row, king_col):
                possible_captures.append(convert_move_to_long_alg_notation(row, col, row + 1, col + u))
    return possible_advances, possible_captures


def rook_moves(state, row, col, king_row, king_col):
    """
    Generates all possible Rook moves for the given BoardState and a given Rook
    :param state: The BoardState
    :param row: The row of the Rook
    :param col: The column of the Rook
    :param king_row: The row of the king
    :param king_col: The column of the king
    """
    possible_advances = []
    possible_captures = []
    # x-axis to the right
    for u in range(1, 8 - col):
        move = convert_move_to_long_alg_notation(row, col, row, col + u)
        if check_if_square_is_empty(state, row, col + u) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row, col + u) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    # x-axis to the left
    for u in range(1, col + 1):
        move = convert_move_to_long_alg_notation(row, col, row, col - u)
        if check_if_square_is_empty(state, row, col - u) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row, col - u) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    # y-axis to the bottom
    for v in range(1, 8 - row):
        move = convert_move_to_long_alg_notation(row, col, row + v, col)
        if check_if_square_is_empty(state, row + v, col) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row + v, col) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    # y-axis to the top
    for v in range(1, row + 1):
        move = convert_move_to_long_alg_notation(row, col, row - v, col)
        if check_if_square_is_empty(state, row - v, col) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row - v, col) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    return possible_advances, possible_captures

def knight_moves(state, row, col, king_row, king_col):
    """
    Generates all possible Knight moves for the given BoardState and a given Knight
    :param state: The BoardState
    :param row: The row of the Knight
    :param col: The column of the Knight
    :param king_row: The row of the king
    :param king_col: The column of the king
    """
    possible_advances = []
    possible_captures = []
    u1, u2, v1, v2 = 2, -2, 1, -1
    # horizontal two squares
    a, b = _knight_move(state, row, col, king_row, king_col, u1, u2, v1, v2)
    possible_advances += a
    possible_captures += b
    a, b = _knight_move(state, row, col, king_row, king_col, v1, v2, u1, u2)
    possible_advances += a
    possible_captures += b
    # horizontal one square
    return possible_advances, possible_captures


def _knight_move(state, row, col, king_row, king_col, u1, u2, v1, v2):
    """
    A helper method to calculate the possible squares a knight can jump to. u1, u2, v1, v2 are the different
    combinations of the squares the knight can jump to.
    :param state: The BoardState
    :param row: The row of the Knight
    :param col: The column of the Knight
    :param king_row: The row of the king
    :param king_col: The column of the king
    :param u1: value1
    :param u2: value2
    :param v1: value3
    :param v2: value4
    :return:
    """
    possible_advances, possible_captures = [], []
    for u in [u1, u2]:
        if 0 <= (row + u) <= 7:
            for v in [v1, v2]:
                if 0 <= (col + v) <= 7:
                    move = convert_move_to_long_alg_notation(row, col, row + u, col + v)
                    if check_if_square_is_empty(state, row + u, col + v) and not_check_after_move(state, move, king_row, king_col):
                        possible_advances.append(convert_move_to_long_alg_notation(row, col, row + u, col + v))
                    elif check_if_square_is_capturable(state, row + u, col + v) and not_check_after_move(state, move, king_row, king_col):
                        possible_captures.append(convert_move_to_long_alg_notation(row, col, row + u, col + v))
    return possible_advances, possible_captures


def bishop_moves(state, row, col, king_row, king_col):
    """
    Generates all possible Bishop moves for the given BoardState and a given Bishop
    :param state: The BoardState
    :param row: The row of the Bishop
    :param col: The column of the Bishop
    :param king_row: The row of the king
    :param king_col: The column of the king
    """
    possible_advances = []
    possible_captures = []
    # Bottom right
    for u in range(1, 8 - max(row, col)):
        move = convert_move_to_long_alg_notation(row, col, row + u, col + u)
        if check_if_square_is_empty(state, row + u, col + u) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row + u, col + u) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    # Top left
    for u in range(1, min(row, col) + 1):
        move = convert_move_to_long_alg_notation(row, col, row - u, col - u)
        if check_if_square_is_empty(state, row - u, col - u) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row - u, col - u) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    # Top right
    for v in range(1, min(row, 7 - col) + 1):
        move = convert_move_to_long_alg_notation(row, col, row - v, col + v)
        if check_if_square_is_empty(state, row - v, col + v) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row - v, col + v) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    # Bottom left
    for v in range(1, min(7 - row, col) + 1):
        move = convert_move_to_long_alg_notation(row, col, row + v, col - v)
        if check_if_square_is_empty(state, row + v, col - v) and not_check_after_move(state, move, king_row, king_col):
            possible_advances.append(move)
        elif check_if_square_is_capturable(state, row + v, col - v) and not_check_after_move(state, move, king_row, king_col):
            possible_captures.append(move)
            break
        else:
            break
    return possible_advances, possible_captures


def queen_moves(state, row, col, king_row, king_col):
    """
    Generates all possible Queen moves for the given BoardState and a given Queen
    :param state: The BoardState
    :param row: The row of the Queen
    :param col: The column of the Queen
    :param king_row: The row of the king
    :param king_col: The column of the king
    """
    possible_advances_rook, possible_captures_rook = rook_moves(state, row, col,king_row, king_col)
    possible_advances_bishop, possible_captures_bishop = bishop_moves(state, row, col, king_row, king_col)
    return possible_advances_rook + possible_advances_bishop, possible_captures_rook + possible_captures_bishop


def king_moves(state, row, col):
    """
    Generates all possible King moves for the given BoardState and a given King
    :param state: The BoardState
    :param row: The row of the King
    :param col: The column of the King
    """
    possible_advances = []
    possible_captures = []
    # All the possible squares around the king
    for u in [-1, 0, 1]:
        if 0 <= (row + u) <= 7:
            for v in [-1, 0, 1]:
                if 0 <= (col + v) <= 7:
                    move = convert_move_to_long_alg_notation(row, col, row + u, col + v)
                    if check_if_square_is_empty(state, row + u, col + v) and not_check_after_move(state, move, row + u, col + v):
                        possible_advances.append(move)
                    elif check_if_square_is_capturable(state, row + u, col + v) and not_check_after_move(state, move, row + u, col + v):
                        possible_captures.append(move)
    return possible_advances, possible_captures


def convert_move_to_long_alg_notation(old_row, old_col, new_row, new_col):
    """
    Converts a move to the long string notation which is used in the UCI interface.
    For example: A Pawnmove from a2 to a4 would be a2a4, a knight capture from b3 to d4 would be b3d4
    :param old_row: The old row of the move
    :param old_col: The old column of the move
    :param new_row: The new row of the move
    :param new_col: The new column of the move
    :return:
    """
    long_notation = ""
    long_notation += chr(old_col + 97)
    long_notation += str(8 - old_row)
    long_notation += chr(new_col + 97)
    long_notation += str(8 - new_row)
    return long_notation
