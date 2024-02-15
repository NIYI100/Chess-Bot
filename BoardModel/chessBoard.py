# Represenation of a chessboard + logic

import copy

from Constants.pieceConstants import *
import TranspositionTable.ZobristKey.ZobristKeyCalculations as zobrist
from MoveGeneration.castling import update_castling_rights as update_castling_rights


class BoardState:

    def __init__(self, board=None, color=None, castle_rights=None, en_passant=None, halfmoves=None, fullmoves=None):
        self.board = board
        self.color = color
        self.castle_rights = castle_rights
        self.en_passant = en_passant
        self.halfmoves = halfmoves
        self.fullmoves = fullmoves
        self.zobristKey = None
        self.history = []

    # Creates the initial board
    def create_initial_board(self, zobrist_random_values):
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
        self.castle_rights = "QKqk"
        self.en_passant = "-"
        self.halfmoves = "0"
        self.fullmoves = "0"
        self.zobristKey = zobrist.get_zobrist_key_of_board(self, zobrist_random_values)

    # Executes a given move on the board
    def execute_move(self, move, zobrist_values):
        if move in ["e1b1", "e1g1", "e8b8", "e8g8"]:
            self.execute_castling(move, zobrist_values)
        else:

            old_x = ord(move[0]) - 97
            old_y = 8 - int(move[1])
            new_x = ord(move[2]) - 97
            new_y = 8 - int(move[3])

            zobrist.update_key_for_move(self, old_x, old_y, new_x, new_y, zobrist_values)
            self.board[new_y][new_x] = self.board[old_y][old_x]
            self.board[old_y][old_x] = EMPTY
        update_castling_rights(move)

    def execute_castling(self, move, zobrist_values):
        match move:
            case "e1b1":
                self.board[0][2] = WHITE_ROOK
                self.board[0][0] = EMPTY
                self.board[0][1] = WHITE_KING
                self.board[0][4] = EMPTY
                zobrist.update_key_for_move(self, 0, 0, 2, 0, zobrist_values)
                zobrist.update_key_for_move(self, 4, 0, 1, 0, zobrist_values)
            case "e1g1":
                self.board[0][5] = WHITE_ROOK
                self.board[0][7] = EMPTY
                self.board[0][6] = WHITE_KING
                self.board[0][4] = EMPTY
                zobrist.update_key_for_move(self, 7, 0, 5, 0, zobrist_values)
                zobrist.update_key_for_move(self, 4, 0, 6, 0, zobrist_values)
            case "e8b8":
                self.board[7][2] = BLACK_ROOK
                self.board[7][0] = EMPTY
                self.board[7][1] = BLACK_KING
                self.board[7][4] = EMPTY
                zobrist.update_key_for_move(self, 0, 7, 2, 7, zobrist_values)
                zobrist.update_key_for_move(self, 4, 7, 1, 7, zobrist_values)
            case "e8g8":
                self.board[7][5] = BLACK_ROOK
                self.board[7][7] = EMPTY
                self.board[7][6] = BLACK_KING
                self.board[7][4] = EMPTY
                zobrist.update_key_for_move(self, 7, 7, 5, 7, zobrist_values)
                zobrist.update_key_for_move(self, 4, 7, 6, 7, zobrist_values)

    # Used to push a move on the board - This is used in the NagaMax Algorithm
    def push(self, move, zobrist_values):
        self.history.append(self._save_state())
        self.execute_move(move, zobrist_values)
        self.switch_color(zobrist_values)

    # Chat-GPT - Used to make a deepcopy of the board as well as the other variables so the old state can be reconstructed
    def _save_state(self):
        return copy.deepcopy(self.board), self.color, self.castle_rights, self.en_passant, self.halfmoves, self.fullmoves, self.zobristKey

    # Used to pop the topmost state of the history and set the board to the state before that
    def pop(self, zobrist_values):
        last_state = self.history.pop()
        self._restore_state(last_state)
        self.switch_color(zobrist_values)

    # Restores the state
    def _restore_state(self, state):
        self.board, self.color, self.castle_rights, self.en_passant, self.halfmoves, self.fullmoves, self.zobristKey = state

    # Used to switch the active color and update the zobrist-key accordingly
    def switch_color(self, zobrist_values):
        if self.color == COLOR_WHITE:
            self.color = COLOR_BLACK
        else:
            self.color = COLOR_WHITE
        zobrist.update_color_in_zobrist_key(self, zobrist_values)
