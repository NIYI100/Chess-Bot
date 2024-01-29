from ChessBot.chessBoard import BoardState
from pieceConstants import *

white_kingside_castle_rights = True
white_queenside_castle_rights = True
black_kingside_castle_rights = True
black_queenside_castle_rights = True

# Takes a FEN String and converts it to a BoardState object
def fen_to_board(fen):
    fen_array = fen.split(" ")
    board = get_piece_placement_from_fen(fen_array[0])

    color = fen_array[1]

    castleRights = fen_array[2]

    enPassant = fen_array[3]

    halfmoves = fen_array[4]

    fullmoves = fen_array[5]

    return BoardState(board, color, castleRights, enPassant, halfmoves, fullmoves)

# sets the board to the position defined in a FEN string
def set_fen_to_board(fen, board):
    fen_array = fen.split(" ")
    board.board = get_piece_placement_from_fen(fen_array[0])

    board.color = fen_array[1]

    board.castleRights = fen_array[2]

    board.enPassant = fen_array[3]

    board.halfmoves = fen_array[4]

    board.fullmoves = fen_array[5]

    return



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

# Takes a board state and converts it to the FEN String representation to feed to the GUI
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
    fen_string += state.enPassant

    # TODO Implement halfmoves / End on 100 halfmoves
    fen_string += " "
    fen_string += state.halfmoves

    fen_string += " "
    fen_string += state.fullmoves if state.color == COLOR_WHITE else str(int(state.fullmoves) + 1)
    return fen_string

def get_castleing_rights():
    # TODO - For the chosen best move we do a execute_move(state, move) method where we will check if a king or rook have moved -> castleing rights gone
    return