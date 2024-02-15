# This class is used to calculalte all legal moves that are possible on a given board


from Constants.pieceConstants import *
from MoveGeneration.Checks.check import check_if_king_is_in_check

# Calculate all the legal possible moves
# For move ordering purposes the captures are put in the front
#############################################################
# In the moment there are no checks if the king is in check or if a piece is pinned. If that is the case and the king can
# be taken a big penalty is given so the engine will not do this - Note: Due to the horizon effect this does not work every time
# but for the moment it is okay
def get_legal_moves(state):
    advances, captures = [], []
    if state.color == COLOR_WHITE:
        for y in range(8):
            for x in range(8):
                match state.board[y][x]:
                    case "P":
                        possible_advances, possible_captures = pawn_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "R":
                        possible_advances, possible_captures = rook_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "N":
                        possible_advances, possible_captures = knight_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "B":
                        possible_advances, possible_captures = bishop_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "K":
                        possible_advances, possible_captures = king_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "Q":
                        possible_advances, possible_captures = queen_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
    else:
        for y in range(8):
            for x in range(8):
                match state.board[y][x]:
                    case "p":
                        possible_advances, possible_captures = pawn_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "r":
                        possible_advances, possible_captures = rook_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "n":
                        possible_advances, possible_captures = knight_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "b":
                        possible_advances, possible_captures = bishop_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "k":
                        possible_advances, possible_captures = king_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
                    case "q":
                        possible_advances, possible_captures = queen_moves(state, x, y)
                        advances += possible_advances
                        captures += possible_captures
    return captures + advances


def pawn_moves(state, x, y):
    possible_advances = []
    possible_captures = []
    if state.color == COLOR_WHITE:
        # normal advance
        if check_if_square_is_empty(state, x, y - 1):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x, y - 1))
            # move from baseline
            if y == 6 and check_if_square_is_empty(state, x, y - 2):
                possible_advances.append(convert_move_to_long_alg_notation(x, y, x, y - 2))
        # capture piece
        for u in [-1, 1]:
            if check_if_square_is_capturable(state,x + u, y - 1):
                possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y - 1))
            # EnPassant
            if ord(state.en_passant[0]) - 97 == x + u:
                possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y - 1))
    else:
        # normal advance
        if check_if_square_is_empty(state, x, y + 1):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x, y + 1))
            # move from baseline
            if y == 1 and check_if_square_is_empty(state, x, y + 2):
                possible_advances.append(convert_move_to_long_alg_notation(x, y, x, y + 2))
        # capture piece
        for u in [-1, 1]:
            if check_if_square_is_capturable(state, x + u, y + 1):
                possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y + 1))
            # EnPassant
            if ord(state.en_passant[0]) - 97 == x + u:
                possible_advances.append(convert_move_to_long_alg_notation(x, y, x + u, y + 1))
    return possible_advances, possible_captures


def rook_moves(state, x, y):
    possible_advances = []
    possible_captures = []
    # x-axis to the right
    for u in range(1, 8 - x):
        if check_if_square_is_empty(state, x + u, y):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x + u, y))
        elif check_if_square_is_capturable(state, x + u, y):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y))
            break
        else:
            break
    # x-axis to the left
    for u in range(-1, -x - 1, -1):
        if check_if_square_is_empty(state, x + u, y):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x + u, y))
        elif check_if_square_is_capturable(state, x + u, y):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y))
            break
        else:
            break
    # y-axis to the top
    for v in range(1, 8 - y):
        if check_if_square_is_empty(state, x, y + v):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x, y + v))
        elif check_if_square_is_capturable(state, x, y + v):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x, y + v))
            break
        else:
            break
    # y-axis to the bottom
    for v in range(-1, -y - 1, -1):
        if check_if_square_is_empty(state, x, y + v):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x, y + v))
        elif check_if_square_is_capturable(state, x, y + v):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x, y + v))
            break
        else:
            break
    return possible_advances, possible_captures

def knight_moves(state, x, y):
    possible_advances = []
    possible_captures = []
    u1, u2, v1, v2 = 2, -2, 1, -1
    # horizontal two squares
    knight_move(possible_advances, possible_captures, state, x, y, u1, u2, v1, v2)
    knight_move(possible_advances, possible_captures, state, x, y, v1, v2, u1, u2)
    # horizontal one square
    return possible_advances, possible_captures


def knight_move(possible_advances, possible_captures, state, x, y, u1, u2, v1, v2):
    for u in [u1, u2]:
        if 0 <= (x + u) <= 7:
            for v in [v1, v2]:
                if 0 <= (y + v) <= 7:
                    if check_if_square_is_empty(state, x + u, y + v):
                        possible_advances.append(convert_move_to_long_alg_notation(x, y, x + u, y + v))
                    elif check_if_square_is_capturable(state, x + u, y + v):
                        possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y + v))
                        break
                    else:
                        break


def bishop_moves(state, x, y):
    possible_advances = []
    possible_captures = []
    # diagonal right top
    for u in range(1, 7 - max(x, y)):
        if check_if_square_is_empty(state, x + u, y + u):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x + u, y + u))
        elif check_if_square_is_capturable(state, x + u, y + u):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y + u))
            break
        else:
            break
    # diagonal left bottom
    for u in range(-1, max(-x, -y) - 1, -1):
        if check_if_square_is_empty(state, x + u, y + u):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x + u, y + u))
        elif check_if_square_is_capturable(state, x + u, y + u):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x + u, y + u))
            break
        else:
            break
    # diagonal left top
    for v in range(1, 7 - max(x, y)):
        if check_if_square_is_empty(state, x - v, y + v):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x - v, y + v))
        elif check_if_square_is_capturable(state, x - v, y + v):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x - v, y + v))
            break
        else:
            break
    # diagonal right bottom
    for v in range(1, min(7 - x, y)):
        if check_if_square_is_empty(state, x + v, y - v):
            possible_advances.append(convert_move_to_long_alg_notation(x, y, x + v, y - v))
        elif check_if_square_is_capturable(state, x + v, y - v):
            possible_captures.append(convert_move_to_long_alg_notation(x, y, x + v, y - v))
            break
        else:
            break
    return possible_advances, possible_captures


def queen_moves(state, i, j):
    possible_advances_rook, possible_captures_rook = rook_moves(state, i, j)
    possible_advances_bishop, possible_captures_bishop = bishop_moves(state, i, j)
    return possible_advances_rook + possible_advances_bishop, possible_captures_rook + possible_captures_bishop


def king_moves(state, i, j):
    possible_advances = []
    possible_captures = []
    # All the possible squares around the king
    for u in [-1, 0, 1]:
        if 0 <= (i + u) <= 7:
            for v in [-1, 0, 1]:
                if 0 <= (j + v) <= 7:
                    if check_if_square_is_empty(state, i + u, j + v):
                        possible_advances.append(convert_move_to_long_alg_notation(i, j, i + u, j + v))
                    elif check_if_square_is_capturable(state, i + u, j + v):
                        possible_captures.append(convert_move_to_long_alg_notation(i, j, i + u, j + v))
                        break
                    else:
                        break
    return possible_advances, possible_captures

def is_castling_possible(state):
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

# Converts the array indexes to the long notation used in UCI
# a2a4 for the pawn at a2 that moves 2 squares to the front on its first move
def convert_move_to_long_alg_notation(old_x, old_y, new_x, new_y):
    long_notation = ""
    long_notation += chr(old_x + 97)
    long_notation += str(8 - old_y)
    long_notation += chr(new_x + 97)
    long_notation += str(8 - new_y)
    return long_notation
