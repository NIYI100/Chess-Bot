# Represenation of a chessboard + logic

import copy
from Application.BoardModel.castlingRights import CastlingRights
from Application.BoardModel.history import History
from Application.Constants.pieceConstants import *
import Application.TranspositionTable.ZobristKey.ZobristKeyCalculations as zobrist
#from MoveGeneration.castling import update_castling_rights as update_castling_rights


class BoardState:
    """
    This class represents the State of the chess game.
    """

    def __init__(self):
        self.board = None
        self.color = None
        self.castle_rights = CastlingRights()
        self.en_passant = None
        self.halfmoves = None
        self.fullmoves = None
        self.zobristKey = None

    def __eq__(self, other):
        """
        Checks if two Boardstates have the same values. At the moment this is only used in testing.
        :param other: The other Boardstate object
        """
        return (self.board == other.board
                and self.color == other.color
                and vars(self.castle_rights) == vars(other.castle_rights)
                and self.en_passant == other.en_passant
                and self.halfmoves == other.halfmoves
                and self.fullmoves == other.fullmoves
                and self.zobristKey == other.zobristKey)

    def create_initial_board(self):
        """
        Creates the initial BoardState corresponding to the normal chess starting position.
        Initializes the zobristKey.
        """
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
        self.color = COLOR_WHITE
        self.castle_rights = CastlingRights()
        self.en_passant = "-"
        self.halfmoves = 0
        self.fullmoves = 1
        self.zobristKey = zobrist.get_zobrist_key_of_board(self)

    def _put_move_on_board(self, move):
        """
        Puts the move on the board
        :param move: The move to put on the board
        """
        old_row, old_col, new_row, new_col = self.convert_move_string_to_coordinates(move)
        if move in ["e1b1", "e1g1", "e8b8", "e8g8"] and self._is_castling(move):
            self.put_castling_on_the_board(move)
        elif self._move_is_promotion(old_row, old_col, new_row):
            self._promote_pawn_to_queen(old_row, old_col, new_row, new_col)
        else:
            self.board[new_row][new_col] = self.board[old_row][old_col]
            self.board[old_row][old_col] = EMPTY

    def _move_is_promotion(self, old_row, old_col, new_row) -> bool:
        """
        Returns if the move corresponding to old_row, old_col and new_row is a promotion
        :param old_row: The old row of the piece that should be checked
        :param old_col: The old column of the piece that should be checked
        :param new_row: The new row of the piece that should be checked
        """
        row = 0
        piece = WHITE_PAWN
        if self.color == COLOR_BLACK:
            row = 7
            piece = BLACK_PAWN
        if new_row == row and self.board[old_row][old_col] == piece:
            return True
        else:
            return False

    # TODO: At the moment only a automated promotion to queen is possible
    def _promote_pawn_to_queen(self, old_row, old_col, new_row, new_col):
        """
        Promotes the Pawn at [old_row][old_col] to a queen at [new_row][new_col]
        :param old_row: The old row of the piece
        :param old_col: The old column of the piece
        :param new_row: The new row of the piece
        :param new_col: The new column of the piece
        """
        self.board[old_row][old_col] = EMPTY
        piece = WHITE_QUEEN
        if self.color == COLOR_BLACK:
            piece = BLACK_QUEEN

        self.board[new_row][new_col] = piece

    def put_castling_on_the_board(self, castling_move):
        """
        Puts a castling move on the board
        :param castling_move: the castling move
        """
        match castling_move:
            case "e1b1":
                self.board[7][2] = WHITE_ROOK
                self.board[7][0] = EMPTY
                self.board[7][1] = WHITE_KING
                self.board[7][3] = EMPTY
            case "e1g1":
                self.board[7][5] = WHITE_ROOK
                self.board[7][7] = EMPTY
                self.board[7][6] = WHITE_KING
                self.board[7][3] = EMPTY
            case "e8b8":
                self.board[0][2] = BLACK_ROOK
                self.board[0][0] = EMPTY
                self.board[0][1] = BLACK_KING
                self.board[0][3] = EMPTY
            case "e8g8":
                self.board[0][5] = BLACK_ROOK
                self.board[0][7] = EMPTY
                self.board[0][6] = BLACK_KING
                self.board[0][3] = EMPTY

    def update_zobrist_for_move(self, move):
        """
        Updates the zobrist key for the board depending on th move
        :param move: The move for which the zobrist key should be updated
        """
        old_col = ord(move[0]) - 97
        old_row = 8 - int(move[1])
        new_col = ord(move[2]) - 97
        new_row = 8 - int(move[3])
        if move in ["e1b1", "e1g1", "e8b8", "e8g8"] and self._is_castling(move):
            zobrist.update_zobrist_for_castling(self, move)
        elif self._move_is_promotion(old_row, old_col, new_row):
            zobrist.update_zobrist_for_promotion(self, old_row, old_col, new_row, new_col)
        else:
            zobrist.update_key_for_move(self, old_col, old_row, new_col, new_row)

    def _is_castling(self, move):
        """
        Checks if the move is castling or if it is another move
        :param move: The move to check
        """
        match move:
            case "e1b1":
                return self.castle_rights.white_castle_long
            case "e1g1":
                return self.castle_rights.white_castle_short
            case "e8b8":
                return self.castle_rights.black_castle_long
            case "e8g8":
                return self.castle_rights.black_castle_short


    def update_halfmove(self, move):
        """
        Updates the halfmove count of the game or resets it, if:

        - The move is a pawn advancement
        - The move is a capture
        - The move is castling
        :param move: The move
        """
        old_col = ord(move[0]) - 97
        old_row = 8 - int(move[1])
        new_col = ord(move[2]) - 97
        new_row = 8 - int(move[3])
        if self.board[old_row][old_col].upper() == WHITE_PAWN or self.board[new_row][new_col] != EMPTY or move in ["e1b1", "e1g1", "e8b8", "e8g8"]:
        #if move in ["a2a4", "b2b4", "c2c4", "d2d4","e2e4", "f2f4","g2g4", "h2h4"] or move in ["a7a5", "b7b5", "c7c5", "d7d5","e7e5", "f7f5","g7g5", "h7h5"] or self.board[new_row][new_col] != EMPTY:
            self.halfmoves = 0
        else:
            self.halfmoves += 1

    def update_enPassant(self, move):
        """
        Updates the enPassant value for the FEN string
        :param move: The move which updates the FEN string
        """
        if move in ["a2a4", "b2b4", "c2c4", "d2d4","e2e4", "f2f4","g2g4", "h2h4"]:
            self.en_passant = move[0] + str(int(move[1]) + 1)
        elif move in ["a7a5", "b7b5", "c7c5", "d7d5","e7e5", "f7f5","g7g5", "h7h5"]:
            self.en_passant = move[0] + str(int(move[1]) - 1)
        else:
            self.en_passant = "-"

    def update_fullmove(self):
        """
        Updates the fullmove count if its blacks turn
        """
        if self.color == COLOR_BLACK:
            self.fullmoves += 1



    def execute_move(self, move):
        """
        Execute the move. This includes:

        - Updating the zobrist key
        - Putting the move on board
        - Updating the enPassant value
        - Updating the castling rights
        - Updating the halfmove count
        - Updating the fullmove count
        - Switching the color
        :param move: The move to execute
        """
        self.update_zobrist_for_move(move)
        self._put_move_on_board(move)

        self.castle_rights.update_castling(move)
        self.update_enPassant(move)
        self.update_halfmove(move)
        self.update_fullmove()

        self.switch_color()
        zobrist.update_color_in_zobrist_key(self)


    def push(self, move):
        """
        Executes the move and saves the board in the History() singleton.
        This method is mostly used in the NegaMax algorithm
        :param move: The move to execute and save
        """
        History().append(self._save_state())
        self.execute_move(move)

    # Chat-GPT - Used to make a deepcopy of the board as well as the other variables so the old state can be reconstructed
    def _save_state(self):
        """
        Returns a deep copy of the BoardState
        """
        return copy.deepcopy(self.board), self.color, self.castle_rights, self.en_passant, self.halfmoves, self.fullmoves, self.zobristKey

    def pop(self):
        """
        Pops and restores the last BoardState from the History() singleton.
        """
        last_state = History().pop()
        self._restore_state(last_state)

    def _restore_state(self, history):
        """
        Sets a History() entry to the BoardState
        :param history: The History() entry
        """
        self.board, self.color, self.castle_rights, self.en_passant, self.halfmoves, self.fullmoves, self.zobristKey = history

    def switch_color(self):
        """
        Switches the color of the active player
        """
        if self.color == COLOR_WHITE:
            self.color = COLOR_BLACK
        else:
            self.color = COLOR_WHITE

    def convert_move_string_to_coordinates(self, move):
        """
        Converts the move to coordinates
        :param move: The move
        """
        old_col = ord(move[0]) - 97
        old_row = 8 - int(move[1])
        new_col = ord(move[2]) - 97
        new_row = 8 - int(move[3])

        return old_row, old_col, new_row, new_col
