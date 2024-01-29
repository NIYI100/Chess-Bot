# Disclaimer: As it is in wip this is veryx close to the https://github.com/healeycodes/andoma/blob/main/communication.py
# Over the time it will be rewritten and expanded
# UCI uses print for communication

import argparse
import sys

import chessBoard
from boardConversion import set_fen_to_board
from bestMoveGeneration import calculateMove

def talk():
    board = chessBoard.BoardState()
    depth = get_depth()

    while True:
        msg = input()
        command(depth, board, msg)


def command(depth, board, msg):
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

        case "position":
            if len(tokens) < 2:
                return

            if tokens[1] == "startpos":
                board.create_initial_board()
                moves_start = 2
            elif tokens[1] == "fen":
                fen = " ".join(tokens[2:8])
                set_fen_to_board(fen, board)
                moves_start = 8
            else:
                return

            if len(tokens) <= moves_start or tokens[moves_start] != "moves":
                return

            for move in tokens[(moves_start + 1):]:
                board.execute_move(move)

    if msg[0:2] == "go":
        _move = calculateMove(depth, board)
        print("bestmove ", _move)
        return


def get_depth():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", default=3, help="Provide an integer (default: 3)")
    args = parser.parse_args()
    return max([1, int(args.depth)])