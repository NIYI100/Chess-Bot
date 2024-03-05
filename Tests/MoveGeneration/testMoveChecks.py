import unittest

from Application.BoardModel.chessBoard import BoardState
from Application.MoveGeneration.moveChecks import *

class TestMoveChecks(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()
        self.empty_board = [[EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8,
                            [EMPTY] * 8]
    def test_find_king(self):
        row, col = find_king(self.state)
        self.assertEqual(row, 7)
        self.assertEqual(col, 4)

        self.state.color = "b"
        b_row, b_col = find_king(self.state)
        self.assertEqual(b_row, 0)
        self.assertEqual(b_col, 4)

    def test_check_square_empty(self):
        self.assertTrue(check_if_square_is_empty(self.state, 4, 4))

    def test_check_square_not_empty(self):
        self.assertFalse(check_if_square_is_empty(self.state, 8, 8))

    def test_check_after_move(self):
        self.state.board[7][4] = EMPTY
        self.state.board[4][4] = WHITE_KING
        self.state.board[5][5] = BLACK_BISHOP
        not_check = not_check_after_move(self.state, "a2a3", 4, 4)
        self.assertFalse(not_check)

    def test_not_check_after_move(self):
        self.state.board[7][4] = EMPTY
        self.state.board[4][4] = WHITE_KING
        self.state.board[5][5] = BLACK_ROOK
        not_check = not_check_after_move(self.state, "a2a3", 4, 4)
        self.assertTrue(not_check)

    def test_check_king_in_check_from_knight1(self):
        self.state.board[7][4] = EMPTY
        self.state.board[4][4] = WHITE_KING
        self.state.board[5][6] = BLACK_KNIGHT
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_knight2(self):
        self.state.board[7][4] = EMPTY
        self.state.board[4][4] = WHITE_KING
        self.state.board[6][5] = BLACK_KNIGHT
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_rook1(self):
        self.state.board[7][4] = EMPTY
        self.state.board[4][4] = WHITE_KING
        self.state.board[4][7] = BLACK_ROOK
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_rook2(self):
        self.state.board[7][4] = EMPTY
        self.state.board[4][4] = WHITE_KING
        self.state.board[6][4] = BLACK_ROOK
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_bishop1(self):
        self.state.board = self.empty_board
        self.state.board[4][4] = WHITE_KING
        self.state.board[0][0] = BLACK_BISHOP
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_bishop2(self):
        self.state.board = self.empty_board
        self.state.board[4][4] = WHITE_KING
        self.state.board[7][7] = BLACK_BISHOP
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_bishop3(self):
        self.state.board = self.empty_board
        self.state.board[4][4] = WHITE_KING
        self.state.board[7][1] = BLACK_BISHOP
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_bishop4(self):
        self.state.board = self.empty_board
        self.state.board[4][4] = WHITE_KING
        self.state.board[1][7] = BLACK_BISHOP
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)

    def test_check_king_in_check_from_pawn(self):
        self.state.board[4][4] = WHITE_KING
        self.state.board[3][5] = BLACK_PAWN
        is_check = check_if_king_is_in_check(self.state, 4, 4)
        self.assertTrue(is_check)