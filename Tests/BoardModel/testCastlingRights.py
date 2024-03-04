import unittest

from Application.BoardModel.castlingRights import CastlingRights
from Application.BoardModel.chessBoard import BoardState
from Application.Constants.pieceConstants import EMPTY


class TestCastlingRights(unittest.TestCase):
    def setUp(self):
        self.castlingRights = CastlingRights()

    def test_update_castling_no_castling(self):
        self.castlingRights.update_castling("a2a4")
        castlingRights2 = CastlingRights()
        self.assertEqual(vars(self.castlingRights), vars(castlingRights2))

    def test_update_castling_rook_a1(self):
        self.castlingRights.update_castling("a1a4")
        self.assertEqual(self.castlingRights.white_castle_long, False)
        self.assertEqual(self.castlingRights.white_castle_short, True)
        self.assertEqual(self.castlingRights.black_castle_long, True)
        self.assertEqual(self.castlingRights.black_castle_short, True)

    def test_update_castling_rook_h1(self):
        self.castlingRights.update_castling("h1h4")
        self.assertEqual(self.castlingRights.white_castle_long, True)
        self.assertEqual(self.castlingRights.white_castle_short, False)
        self.assertEqual(self.castlingRights.black_castle_long, True)
        self.assertEqual(self.castlingRights.black_castle_short, True)

    def test_update_castling_king_white(self):
        self.castlingRights.update_castling("e1e3")
        self.assertEqual(self.castlingRights.white_castle_long, False)
        self.assertEqual(self.castlingRights.white_castle_short, False)
        self.assertEqual(self.castlingRights.black_castle_long, True)
        self.assertEqual(self.castlingRights.black_castle_short, True)

    def test_update_castling_rook_a8(self):
        self.castlingRights.update_castling("a8a4")
        self.assertEqual(self.castlingRights.white_castle_long, True)
        self.assertEqual(self.castlingRights.white_castle_short, True)
        self.assertEqual(self.castlingRights.black_castle_long, False)
        self.assertEqual(self.castlingRights.black_castle_short, True)

    def test_update_castling_rook_h8(self):
        self.castlingRights.update_castling("h8h4")
        self.assertEqual(self.castlingRights.white_castle_long, True)
        self.assertEqual(self.castlingRights.white_castle_short, True)
        self.assertEqual(self.castlingRights.black_castle_long, True)
        self.assertEqual(self.castlingRights.black_castle_short, False)

    def test_update_castling_king_black(self):
        self.castlingRights.update_castling("e8e3")
        self.assertEqual(self.castlingRights.white_castle_long, True)
        self.assertEqual(self.castlingRights.white_castle_short, True)
        self.assertEqual(self.castlingRights.black_castle_long, False)
        self.assertEqual(self.castlingRights.black_castle_short, False)

    def test_get_castling_strings(self):
        self.assertEqual(self.castlingRights.get_castling_string(), "QKqk")

        self.castlingRights.white_castle_long = False
        self.assertEqual(self.castlingRights.get_castling_string(), "Kqk")

        self.castlingRights.white_castle_short = False
        self.assertEqual(self.castlingRights.get_castling_string(), "qk")

        self.castlingRights.black_castle_long = False
        self.assertEqual(self.castlingRights.get_castling_string(), "k")

        self.castlingRights.black_castle_short = False
        self.assertEqual(self.castlingRights.get_castling_string(), "-")

    def test_get_castling_from_string(self):
        self.castlingRights.get_castling_from_string("-")
        self.assertEqual(self.castlingRights.white_castle_long, False)
        self.assertEqual(self.castlingRights.white_castle_short, False)
        self.assertEqual(self.castlingRights.black_castle_long, False)
        self.assertEqual(self.castlingRights.black_castle_short, False)

        self.castlingRights.get_castling_from_string("Q")
        self.assertEqual(self.castlingRights.white_castle_long, True)
        self.assertEqual(self.castlingRights.white_castle_short, False)
        self.assertEqual(self.castlingRights.black_castle_long, False)
        self.assertEqual(self.castlingRights.black_castle_short, False)

        self.castlingRights.get_castling_from_string("K")
        self.assertEqual(self.castlingRights.white_castle_long, False)
        self.assertEqual(self.castlingRights.white_castle_short, True)
        self.assertEqual(self.castlingRights.black_castle_long, False)
        self.assertEqual(self.castlingRights.black_castle_short, False)

        self.castlingRights.get_castling_from_string("q")
        self.assertEqual(self.castlingRights.white_castle_long, False)
        self.assertEqual(self.castlingRights.white_castle_short, False)
        self.assertEqual(self.castlingRights.black_castle_long, True)
        self.assertEqual(self.castlingRights.black_castle_short, False)

        self.castlingRights.get_castling_from_string("k")
        self.assertEqual(self.castlingRights.white_castle_long, False)
        self.assertEqual(self.castlingRights.white_castle_short, False)
        self.assertEqual(self.castlingRights.black_castle_long, False)
        self.assertEqual(self.castlingRights.black_castle_short, True)

        self.castlingRights.get_castling_from_string("QKqk")
        self.assertEqual(self.castlingRights.white_castle_long, True)
        self.assertEqual(self.castlingRights.white_castle_short, True)
        self.assertEqual(self.castlingRights.black_castle_long, True)
        self.assertEqual(self.castlingRights.black_castle_short, True)



