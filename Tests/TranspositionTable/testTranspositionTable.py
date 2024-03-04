import unittest

from Application.BoardModel.chessBoard import BoardState
from Application.TranspositionTable.TranspostionTable import *


class TestTranspositionTable(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()
        TranspositionTable().reset_transposition_table()
        self.transposition_table = TranspositionTable().get_transposition_table()
        self.index = self.state.zobristKey % len(self.transposition_table)
    def test_create_entry_in_empty_table(self):
        create_entry_in_transpos_table_if_better(self.state, 2, HASH_EXACT, 50)
        self.assertIsNotNone(self.transposition_table[self.index])
        self.assertIsNone(self.transposition_table[self.index + 1])

    def test_skip_create_if_entry_has_higher_depth(self):
        create_entry_in_transpos_table_if_better(self.state, 2, HASH_EXACT, 50)
        create_entry_in_transpos_table_if_better(self.state, 1, HASH_BETA, 40)

        saved_depth = self.transposition_table[self.index].depth
        saved_flag = self.transposition_table[self.index].flag
        saved_evaluation = self.transposition_table[self.index].evaluation
        self.assertEqual(saved_depth, 2)
        self.assertEqual(saved_flag, HASH_EXACT)
        self.assertEqual(saved_evaluation, 50)

    def test_create_if_entry_has_lower_depth(self):
        create_entry_in_transpos_table_if_better(self.state, 1, HASH_EXACT, 50)
        create_entry_in_transpos_table_if_better(self.state, 5, HASH_BETA, 40)

        saved_depth = self.transposition_table[self.index].depth
        saved_flag = self.transposition_table[self.index].flag
        saved_evaluation = self.transposition_table[self.index].evaluation
        self.assertEqual(saved_depth, 5)
        self.assertEqual(saved_flag, HASH_BETA)
        self.assertEqual(saved_evaluation, 40)

    def test_check_if_transpos_table_is_useable_empty(self):
        self.assertFalse(check_transpos_table_if_useable(self.state, 1, 5, 5))

    def test_check_if_transpos_table_is_useable_HASH_EXACT_useable(self):
        create_entry_in_transpos_table_if_better(self.state, 10, HASH_EXACT, 100)
        self.assertTrue(check_transpos_table_if_useable(self.state, 4, 10, 10))

    def test_check_if_transpos_table_is_useable_HASH_BETA_useable(self):
        create_entry_in_transpos_table_if_better(self.state, 10, HASH_BETA, 100)
        self.assertTrue(check_transpos_table_if_useable(self.state, 4, 10, 10))

    def test_check_if_transpos_table_is_useable_HASH_BETA_unuseable(self):
        create_entry_in_transpos_table_if_better(self.state, 10, HASH_BETA, 100)
        self.assertFalse(check_transpos_table_if_useable(self.state, 4, 10, 110))

    def test_check_if_transpos_table_is_useable_HASH_ALPHA_useable(self):
        create_entry_in_transpos_table_if_better(self.state, 10, HASH_ALPHA, 100)
        self.assertTrue(check_transpos_table_if_useable(self.state, 4, 110, 10))

    def test_check_if_transpos_table_is_useable_HASH_ALPHA_unuseable(self):
        create_entry_in_transpos_table_if_better(self.state, 10, HASH_ALPHA, 100)
        self.assertFalse(check_transpos_table_if_useable(self.state, 4, 10, 110))

    def test_get_eval_of_transposition_table(self):
        create_entry_in_transpos_table_if_better(self.state, 10, HASH_ALPHA, 100)
        self.assertEqual(get_eval_of_transpos_table(self.state), 100)

    def test_sort_for_transpos_table_for_color_white(self):
        self.state.push("a2a4")
        self.transposition_table[self.state.zobristKey % len(self.transposition_table)] = HashEntry(self.state.zobristKey, 3, HASH_EXACT, 110, "w")
        self.state.pop()

        self.state.push("b2b4")
        self.transposition_table[self.state.zobristKey % len(self.transposition_table)] = HashEntry(self.state.zobristKey, 3, HASH_EXACT, 500, "w")
        self.state.pop()

        moves = ["a2a4", "b2b4", "c2c4"]
        sorted_moves = sort_for_transpos_table(self.state, moves)
        self.assertEqual(sorted_moves, ["b2b4", "a2a4", "c2c4"])


    def test_sort_for_transpos_table_for_color_black(self):
        self.state.switch_color()

        self.state.push("a2a4")
        self.transposition_table[self.state.zobristKey % len(self.transposition_table)] = HashEntry(self.state.zobristKey, 3, HASH_EXACT, 110, "w")
        self.state.pop()

        self.state.push("b2b4")
        self.transposition_table[self.state.zobristKey % len(self.transposition_table)] = HashEntry(self.state.zobristKey, 3, HASH_EXACT, 500, "w")
        self.state.pop()

        moves = ["b2b4", "c2c4", "a2a4"]
        sorted_moves = sort_for_transpos_table(self.state, moves)
        self.assertEqual(sorted_moves, ["c2c4", "a2a4", "b2b4"])