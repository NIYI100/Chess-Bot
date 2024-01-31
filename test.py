import unittest

import ChessBot.legalMovesGeneration as main
from ChessBot.chessBoard import BoardState
from ChessBot.pieceConstants import *


class TestChessBot(unittest.TestCase):
    def setUp(self):
        board = [
            [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK],
            [WHITE_PAWN] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [EMPTY] * 8,
            [BLACK_PAWN] * 8,
            [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
        ]
        self.state = BoardState(board, "w", "-", "-", "0", "0")

