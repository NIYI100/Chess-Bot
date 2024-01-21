# Pieces - naming as per FEN (Forsyth-Edwards Notation)
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

