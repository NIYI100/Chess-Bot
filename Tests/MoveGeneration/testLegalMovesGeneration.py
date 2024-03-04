import unittest
from Application.MoveGeneration.legalMovesGeneration import *


class TestLegalMovesGeneration(unittest.TestCase):
    def setUp(self):
        self.state = BoardState()
        self.state.create_initial_board()
        self.empty_board = [[EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8, [EMPTY] * 8,
                            [EMPTY] * 8]

    def test_convert_move_to_long_notation(self):
        old_row, old_col, new_row, new_col = 6, 0, 4, 0
        self.assertEqual(convert_move_to_long_alg_notation(old_row, old_col, new_row, new_col), "a2a4")

    def test_king_moves_every_square_free(self):
        self.state.board = self.empty_board
        self.state.board[6][1] = WHITE_KING
        possible_moves = ["b2b3", "b2c3", "b2c2", "b2c1", "b2b1", "b2a1", "b2a2", "b2a3"]
        actual_advances, _ = king_moves(self.state, 6, 1)
        self.assertEqual(sorted(possible_moves), sorted(actual_advances))
        self.assertEqual(len(_), 0)

    def test_king_moves_every_square_capture(self):
        self.state.board = self.empty_board
        for u in [-1, 1]:
            for v in [-1, 0, 1]:
                self.state.board[6 + u][1 + v] = BLACK_PAWN
        self.state.board[6][1] = WHITE_KING
        possible_captures = ["b2b3", "b2c3", "b2c1", "b2b1", "b2a1", "b2a3"]
        _, actual_captures = king_moves(self.state, 6, 1)
        self.assertEqual(sorted(possible_captures), sorted(actual_captures))
        self.assertEqual(len(_), 0)

    def test_king_moves_some_advances_some_captures(self):
        self.state.board = self.empty_board
        self.state.board[5][1] = BLACK_ROOK
        self.state.board[5][2] = BLACK_BISHOP
        self.state.board[6][1] = WHITE_KING
        possible_advances = ["b2a2", "b2c2", "b2c1"]
        possible_captures = ["b2b3"]
        actual_advances, actual_captures = king_moves(self.state, 6, 1)
        self.assertEqual(sorted(possible_captures), sorted(actual_captures))
        self.assertEqual(sorted(possible_advances), sorted(actual_advances))

    def test_bishop_moves_every_square_empty(self):
        self.state.board = self.empty_board
        self.state.board[4][4] = WHITE_BISHOP
        king_row, king_col = 4, 3
        advances, _ = bishop_moves(self.state, 4, 4, king_row, king_col)
        self.assertEqual(len(advances), 13)

    def test_bishop_moves_captures(self):
        self.state.board = self.empty_board
        self.state.board[4][4] = WHITE_BISHOP
        self.state.board[2][2] = BLACK_PAWN
        self.state.board[6][6] = BLACK_PAWN
        self.state.board[7][1] = BLACK_PAWN
        self.state.board[1][7] = BLACK_PAWN
        king_row, king_col = 4, 3
        advances, captures = bishop_moves(self.state, 4, 4, king_row, king_col)
        self.assertEqual(len(advances), 6)
        self.assertEqual(len(captures), 4)

    def test_knight_moves_every_square_empty(self):
        self.state.board = self.empty_board
        self.state.board[3][4] = WHITE_KNIGHT
        advances = ["e5g4", "e5g6", "e5f7", "e5d7", "e5c6", "e5c4", "e5d3", "e5f3"]
        a, _ = knight_moves(self.state, 3, 4, 4, 3)
        self.assertEqual(sorted(advances), sorted(a))

    def test_knight_moves_some_captures(self):
        self.state.board = self.empty_board
        self.state.board[3][4] = WHITE_KNIGHT
        self.state.board[2][6] = BLACK_PAWN
        self.state.board[4][6] = BLACK_PAWN
        a, b = knight_moves(self.state, 3, 4, 7, 7)
        self.assertEqual(len(a), 6)
        self.assertEqual(len(b), 2)

    def test_rook_moves_every_square_empty(self):
        self.state.board = self.empty_board
        self.state.board[3][4] = WHITE_ROOK
        a, b = rook_moves(self.state,3, 4, 7, 7)
        self.assertEqual(len(a), 14)
        self.assertEqual(len(b), 0)

    def test_rook_moves_some_squares_capture(self):
        self.state.board = self.empty_board
        self.state.board[3][4] = WHITE_ROOK
        self.state.board[3][0] = BLACK_PAWN
        self.state.board[3][7] = BLACK_PAWN
        self.state.board[0][4] = BLACK_PAWN
        self.state.board[7][4] = BLACK_PAWN
        a, b = rook_moves(self.state,3, 4, 7, 7)
        self.assertEqual(len(a), 10)
        self.assertEqual(len(b), 4)

    def test_pawn_move_from_baseline(self):
        a, b = pawn_moves(self.state, 6, 0, 7, 4)
        possible_moves = ["a2a3", "a2a4"]
        self.assertEqual(sorted(a), sorted(possible_moves))
        self.assertEqual(b, [])

    def test_pawn_capture_white(self):
        self.state.board[5][2] = BLACK_PAWN
        self.state.board[5][0] = BLACK_PAWN
        a, b = pawn_moves(self.state, 6, 1, 7, 4)
        self.assertEqual(sorted(a), sorted(["b2b3","b2b4"]))
        self.assertEqual(sorted(b), sorted(["b2a3","b2c3"]))

    def test_pawn_capture_black(self):
        self.state.color = "b"
        self.state.board[5][2] = WHITE_PAWN
        self.state.board[5][0] = WHITE_PAWN
        a, b = pawn_moves(self.state, 4, 1, 0, 4)
        self.assertEqual(sorted(a), sorted(["b4b3"]))
        self.assertEqual(sorted(b), sorted(["b4a3","b4c3"]))

    def test_en_passant_white(self):
        self.state.en_passant = "b6"
        a, b = pawn_moves(self.state, 3, 2, 7, 4)
        self.assertEqual(b, ["c5b6"])

    def test_en_passant_black(self):
        self.state.color = "b"
        self.state.en_passant = "b3"
        a, b = pawn_moves(self.state, 4, 2, 0, 4)
        self.assertEqual(b, ["c4b3"])

    def test_get_legal_moves_white(self):
        a, b = get_legal_moves(self.state)
        self.assertEqual(len(a + b), 20)

    def test_get_legal_moves_black(self):
        self.state.color = "b"
        a, b = get_legal_moves(self.state)
        self.assertEqual(len(a + b), 20)

    def test_king_moves_after_promotion_in_check(self):
        # This is test_promotion_of_white_pawn
        self.state.board = self.empty_board
        self.state.board[0][1] = WHITE_QUEEN
        self.state.board[0][2] = BLACK_KING
        self.state.color = "b"
        self.state.castle_rights.get_castling_from_string("-")

        a, b = get_legal_moves(self.state)
        self.assertEqual(a, ["c8b8"])
        self.assertEqual(b, ["c8d7"])

    def test_get_castling_moves_no_castling_white(self):
        state = BoardState()
        state.create_initial_board()
        self.assertEqual(get_castling_moves(state), [])

    def test_get_castling_moves_no_castling_black(self):
        state = BoardState()
        state.create_initial_board()
        state.color = "b"
        self.assertEqual(get_castling_moves(state), [])

    def test_get_castling_moves_white_short(self):
        state = BoardState()
        state.create_initial_board()
        state.board[7][5] = EMPTY
        state.board[7][6] = EMPTY
        self.assertEqual(get_castling_moves(state), ["e1g1"])

    def test_get_castling_moves_white_long(self):
        state = BoardState()
        state.create_initial_board()
        state.board[7][3] = EMPTY
        state.board[7][2] = EMPTY
        state.board[7][1] = EMPTY
        self.assertEqual(get_castling_moves(state), ["e1b1"])

    def test_get_castling_moves_black_short(self):
        state = BoardState()
        state.create_initial_board()
        state.color = "b"
        state.board[0][5] = EMPTY
        state.board[0][6] = EMPTY
        self.assertEqual(get_castling_moves(state), ["e8g8"])

    def test_get_castling_moves_black_long(self):
        state = BoardState()
        state.create_initial_board()
        state.color = "b"
        state.board[0][3] = EMPTY
        state.board[0][2] = EMPTY
        state.board[0][1] = EMPTY
        self.assertEqual(get_castling_moves(state), ["e8b8"])