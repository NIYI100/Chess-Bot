import unittest

from Application.BoardModel.chessBoard import BoardState
from Application.BoardModel.history import History
from Application.TranspositionTable.ZobristKey.ZobristKeyCalculations import update_key_for_move
from Application.Constants.pieceConstants import *

class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()

    def test_put_normal_move_on_board(self):
        boardCopy = self.state.board
        self.state._put_move_on_board("a2a4")
        boardCopy[0][1] = EMPTY
        boardCopy[0][3] = WHITE_PAWN

        self.assertEqual(self.state.board, boardCopy)

    def test_put_castling_move_e1b1_on_board(self):
        boardCopy = self.state.board
        self.state._put_move_on_board("e1b1")
        boardCopy[7][2] = WHITE_ROOK
        boardCopy[7][0] = EMPTY
        boardCopy[7][1] = WHITE_KING
        boardCopy[7][3] = EMPTY

        self.assertEqual(self.state.board, boardCopy)

    def test_put_castling_move_e1g1_on_board(self):
        boardCopy = self.state.board
        self.state._put_move_on_board("e1g1")
        boardCopy[7][5] = WHITE_ROOK
        boardCopy[7][7] = EMPTY
        boardCopy[7][6] = WHITE_KING
        boardCopy[7][3] = EMPTY

        self.assertEqual(self.state.board, boardCopy)

    def test_put_castling_move_e8b8_on_board(self):
        boardCopy = self.state.board
        self.state._put_move_on_board("e8b8")
        boardCopy[0][2] = WHITE_ROOK
        boardCopy[0][0] = EMPTY
        boardCopy[0][1] = WHITE_KING
        boardCopy[0][3] = EMPTY

        self.assertEqual(self.state.board, boardCopy)

    def test_put_castling_move_e8g8_on_board(self):
        boardCopy = self.state.board
        self.state._put_move_on_board("e8g8")
        boardCopy[0][5] = WHITE_ROOK
        boardCopy[0][7] = EMPTY
        boardCopy[0][6] = WHITE_KING
        boardCopy[0][3] = EMPTY

        self.assertEqual(self.state.board, boardCopy)

    # TODO -> stateCopy = self.state is reference to same object i think -> So copy method
    def test_update_zobrist_for_normal_move(self):
        stateCopy = self.state
        self.state._put_move_on_board("a2a4")
        update_key_for_move(stateCopy, 0, 1, 0, 3)

        self.assertEqual(self.state.zobristKey, stateCopy.zobristKey)

    def test_update_zobrist_for_castling_move_e1b1(self):
        stateCopy = self.state
        self.state.update_zobrist_for_move("e1b1")
        update_key_for_move(stateCopy, 7, 0, 7, 2)
        update_key_for_move(stateCopy, 7, 3, 7, 1)

        self.assertEqual(self.state.zobristKey, stateCopy.zobristKey)

    def test_update_zobrist_for_castling_move_e1g1(self):
        stateCopy = self.state
        self.state.update_zobrist_for_move("e1g1")
        update_key_for_move(stateCopy, 7, 7, 7, 5)
        update_key_for_move(stateCopy, 7, 3, 7, 6)

        self.assertEqual(self.state.zobristKey, stateCopy.zobristKey)

    def test_update_zobrist_for_castling_move_e8b8(self):
        stateCopy = self.state
        self.state.update_zobrist_for_move("e8b8")
        update_key_for_move(stateCopy, 0, 0, 0, 2)
        update_key_for_move(stateCopy, 0, 3, 0, 1)

        self.assertEqual(self.state.zobristKey, stateCopy.zobristKey)

    def test_update_zobrist_for_castling_move_e8g8(self):
        stateCopy = self.state
        self.state.update_zobrist_for_move("e8g8")
        update_key_for_move(stateCopy, 0, 7, 0, 5)
        update_key_for_move(stateCopy, 0, 3, 0, 6)

        self.assertEqual(self.state.zobristKey, stateCopy.zobristKey)

    def test_update_halfmove_pawn_advance(self):
        self.state.board[4][0] = WHITE_PAWN
        self.state.halfmoves = 30
        self.state.update_halfmove("a4a5")
        self.assertEqual(self.state.halfmoves, 0)

    def test_update_halfmove_capture(self):
        self.state.board[4][0] = WHITE_QUEEN
        self.state.board[3][0] = BLACK_PAWN
        self.state.halfmoves = 30
        self.state.update_halfmove("a4a5")
        self.assertEqual(self.state.halfmoves, 0)

    def test_update_halfmove_increment(self):
        self.state.board[4][0] = WHITE_QUEEN
        self.state.board[3][0] = EMPTY
        self.state.halfmoves = 30
        self.state.update_halfmove("a4a5")
        self.assertEqual(self.state.halfmoves, 31)

    def test_update_halfmove_castling(self):
        self.state.halfmoves = 30
        self.state.update_halfmove("e1b1")
        self.assertEqual(self.state.halfmoves, 0)

    def test_update_enPassant_white(self):
        self.state.update_enPassant("a2a4")
        self.assertEqual(self.state.en_passant, "a3")

    def test_update_enPassant_black(self):
        self.state.update_enPassant("a7a5")
        self.assertEqual(self.state.en_passant, "a6")

    def test_update_enPassant_no_enPassant(self):
        self.state.en_passant = "a3"
        self.state.update_enPassant("e4e6")
        self.assertEqual(self.state.en_passant, "-")

    def test_udate_fullmove_white(self):
        self.state.color = "w"
        self.state.fullmoves = 20
        self.state.update_fullmove()
        self.assertEqual(self.state.fullmoves, 20)

    def test_udate_fullmove_black(self):
        self.state.color = "b"
        self.state.fullmoves = 20
        self.state.update_fullmove()
        self.assertEqual(self.state.fullmoves, 21)

    def test_push(self):
        history = History()
        self.assertEqual(len(history._history), 0)
        self.state.push("a2a4")
        self.assertEqual(len(history._history), 1)

    def test_pop(self):
        history = History()
        self.state.push("a2a4")
        self.assertEqual(len(history._history), 1)
        self.state.pop()
        self.assertEqual(len(history._history), 0)

    def test_switch_color(self):
        self.state.switch_color()
        self.assertEqual(self.state.color, "b")
        self.state.switch_color()
        self.assertEqual(self.state.color, "w")

    def test_promotion_of_white_pawn(self):
        self.state.board = [[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8]
        self.state.board[1][1] = WHITE_PAWN
        self.state.board[0][2] = BLACK_KING
        self.state.execute_move("b7b8")
        self.assertEqual(self.state.board[0][1], WHITE_QUEEN)

    def test_promotion_of_black_pawn(self):
        self.state.board = [[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8]
        self.state.board[6][1] = BLACK_PAWN
        self.state.board[7][2] = WHITE_KING
        self.state.color = "b"
        self.state.execute_move("b2b1")
        self.assertEqual(self.state.board[7][1], BLACK_QUEEN)


