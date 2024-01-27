from ChessBot.myConstants import *


class BoardState:

    def __init__(self, board=None, color=None, castleRights=None, enPassant=None, halfmoves=None, fullmoves=None):
        self.board = board
        self.color = color
        self.castleRights = castleRights
        self.enPassant = enPassant
        self.halfmoves = halfmoves
        self.fullmoves = fullmoves

    # Creates the initial board
    def create_initial_board(self):
        self.board = [
            [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
            [BLACK_PAWN] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [WHITE_PAWN] * 8,
            [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]
        ]
        self.color = "w"
        self.castleRights = "QKqk"
        self.enPassant = "-"
        self.halfmoves = "0"
        self.fullmoves = "0"

    # executes a given move on the board
    def execute_move(self, move):
        old_x = ord(move[0]) - 97
        old_y = 8 - int(move[1])
        new_x = ord(move[2]) - 97
        new_y = 8 - int(move[3])
        self.board[new_y][new_x] = self.board[old_y][old_x]
        self.board[old_y][old_x] = "."