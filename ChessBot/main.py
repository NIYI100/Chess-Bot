# Pieces - naming as per FEN (Forsyth-Edwards Notation)
from ChessBot.board import BoardState

WHITE_ROOK = "R"
WHITE_KNIGHT = "N"
WHITE_BISHOP = "B"
WHITE_QUEEN = "Q"
WHITE_KING = "K"
WHITE_PAWN = "P"
BLACK_ROOK = "r"
BLACK_KNIGHT = "n"
BLACK_BISHOP = "b"
BLACK_QUEEN = "q"
BLACK_KING = "k"
BLACK_PAWN = "p"

EMPTY = "."

COLOR_WHITE = "w"
COLOR_BLACK = "b"


# Creates the initial board
def create_initial_board():
    return [
        [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK],
        [WHITE_PAWN] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [BLACK_PAWN] * 8,
        [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
    ]


def fen_to_board(fen):
    fen_array = fen.split(" ")
    piece_placement = get_piece_placement_from_rows(fen_array[0])

    color = fen_array[1]

    castleRights = fen_array[2]

    enPassant = fen_array[3]

    halfmoves = fen_array[4]

    fullmoves = fen_array[5]

    return BoardState(piece_placement, color, castleRights, enPassant, halfmoves, fullmoves)


def get_piece_placement_from_rows(boardFEN):
    rows = boardFEN.split("/")
    piecePlacement = []
    for row in rows:
        rowArray = []
        for char in row:
            rowArray.extend(["."] * int(char)) if char.isdigit() else rowArray.append(char)
        piecePlacement.append(rowArray)
    return piecePlacement


def get_legal_moves(state):
    moves = []
    for i in range(8):
        for j in range(8):
            match state.board[i][j].upper():
                case "P":
                    moves.append(pawn_moves(state, i, j))
                case "R":
                    moves.append(rook_moves(state, i, j))
                case "N":
                    moves.append(knight_moves(state, i, j))
                case "B":
                    moves.append(bishop_moves(state, i, j))
                case "K":
                    moves.append(king_moves(state, i, j))
                case "Q":
                    moves.append(queen_moves(state, i, j))
    print(moves)

#TODO Still to do
def pawn_moves(state, i, j):
    return


def rook_moves(state, i, j):
    possible_moves = []
    for u in range(1, 8 - i):
        if check_if_sqaure_is_empty(state, i + u, j):
            possible_moves.append((i + u, j))
        elif check_if_square_is_capturable(state, i + u, j):
            possible_moves.append((i + u, j))
            break
        else:
            break
    for u in range(-1, -i - 1, -1):
        if check_if_sqaure_is_empty(state, i + u, j):
            possible_moves.append((i + u, j))
        elif check_if_square_is_capturable(state, i + u, j):
            possible_moves.append((i + u, j))
            break
        else:
            break
    for v in range(1, 8 - j):
        if check_if_sqaure_is_empty(state, i, j + v):
            possible_moves.append((i, j + v))
        elif check_if_square_is_capturable(state, i, j + v):
            possible_moves.append((i, j + v))
            break
        else:
            break
    for v in range(-1, -j - 1, -1):
        if check_if_sqaure_is_empty(state, i, j + v):
            possible_moves.append((i, j + v))
        elif check_if_square_is_capturable(state, i, j + v):
            possible_moves.append((i, j + v))
            break
        else:
            break
    return possible_moves


def knight_moves(state, i, j):
    possible_moves = []
    for u in [2, -2]:
        if 0 <= (i + u) <= 7:
            for v in [1, -1]:
                if 0 <= (j + v) <= 7:
                    if check_if_sqaure_is_empty(state, i + u, j + v):
                        possible_moves.append((i + u, j + v))
                    elif check_if_square_is_capturable(state, i + u, j + v):
                        possible_moves.append((i + u, j + v))
                        break
                    else:
                        break
    for u in [1, -1]:
        if 0 <= (i + u) <= 7:
            for v in [2, -2]:
                if 0 <= (j + v) <= 7:
                    if check_if_sqaure_is_empty(state, i + u, j + v):
                        possible_moves.append((i + u, j + v))
                    elif check_if_square_is_capturable(state, i + u, j + v):
                        possible_moves.append((i + u, j + v))
                        break
                    else:
                        break
    return possible_moves


def bishop_moves(state, i, j):
    possible_moves = []
    for u in range(1, 7 - max(i, j)):
        if check_if_sqaure_is_empty(state, i + u, j + u):
            possible_moves.append((i + u, j + u))
        elif check_if_square_is_capturable(state, i + u, j + u):
            possible_moves.append((i + u, j + u))
            break
        else:
            break
    for u in range(-1, max(-i, -j) - 1, -1):
        if check_if_sqaure_is_empty(state, i + u, j + u):
            possible_moves.append((i + u, j + u))
        elif check_if_square_is_capturable(state, i + u, j + u):
            possible_moves.append((i + u, j + u))
            break
        else:
            break
    for v in range(1, 7 - max(i, j)):
        if check_if_sqaure_is_empty(state, i - v, j + v):
            possible_moves.append((i - v, j + v))
        elif check_if_square_is_capturable(state, i - v, j + v):
            possible_moves.append((i - v, j + v))
            break
        else:
            break
    for v in range(-1, -j - 1, -1):
        if check_if_sqaure_is_empty(state, i - v, j + v):
            possible_moves.append((i - v, j + v))
        elif check_if_square_is_capturable(state, i - v, j + v):
            possible_moves.append((i - v, j + v))
            break
        else:
            break
    return possible_moves


def queen_moves(state, i, j):
    return rook_moves(state, i, j) + bishop_moves(state, i, j)


def king_moves(state, i, j):
    possible_moves = []
    for u in [-1, 0, 1]:
        if 0 <= (i + u) <= 7:
            for v in [-1, 0, 1]:
                if 0 <= (j + v) <= 7:
                    if check_if_sqaure_is_empty(state, i + u, j + v):
                        possible_moves.append((i + u, j + v))
                    elif check_if_square_is_capturable(state, i + u, j + v):
                        possible_moves.append((i + u, j + v))
                        break
                    else:
                        break
    return possible_moves


def check_if_sqaure_is_empty(state, i, j):
    return state.board[i][j] == "."


def check_if_square_is_capturable(state, i, j):
    if ((state.color == COLOR_WHITE and state.board[i][j].islower()) or
            (state.color == COLOR_BLACK and state.board[i][j].isupper()) or
            (state.board[i][j] == ".")):
        return True
    return False


get_legal_moves(fen_to_board("8/2P2n2/8/1p1Pp2p/pP2Pp1P/P4P1K/7P/8 b - - 99 50"))
