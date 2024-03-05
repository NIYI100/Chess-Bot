import unittest

from Application.BoardModel.boardConversion import set_fen_to_board
from Application.Constants.pieceConstants import *
from Application.MoveGeneration.bestMoveGeneration import *

class TestMoveGeneration(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()
        TranspositionTable()._transpositionTable = [None] * 1048583

    def test_evaluate_position_white(self):
        self.state.board[6][3] = EMPTY
        self.state.board[4][3] = WHITE_PAWN
        self.assertEqual(evaluate_position(self.state), 40)

    def test_evaluate_position_black(self):
        self.state.color = "b"
        self.state.board[6][3] = EMPTY
        self.state.board[4][3] = WHITE_PAWN
        self.assertEqual(evaluate_position(self.state), -40)

    def test_nega_max_depth_0(self):
        self.state.execute_move("d2d4")
        self.state.execute_move("a7a5")
        evaluation = nega_max(0, self.state, 0, 0)
        self.assertEqual(evaluation, 0)

    def test_nega_max_transposition_table(self):
        self.state.execute_move("d2d4")
        self.state.execute_move("a7a5")
        create_entry_in_transpos_table_if_better(self.state, 5, HASH_EXACT, 55)

        evaluation = nega_max(0, self.state, 0, 0)
        self.assertEqual(evaluation, 55)

    def test_nega_max_depth_2(self):
        self.state.execute_move("d2d4")
        self.state.execute_move("a7a5")
        evaluation = - nega_max(2, self.state, -math.inf, math.inf)
        self.assertEqual(evaluation, -45)

    def test_nega_max_alpha_isbigger(self):
        self.state.execute_move("d2d4")
        self.state.execute_move("a7a6")
        evaluation = - nega_max(1, self.state, 5000, math.inf)
        self.assertEqual(evaluation, -5000)

    def test_no_possible_moves(self):
        self.state.board = [[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8]
        self.state.board[0][0] = WHITE_KING
        self.state.board[1][1] = BLACK_QUEEN
        self.state.board[1][2] = BLACK_ROOK
        self.state.castle_rights.get_castling_from_string("-")
        evaluation = nega_max(1, self.state, 0, 0)
        self.assertEqual(evaluation, -math.inf)

    def test_calculate_best_move(self):
        move = calculate_best_move(1, self.state)
        self.assertIsNotNone(move)

    def test_iterative_deepening(self):
        move = iterative_deepening(1, self.state, 2.0)
        self.assertIsNotNone(move)

    def test_cancelation_of_nega_max_if_checkmate(self):
        self.state.board = [[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8]
        self.state.board[2][2] = WHITE_KING
        self.state.board[2][1] = WHITE_ROOK
        self.state.board[1][0] = BLACK_KING

        eval = nega_max(7, self.state, math.inf, - math.inf)
        self.assertEqual(eval, math.inf)

    def test_stalemate(self):
        self.state.board = [[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8,[EMPTY] * 8]
        self.state.board[0][0] = BLACK_KING
        self.state.board[2][1] = WHITE_QUEEN
        self.state.board[3][2] = WHITE_QUEEN
        self.state.color = "b"
        evaluation = nega_max(1, self.state, - math.inf, math.inf)
        self.assertEqual(evaluation, 0)

    def test_negaMax_with_LMR(self):
        evaluation = nega_max(3, self.state, - math.inf, math.inf)
        self.assertEqual(evaluation, 20)