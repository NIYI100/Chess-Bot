# Conversion of a chessboard to a fen string and the other way around

from Application.Constants.pieceConstants import *
from Application.TranspositionTable.ZobristKey.ZobristKeyCalculations import get_zobrist_key_of_board


def set_fen_to_board(fen: str, state):
    """
    Sets a fen to its corresponding BoardState
    """
    fen_array = fen.split(" ")
    state.board = get_piece_placement_from_fen(fen_array[0])
    state.color = fen_array[1]
    state.castle_rights.get_castling_from_string(fen_array[2])
    state.en_passant = fen_array[3]
    state.halfmoves = int(fen_array[4])
    state.fullmoves = int(fen_array[5])
    state.zobristKey = get_zobrist_key_of_board(state)


# Helper method to create the BoardState object from the FEN string
def get_piece_placement_from_fen(boardFEN) -> list[list[str]]:
    """
    returns the piece placement for the BoardState
    """
    rows = boardFEN.split("/")
    piecePlacement = []
    for row in rows:
        rowArray = []
        for char in row:
            rowArray.extend(["."] * int(char)) if char.isdigit() else rowArray.append(char)
        piecePlacement.append(rowArray)
    return piecePlacement


def board_to_fen(state) -> str:
    """
    Converts a BoardState to the corresponding FEN string
    """
    fen_string = ""
    for row in range(8):
        row_string = ""
        empty_spaces = 0
        for column in range(8):
            if state.board[row][column] == EMPTY:
                empty_spaces += 1
            else:
                if empty_spaces != 0:
                    row_string += str(empty_spaces)
                    empty_spaces = 0
                row_string += state.board[row][column]
        if empty_spaces != 0:
            row_string += str(empty_spaces)
        row_string += "/"
        fen_string += row_string
    fen_string = fen_string[:-1]

    fen_string += " "
    fen_string += state.color

    fen_string += " "
    fen_string += state.castle_rights.get_castling_string()

    fen_string += " "
    fen_string += state.en_passant

    fen_string += " "
    fen_string += str(state.halfmoves)

    fen_string += " "
    fen_string += str(state.fullmoves)
    return fen_string
