import unittest

from Application.BoardModel.boardConversion import *
from Application.BoardModel.chessBoard import BoardState


class TestBoardConversion(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()

    def test_get_piece_placement_of_starting_position(self):
        """
        Tests the return of the piece placement for the starting position
        """
        piecePlacement = [
            [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
            [BLACK_PAWN] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [WHITE_PAWN] * 8,
            [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]
        ]
        self.assertEqual(get_piece_placement_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"), piecePlacement)

    def test_get_piece_placement_of_later_position(self):
        """
        Tests the return of the piece placement for a later position
        """
        piecePlacement = [
            [EMPTY] * 8,
            [BLACK_PAWN] * 4 + [BLACK_KING, BLACK_ROOK] + [EMPTY] * 2,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 7 + [WHITE_KING],
            [WHITE_PAWN] * 6 + [EMPTY] * 2,
            [EMPTY] * 8
        ]
        self.assertEqual(get_piece_placement_from_fen("8/ppppkr2/8/8/8/7K/PPPPPP2/8"), piecePlacement)

    def test_board_to_fen_of_starting_position(self):
        """

        """
        fen = board_to_fen(self.state)
        self.assertEqual(fen, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w QKqk - 0 1")

    def test_board_to_fen_of_later_position(self):
        set_fen_to_board("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50", self.state)
        fen = board_to_fen(self.state)
        self.assertEqual(fen, "8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50")

    def test_set_fen_to_board_of_later_position(self):
        state = BoardState()
        self.state.board = [
            [EMPTY] * 8,
            [BLACK_PAWN] * 4 + [BLACK_KING, BLACK_ROOK] + [EMPTY] * 2,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 7 + [WHITE_KING],
            [WHITE_PAWN] * 6 + [EMPTY] * 2,
            [EMPTY] * 8
        ]
        self.state.color = "b"
        self.state.castle_rights.get_castling_from_string("-")
        self.state.en_passant = "-"
        self.state.halfmoves = 20
        self.state.fullmoves = 40
        self.state.zobristKey = get_zobrist_key_of_board(self.state)
        set_fen_to_board("8/ppppkr2/8/8/8/7K/PPPPPP2/8 b - - 20 40", state)
        self.assertEqual(self.state, state)