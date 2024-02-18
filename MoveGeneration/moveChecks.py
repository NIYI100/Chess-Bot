from Constants.pieceConstants import *

def get_castling_moves_if_possible(state):
    possible_moves = []
    possible = True
    if (state.color == COLOR_WHITE and state.castle_rights[0] != "-"):
        if state.castle_rights[0] == "Q":
            for u in range(1, 4):
                if check_if_king_is_in_check(state, 4 - u, 0):
                    possible = False
            if possible:
                possible_moves.append("e1b1")
        possible = True
        if state.castle_rights[0] == "K" or state.castle_rights[1] == "K":
            for u in range(1, 3):
                if check_if_king_is_in_check(state, 4 + u, 0):
                    possible = False
            if possible:
                possible_moves.append("e1g1")
    if (state.color == COLOR_BLACK and state.castle_rights[0] != "-"):
        if state.castle_rights[0] == "q" or state.castle_rights[1] == "q" or state.castle_rights[2] == "q":
            for u in range(1, 4):
                if check_if_king_is_in_check(state, 4 - u, 7):
                    possible = False
            if possible:
                possible_moves.append("e7b7")
        possible = True
        if state.castle_rights[0] == "k" or state.castle_rights[1] == "k" or state.castle_rights[2] == "k" or state.castle_rights[3] == "k":
            for u in range(1, 3):
                if check_if_king_is_in_check(state, 4 + u, 7):
                    possible = False
            if possible:
                possible_moves.append("e7g7")
    return possible_moves

def check_if_king_is_in_check(state, x, y):
    _, captures = [], []
    if check_knight_capture_of_king(state, x, y):
        return True
    if check_rook_capture_of_king(state, x, y):
        return True
    if check_bishop_capture_of_king(state, x, y):
        return True
    return False

def check_knight_capture_of_king(state, x, y):
    u1, u2, v1, v2, = 2, -2, 1, -1
    for u in [u1, u2]:
        for v in [v1, v2]:
            if check_if_square_is_capturable(state, x + u, y + v):
                if state.board[y + v][x + u].upper() == WHITE_KNIGHT:
                    return True
    for u in [v1, v2]:
        for v in [u1, u2]:
            if check_if_square_is_capturable(state, x + u, y + v):
                if state.board[y + v][x + u].upper() == WHITE_KNIGHT:
                    return True
    return False

def check_rook_capture_of_king(state, x, y):
    for u in range(1, 8 - x):
        if check_if_square_is_capturable(state, x + u, y):
            if state.board[y][x + u].upper() == WHITE_ROOK or state.board[y][x + u].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x + u, y):
            break

    for u in range(-1, -x - 1, -1):
        if check_if_square_is_capturable(state, x + u, y):
            if state.board[y][x + u].upper() == WHITE_ROOK or state.board[y][x + u].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x + u, y):
            break

    for v in range(1, 8 - y):
        if check_if_square_is_capturable(state, x, y + v):
            if state.board[y + v][x].upper() == WHITE_ROOK or state.board[y + v][x].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x, y + v):
            break


    for v in range(-1, -y - 1, -1):
        if check_if_square_is_capturable(state, x, y + v):
            if state.board[y + v][x].upper() == WHITE_ROOK or state.board[y + v][x].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x, y + v):
            break

    return False

def check_bishop_capture_of_king(state, x, y):
    for u in range(1, 7 - max(x, y)):
        if check_if_square_is_capturable(state, x + u, y + u):
            if state.board[y + u][x + u].upper() == WHITE_BISHOP or state.board[y + u][x + u].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x + u, y + u):
            break

    for u in range(-1, max(-x, -y) - 1, -1):
        if check_if_square_is_capturable(state, x + u, y + u):
            if state.board[y + u][x + u].upper() == WHITE_BISHOP or state.board[y + u][x + u].upper() == WHITE_QUEEN:
                return True
        if check_if_square_is_empty(state, x + u, y + u):
            break

    for v in range(1, 7 - max(x, y)):
        if check_if_square_is_capturable(state, x - v, y + v):
            if state.board[y - v][x + v].upper() == WHITE_BISHOP or state.board[y - v][x + v].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x - v, y + v):
            break

    for v in range(1, min(7 - x, y)):
        if check_if_square_is_capturable(state, x + v, y - v):
            if state.board[y - v][x + v].upper() == WHITE_BISHOP or state.board[y - v][x + v].upper() == WHITE_QUEEN:
                return True
        if not check_if_square_is_empty(state, x + v, y - v):
            break

    return False

def check_if_square_is_empty(state, x, y):
    if 0 <= x <= 7 and 0 <= y <= 7:
        return state.board[y][x] == "."
    return False


def check_if_square_is_capturable(state, x, y):
    if 0 <= x <= 7 and 0 <= y <= 7:
        if ((state.color == COLOR_WHITE and state.board[y][x].islower()) or
                (state.color == COLOR_BLACK and state.board[y][x].isupper())):
            return True
    return False