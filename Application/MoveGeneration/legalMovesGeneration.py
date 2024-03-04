# This class is used to calculalte all legal moves that are possible on a given board
from Application.BoardModel.chessBoard import BoardState
from Application.MoveGeneration.moveChecks import *


# Calculate all the legal possible moves
# For move ordering purposes the captures are put in the front
#############################################################
# In the moment there are no checks if the king is in check or if a piece is pinned. If that is the case and the king can
# be taken a big penalty is given so the engine will not do this - Note: Due to the horizon effect this does not work every time
# but for the moment it is okay
def get_legal_moves(state: BoardState):
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

def pawn_moves(state: BoardState, row: int, col: int, king_row: int, king_col: int) -> (list[str], list[str]):
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


def rook_moves(state: BoardState, row: int, col: int, king_row: int, king_col: int) -> (list[str], list[str]):
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

def knight_moves(state: BoardState, row: int, col: int, king_row: int, king_col: int) -> (list[str], list[str]):
    possible_advances = []
    possible_captures = []
    u1, u2, v1, v2 = 2, -2, 1, -1
    # horizontal two squares
    knight_move(possible_advances, possible_captures, state, row, col, king_row, king_col, u1, u2, v1, v2)
    knight_move(possible_advances, possible_captures, state, row, col, king_row, king_col, v1, v2, u1, u2)
    # horizontal one square
    return possible_advances, possible_captures


def knight_move(possible_advances: list[str], possible_captures: list[str], state: BoardState, row: int, col: int, king_row: int, king_col: int, u1: int, u2: int, v1: int, v2: int) -> (list[str], list[str]):
    for u in [u1, u2]:
        if 0 <= (row + u) <= 7:
            for v in [v1, v2]:
                if 0 <= (col + v) <= 7:
                    move = convert_move_to_long_alg_notation(row, col, row + u, col + v)
                    if check_if_square_is_empty(state, row + u, col + v) and not_check_after_move(state, move, king_row, king_col):
                        possible_advances.append(convert_move_to_long_alg_notation(row, col, row + u, col + v))
                    elif check_if_square_is_capturable(state, row + u, col + v) and not_check_after_move(state, move, king_row, king_col):
                        possible_captures.append(convert_move_to_long_alg_notation(row, col, row + u, col + v))


def bishop_moves(state: BoardState, row: int, col: int, king_row: int, king_col: int) -> (list[str], list[str]):
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


def queen_moves(state: BoardState, row: int, col: int, king_row: int, king_col: int) -> (list[str], list[str]):
    possible_advances_rook, possible_captures_rook = rook_moves(state, row, col,king_row, king_col)
    possible_advances_bishop, possible_captures_bishop = bishop_moves(state, row, col, king_row, king_col)
    return possible_advances_rook + possible_advances_bishop, possible_captures_rook + possible_captures_bishop


def king_moves(state: BoardState, row: int, col: int) -> (list[str], list[str]):
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


# Converts the array indexes to the long notation used in UCI
# a2a4 for the pawn at a2 that moves 2 squares to the front on its first move
def convert_move_to_long_alg_notation(old_row: int, old_col: int, new_row: int, new_col: int) -> str:
    long_notation = ""
    long_notation += chr(old_col + 97)
    long_notation += str(8 - old_row)
    long_notation += chr(new_col + 97)
    long_notation += str(8 - new_row)
    return long_notation
