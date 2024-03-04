import unittest

from Application.BoardModel.chessBoard import BoardState
from Application.Constants.pieceConstants import WHITE_PAWN
from Application.TranspositionTable.ZobristKey.ZobristKeyCalculations import update_key_for_move


class TestZobristKeyCalculations(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()

        self.state2 = BoardState()
        self.state2.create_initial_board()

    def test_get_zobrist_key_of_board(self):
        self.assertEqual(self.state.zobristKey, self.state2.zobristKey)

    def test_key_identical_after_move(self):
        old_col, old_row, new_col, new_row = 0, 6, 0, 4
        update_key_for_move(self.state, old_col, old_row, new_col, new_row)
        update_key_for_move(self.state2, old_col, old_row, new_col, new_row)
        self.assertEqual(self.state.zobristKey, self.state2.zobristKey)

    def test_key_identical_after_rewinding_move(self):
        old_zobristKey = self.state.zobristKey
        old_col, old_row, new_col, new_row = 0, 6, 0, 4
        update_key_for_move(self.state, old_col, old_row, new_col, new_row)
        self.assertNotEquals(old_zobristKey, self.state.zobristKey)

        self.state.board[4][0] = WHITE_PAWN
        update_key_for_move(self.state, new_col, new_row, old_col, old_row)
        self.assertEqual(old_zobristKey, self.state.zobristKey)
