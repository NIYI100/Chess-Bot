# Disclaimer: As it is in wip this is veryx close to the https://github.com/healeycodes/andoma/blob/main/communication.py
# Over the time it will be rewritten and expanded
# UCI uses print for communication
from Application.BoardModel.chessBoard import BoardState

# Ensure the logger is set up (this should be done once at the start of your program)
import argparse
import sys

from Application.BoardModel.boardConversion import set_fen_to_board
from Application.MoveGeneration.bestMoveGeneration import iterative_deepening


def talk():
    state = BoardState()
    max_depth = get_depth()
    time_to_run = get_time_to_run()

    while True:
        msg = input()
        command(max_depth, time_to_run, state, msg)


def command(max_depth, time_to_run, state, msg):
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
        _move = iterative_deepening(max_depth, state, time_to_run)
        print("bestmove ", _move)
        return


def get_depth():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", default=10, help="Provide an integer (default: 10)")
    args = parser.parse_args()
    return max([1, int(args.depth)])

def get_time_to_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time", type=float, default=4.5, help="Provide an float (default: 4.5)")
    args = parser.parse_args()
    return max([1.0, float(args.time)])