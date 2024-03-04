from Application.Constants.pieceConstants import *


def find_king(state):
    for row in range(8):
        for col in range(8):
            if state.color == COLOR_WHITE and state.board[row][col] == WHITE_KING or state.color == COLOR_BLACK and \
                    state.board[row][col] == BLACK_KING:
                return row, col


def not_check_after_move(state, move, king_row, king_col):
    state.push(move)
    state.switch_color()
    is_not_check = not check_if_king_is_in_check(state, king_row, king_col)
    state.switch_color()
    state.pop()
    return is_not_check


def check_if_king_is_in_check(state, king_row, king_col):
    is_check = False
    if check_knight_capture_of_king(state, king_row, king_col):
        is_check = True
    if not is_check and check_rook_capture_of_king(state, king_row, king_col):
        is_check = True
    if not is_check and check_bishop_capture_of_king(state, king_row, king_col):
        is_check = True
    if not is_check and check_pawn_capture_of_king(state, king_row, king_col):
        is_check = True
    if not is_check and check_king_capture_of_king(state, king_row, king_col):
        is_check = True
    return is_check


def check_pawn_capture_of_king(state, row, col):
    if state.color == COLOR_WHITE:
        pawn = BLACK_PAWN
        row_addition = -1
    else:
        pawn = WHITE_PAWN
        row_addition = 1
    for u in [-1, 1]:
        if check_if_square_is_capturable(state, row + row_addition, col + u):
            if state.board[row + row_addition][col + u] == pawn:
                return True
    return False


def check_knight_capture_of_king(state, row, col):
    u1, u2, v1, v2, = 2, -2, 1, -1
    for u in [u1, u2]:
        for v in [v1, v2]:
            if check_if_square_is_capturable(state, row + u, col + v):
                #if state.board[row + u][col + v] == WHITE_KNIGHT and state.color == COLOR_BLACK or state.board[row + u][col + v] == BLACK_KNIGHT and state.color == COLOR_WHITE:
                if state.board[row + u][col + v].upper() == WHITE_KNIGHT:
                    return True
    for u in [v1, v2]:
        for v in [u1, u2]:
            if check_if_square_is_capturable(state, row + u, col + v):
                #if state.board[row + u][col + v] == WHITE_KNIGHT and state.color == COLOR_BLACK or state.board[row + u][col + v] == BLACK_KNIGHT and state.color == COLOR_WHITE:
                if state.board[row + u][col + v].upper() == WHITE_KNIGHT:
                    return True
    return False


def check_rook_capture_of_king(state, row, col):
    # To the right
    for u in range(1, 8 - col):
        if check_if_square_is_capturable(state, row, col + u):
            if state.board[row][col + u].upper() == WHITE_ROOK or state.board[row][col + u].upper() == WHITE_QUEEN:

            #if ((state.board[row][col + u] == WHITE_ROOK and state.color == COLOR_BLACK or
            #        state.board[row][col + u] == WHITE_QUEEN and state.color == COLOR_BLACK) or
            #    (state.board[row][col + u] == BLACK_ROOK and state.color == COLOR_WHITE or
            #        state.board[row][col + u] == BLACK_QUEEN and state.color == COLOR_WHITE)):
                return True
            else:
                break
        if not check_if_square_is_empty(state, row, col + u):
            break

    # To the left
    for u in range(1, col + 1):
        if check_if_square_is_capturable(state, row, col - u):
            if state.board[row][col - u].upper() == WHITE_ROOK or state.board[row][col - u].upper() == WHITE_QUEEN:

            #if ((state.board[row][col - u] == WHITE_ROOK and state.color == COLOR_BLACK or
            #        state.board[row][col - u] == WHITE_QUEEN and state.color == COLOR_BLACK) or
            #    (state.board[row][col - u] == BLACK_ROOK and state.color == COLOR_WHITE or
            #        state.board[row][col - u] == BLACK_QUEEN and state.color == COLOR_WHITE)):
                return True
            else:
                break
        if not check_if_square_is_empty(state, row, col - u):
            break

    # To the bottom
    for v in range(1, 8 - row):
        if check_if_square_is_capturable(state, row + v, col):
            if state.board[row + v][col].upper() == WHITE_ROOK or state.board[row + v][col].upper() == WHITE_QUEEN:

            #if ((state.board[row + v][col] == WHITE_ROOK and state.color == COLOR_BLACK or
            #        state.board[row + v][col] == WHITE_QUEEN and state.color == COLOR_BLACK) or
            #    (state.board[row + v][col] == BLACK_ROOK and state.color == COLOR_WHITE or
            #        state.board[row + v][col] == BLACK_QUEEN and state.color == COLOR_WHITE)):
                return True
            else:
                break
        if not check_if_square_is_empty(state, row + v, col):
            break

    # To the top
    for v in range(1, row + 1):
        if check_if_square_is_capturable(state, row - v, col):
            if state.board[row - v][col].upper() == WHITE_ROOK or state.board[row - v][col].upper() == WHITE_QUEEN:

            #if ((state.board[row - v][col] == WHITE_ROOK and state.color == COLOR_BLACK or
            #        state.board[row - v][col] == WHITE_QUEEN and state.color == COLOR_BLACK) or
            #    (state.board[row - v][col] == BLACK_ROOK and state.color == COLOR_WHITE or
            #        state.board[row - v][col] == BLACK_QUEEN and state.color == COLOR_WHITE)):
                return True
            else:
                break
        if not check_if_square_is_empty(state, row - v, col):
            break

    return False


