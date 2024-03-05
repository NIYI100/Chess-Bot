import unittest

from Application.TranspositionTable.ZobristKey.ZobristRandomValues import ZobristRandomValues


class TestZobristRandomValues(unittest.TestCase):
    def setUp(self):
        self.zobrist = ZobristRandomValues()

    def test_singleton(self):
        newZobrist = ZobristRandomValues()
        self.assertEqual(self.zobrist, newZobrist)
