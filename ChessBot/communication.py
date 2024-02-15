# Disclaimer: As it is in wip this is veryx close to the https://github.com/healeycodes/andoma/blob/main/communication.py
# Over the time it will be rewritten and expanded
# UCI uses print for communication

from ChessBot.TranspositionTable.ZobristKey.ZobristRandomValues import ZobristRandomValues

# Ensure the logger is set up (this should be done once at the start of your program)
import argparse
import sys

from ChessBot.BoardModel import chessBoard
from ChessBot.BoardModel.boardConversion import set_fen_to_board
from ChessBot.MoveGeneration.bestMoveGeneration import calculate_best_move


def talk():
    state = chessBoard.BoardState()
    ZOBRIST_RANDOM_VALUES = ZobristRandomValues()
    depth = get_depth()

    while True:
        msg = input()
        command(depth, state, msg, ZOBRIST_RANDOM_VALUES)


def command(depth, state, msg, zobrist_random_values):
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
            state.create_initial_board(zobrist_random_values)
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
            state.execute_move_on_board(move)

    if msg[0:2] == "go":
        _move = calculate_best_move(depth, state, zobrist_random_values)
        print("bestmove ", _move)
        return


def get_depth():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", default=3, help="Provide an integer (default: 3)")
    args = parser.parse_args()
    return max([1, int(args.depth)])