def check_bishop_capture_of_king(state, row, col):
    # Bottom right
    for u in range(1, 8 - max(row, col)):
        if check_if_square_is_capturable(state, row + u, col + u):
            if state.board[row + u][col + u].upper() == WHITE_BISHOP or state.board[row + u][col + u].upper() == WHITE_QUEEN:
                return True
            else:
                break
        if not check_if_square_is_empty(state, row + u, col + u):
            break

    # Top left
    for u in range(1, min(row, col) + 1):
        if check_if_square_is_capturable(state, row - u, col - u):
            if state.board[row - u][col - u].upper() == WHITE_BISHOP or state.board[row - u][col - u].upper() == WHITE_QUEEN:
                return True
            else:
                break
        if not check_if_square_is_empty(state, row - u, col - u):
            break

    # Top right
    for v in range(1, min(row, 7 - col) + 1):
        if check_if_square_is_capturable(state, row - v, col + v):
            if state.board[row - v][col + v].upper() == WHITE_BISHOP or state.board[row - v][col + v].upper() == WHITE_QUEEN:
                return True
            else:
                break
        if not check_if_square_is_empty(state, row - v, col + v):
            break

    # Bottom left
    for v in range(1, min(7 - row, col) + 1):
        if check_if_square_is_capturable(state, row + v, col - v):
            if state.board[row + v][col - v].upper() == WHITE_BISHOP or state.board[row + v][col - v].upper() == WHITE_QUEEN:

            #if ((state.board[row + u][col - u] == WHITE_BISHOP and state.switch_color == COLOR_BLACK or
            #        state.board[row + u][col - u] == WHITE_QUEEN and state.color == COLOR_BLACK) or
            #        (state.board[row + u][col - u] == BLACK_BISHOP and state.switch_color == COLOR_WHITE or
            #         state.board[row + u][col - u] == BLACK_QUEEN and state.color == COLOR_WHITE)):
                return True
            else:
                break
        if not check_if_square_is_empty(state, row + v, col - v):
            break

    return False

def check_king_capture_of_king(state, king_row, king_col):
    # All the possible squares around the king
    for u in [-1, 0, 1]:
        if 0 <= (king_row + u) <= 7:
            for v in [-1, 0, 1]:
                if 0 <= (king_col + v) <= 7:
                    if check_if_square_is_capturable(state, king_row + u, king_col + v):
                        if state.board[king_row + u][king_col + v].upper() == WHITE_KING:
                            return True
    return False


def check_if_square_is_empty(state, row, col):
    if 0 <= row <= 7 and 0 <= col <= 7:
        return state.board[row][col] == "."
    return False


def check_if_square_is_capturable(state, row, col):
    if 0 <= row <= 7 and 0 <= col <= 7:
        if ((state.color == COLOR_WHITE and state.board[row][col].islower()) or
                (state.color == COLOR_BLACK and state.board[row][col].isupper())):
            return True
    return False
