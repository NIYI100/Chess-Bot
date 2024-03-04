import unittest
from unittest.mock import patch

import Application.communication
from Application.communication import *


class TestCommunication(unittest.TestCase):
    def test_get_depth(self):
        self.assertEqual(get_depth(), 10)

    def test_get_time_to_run(self):
        self.assertEqual(get_time_to_run(), 4.5)


    @patch('Application.communication.print')
    def test_uci_command(self, mock_print):
        state = BoardState()
        command(0, 1.0, state, "uci")  # Assuming your command returns something for verification
        self.assertEqual(mock_print.call_count, 3)

        # Verify each call to print.
        calls = [call[0][0] for call in mock_print.call_args_list]  # Extracts print arguments
        expected_calls = [
            "id name myownchessengine",
            "id author Sven Ambrosius",
            "uciok"
        ]

        self.assertEqual(calls, expected_calls)

    @patch('Application.communication.sys.exit')
    def test_quit(self, mock_exit):
        state = BoardState()
        command(0,1.0,  state, "quit")
        mock_exit.assert_called()

    @patch('Application.communication.print')
    def test_isready(self, mock_print):
        state = BoardState()
        command(0, 1.0, state, "isready")
        printed_lines = [call_args[0][0] for call_args in mock_print.call_args_list]
        self.assertEqual(printed_lines, ["readyok"])

    @patch('Application.communication.print')
    def test_ucinewgame(self, mock_print):
        state = BoardState()
        command(0, 1.0, state, "ucinewgame")
        printed_lines = [call_args[0][0] for call_args in mock_print.call_args_list]
        self.assertEqual(printed_lines, [])

    @patch('Application.communication.print')
    def test_position_len_not_2(self, mock_print):
        state = BoardState()
        command(0, 1.0, state, "position ")
        printed_lines = [call_args[0][0] for call_args in mock_print.call_args_list]
        self.assertEqual(printed_lines, [])

    def test_position_startpos(self):
        state = BoardState()
        command(0, 1.0, state, "position startpos")
        newBoard = BoardState()
        newBoard.create_initial_board()
        self.assertEqual(state, newBoard)

    def test_position_fen(self):
        state = BoardState()
        command(0, 1.0, state, "position fen rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        newBoard = BoardState()
        newBoard.create_initial_board()
        self.assertEqual(state, newBoard)

    @patch('Application.communication.print')
    def test_position_nothing(self, mock_print):
        state = BoardState()
        command(0, 1.0, state, "position    dfwfwe")
        printed_lines = [call_args[0][0] for call_args in mock_print.call_args_list]
        self.assertEqual(printed_lines, [])

    def test_position_moves_a2a4_a7a5(self):
        state = BoardState()
        command(0, 1.0, state, "position startpos moves a2a4 a7a5")

        newState = BoardState()
        newState.create_initial_board()
        newState.execute_move("a2a4")
        newState.execute_move("a7a5")
        self.assertEqual(state, newState)

    @patch('Application.communication.print')
    def test_go(self, mock_print):
        state = BoardState()
        state.create_initial_board()
        command(2, 1.0, state, "go")

        first_call = mock_print.call_args_list[0]
        bestmove = first_call[0][0]
        move = first_call[0][1]
        self.assertEqual(bestmove + move, "bestmove " + move)

    #@patch('builtins.input', side_effect=["quit"])
    #@patch('sys.exit')
    #def test_talk(self, mock_exit, mock_input):
    #    talk()
    #    mock_exit.assert_called_once()
