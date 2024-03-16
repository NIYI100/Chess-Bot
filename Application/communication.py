# Mainly taken from: https://github.com/healeycodes/andoma/blob/main/communication.py (access: 05.03.2024)
from Application.BoardModel.chessBoard import BoardState
import argparse
import sys
from Application.BoardModel.boardConversion import set_fen_to_board
from Application.MoveGeneration.bestMoveGeneration import iterative_deepening
clean_transposition_table = 0

def talk():
    """
    The main loop of the uci interface. Will listen to inputs and execute the corresponding actions
    """
    state = BoardState()
    max_depth = get_depth()
    time_to_run = get_time_to_run()

    while True:
        msg = input()
        command(max_depth, time_to_run, state, msg)


def command(max_depth, time_to_run, state, msg):
    """
    Executes the command defined in msg if its a known command
    :param max_depth: The maximium depth of the search
    :param time_to_run: The maximum time to run the search
    :param state: The BoardState
    :param msg: The command
    """
    msg = msg.strip()
    tokens = msg.split(" ")
    while "" in tokens:
        tokens.remove("")


    match msg:
        case "quit":
            sys.exit()

        case "uci":
            print("id name myownchessengine")
            print("id author Sven Ambrosius")
            print("uciok")
            return

        case "isready":
            print("readyok")
            return

        case "ucinewgame":
            return

    if tokens[0] == "position":
        if len(tokens) < 2:
            return

        if tokens[1] == "startpos":
            state.create_initial_board()
            moves_start = 2
        elif tokens[1] == "fen":
            fen = " ".join(tokens[2:8])
            set_fen_to_board(fen, state)
            moves_start = 8
        else:
            return

        if len(tokens) <= moves_start or tokens[moves_start] != "moves":
            return

        for move in tokens[(moves_start + 1):]:
            state.execute_move(move)

    if msg[0:2] == "go":
        global clean_transposition_table
        _move = iterative_deepening(max_depth, state, time_to_run)
        if clean_transposition_table == 10:
            clean_transposition_table = 0
        else:
            clean_transposition_table += 1
        print("bestmove ", _move)
        return


def get_depth():
    """
    Returns the depth the engine should search for in the calculation of the best move.
    The default depth is 10
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", default=4, help="Provide an integer (default: 10)")
    args = parser.parse_args()
    return max([1, int(args.depth)])

def get_time_to_run():
    """
    Returns the maximum time the engine should search for in the calculation of the best move.
    The default time is 4.5s
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=float, default=50, help="Provide an float (default: 4.5)")
    args = parser.parse_args()
    return max([1.0, float(args.time)])