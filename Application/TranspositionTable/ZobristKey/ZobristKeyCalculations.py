# This class does all the calculations regarding the zobrist keys that represent the state of the board

from Application.Constants.pieceConstants import *
from Application.TranspositionTable.TranspostionTable import TranspositionTable
from Application.TranspositionTable.ZobristKey.ZobristRandomValues import ZobristRandomValues

"""
Dictionaries used for converting pieces to a corresponding index
"""
pieces_to_value = {
    "P": 0,
    "R": 1,
    "B": 2,
    "N": 3,
    "K": 4,
    "Q": 5
}
color_to_value = {
    "w": 0,
    "b": 1
}
castling_to_value = {
    "": 0,
    "Q": 1,
    "K": 2,
    "QK": 3
}

def get_zobrist_key_of_board(state):
    """
    Calculates the zobrist key for a given state by xoring the values of the corresponding state zobrist values.
    :param state: The BoardState
    :return:
    """
    zobrist_values = ZobristRandomValues()
    zobrist_key = 0

    #Zobrist key calculation for the board
    for row in range(8):
        for col in range(8):
            if state.board[row][col] != EMPTY:
                piece_value = pieces_to_value[state.board[row][col].upper()]
                color_value = color_to_value[state.color]
                zobrist_key ^= zobrist_values.pieces[piece_value][color_value][row][col]

    # Zobrist key calculation for the castling rights
    w_castling_rights_value = 0
    b_castling_rights_value = 0
    if state.castle_rights.white_castle_long:
        w_castling_rights_value += 1
    if state.castle_rights.white_castle_short:
        w_castling_rights_value += 2

    if state.castle_rights.black_castle_long:
        b_castling_rights_value += 1
    if state.castle_rights.black_castle_short:
        b_castling_rights_value += 2

    zobrist_key ^= zobrist_values.w_castling_right[w_castling_rights_value]
    zobrist_key ^= zobrist_values.b_castling_right[b_castling_rights_value]

    # Zobrist key calculation for the color
    if state.color == COLOR_WHITE:
        zobrist_key ^= zobrist_values.side
    return zobrist_key

def update_key_for_move(state, old_col, old_row, new_col, new_row):
    """
    Updates the zobrist key for a given move
    :param state: The BoardState
    :param old_col: The old column
    :param old_row: The old row
    :param new_col: The new column
    :param new_row: The new row
    """
    if state.board[old_row][old_col] != EMPTY:
        old_piece_value = pieces_to_value[state.board[old_row][old_col].upper()]
        state.zobristKey ^= _get_zobrist_values_entry_for_square(state, old_piece_value, old_row, old_col)
        state.zobristKey ^= _get_zobrist_values_entry_for_square(state, old_piece_value, new_row, new_col)

def update_zobrist_for_castling(state, move: str):
    """
    Updates the zobrist key for a castling move
    :param state: The BoardState
    :param move: The castling move
    """
    match move:
        case "e1b1":
            update_key_for_move(state, 7, 0, 7, 2)
            update_key_for_move(state, 7, 3, 7, 1)
        case "e1g1":
            update_key_for_move(state, 7, 7, 7, 5)
            update_key_for_move(state, 7, 3, 7, 6)
        case "e8b8":
            update_key_for_move(state, 0, 0, 0, 2)
            update_key_for_move(state, 0, 3, 0, 1)
        case "e8g8":
            update_key_for_move(state, 0, 7, 0, 5)
            update_key_for_move(state, 0, 3, 0, 6)

def update_zobrist_for_promotion(state, old_row, old_col, new_row, new_col):
    """
    Updates the zobrist key for a promotion of a pawn to a queen
    :param state: The BoardState
    :param old_col: The old column
    :param old_row: The old row
    :param new_col: The new column
    :param new_row: The new row
    """
    pawn_piece_to_value = 0
    queen_piece_to_value = 5

    state.zobristKey ^= _get_zobrist_values_entry_for_square(state, pawn_piece_to_value, old_row, old_col)
    state.zobristKey ^= _get_zobrist_values_entry_for_square(state, queen_piece_to_value, new_row, new_col)

    TranspositionTable().delete_entry(TranspositionTable().get_index(state.zobristKey))

def _get_zobrist_values_entry_for_square(state, piece_value, row, col):
    """
    Get the zobrist value corresponding to the given piece.
    :param state: The BoardState
    :param piece_value: The value of the piece for the dictionary
    :param row: The row
    :param col: The column
    """
    zobrist_values = ZobristRandomValues()
    color_value = color_to_value[state.color]
    return zobrist_values.pieces[piece_value][color_value][row][col]

def update_color_in_zobrist_key(state):
    """
    Update the zobrist key to the other color
    :param state: The BoardState
    """
    zobrist_values = ZobristRandomValues()
    state.zobristKey ^= zobrist_values.side
