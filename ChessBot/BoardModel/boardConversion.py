# Conversion of a chessboard to a fen string and the other way around

from ChessBot.BoardModel.chessBoard import BoardState
from ChessBot.Constants.pieceConstants import *
from ChessBot.MoveGeneration.castling import black_castle_long, black_castle_short, white_castle_short, \
    white_castle_long

# Not used right now
white_kingside_castle_rights = True
white_queenside_castle_rights = True
black_kingside_castle_rights = True
black_queenside_castle_rights = True


# Takes a FEN String and converts it to a BoardState object
def fen_to_board(fen):
    fen_array = fen.split(" ")

    board = get_piece_placement_from_fen(fen_array[0])
    color = fen_array[1]
    castle_rights = fen_array[2]
    en_passant = fen_array[3]
    halfmoves = fen_array[4]
    fullmoves = fen_array[5]

    return BoardState(board, color, castle_rights, en_passant, halfmoves, fullmoves)


# sets the board to the position defined in a FEN string
def set_fen_to_board(fen, board):
    fen_array = fen.split(" ")
    board.board = get_piece_placement_from_fen(fen_array[0])
    board.color = fen_array[1]
    board.castle_rights = fen_array[2]
    board.en_passant = fen_array[3]
    board.halfmoves = fen_array[4]
    board.fullmoves = fen_array[5]


# Helper method to create the BoardState object from the FEN string
def get_piece_placement_from_fen(boardFEN):
    rows = boardFEN.split("/")
    piecePlacement = []
    for row in rows:
        rowArray = []
        for char in row:
            rowArray.extend(["."] * int(char)) if char.isdigit() else rowArray.append(char)
        piecePlacement.append(rowArray)
    return piecePlacement


# Takes a board state and converts it to the FEN String representation
def board_to_fen(state):
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
    fen_string += COLOR_BLACK if state.color == COLOR_WHITE else COLOR_WHITE

    fen_string += " "
    fen_string += get_castleing_rights()

    # TODO Implement enPassant
    fen_string += " "
    fen_string += state.en_passant

    # TODO Implement halfmoves / End on 100 halfmoves
    fen_string += " "
    fen_string += state.halfmoves

    fen_string += " "
    fen_string += state.fullmoves if state.color == COLOR_WHITE else str(int(state.fullmoves) + 1)
    return fen_string


def get_castleing_rights():
    castling_string = ""
    if white_castle_long:
        castling_string += "Q"
    if white_castle_long:
        castling_string += "K"
    if black_castle_long:
        castling_string += "q"
    if black_castle_short:
        castling_string += "k"
    if castling_string == "":
        castling_string = "-"
    return castling_string
