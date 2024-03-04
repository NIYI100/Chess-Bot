# This class does all the calculations regarding the zobrist keys that represent the state of the board

from Application.Constants.pieceConstants import *
from Application.TranspositionTable.ZobristKey.ZobristRandomValues import ZobristRandomValues

# Dictionaries used for converting pieces to a corresponding index
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

# Calculates the zobrist_key for a given board
def get_zobrist_key_of_board(state):
    zobrist_values = ZobristRandomValues()
    zobrist_key = 0
    for row in range(8):
        for col in range(8):
            if state.board[row][col] != EMPTY:
                piece_value = pieces_to_value[state.board[row][col].upper()]
                color_value = color_to_value[state.color]
                # General idea for every calculation here:
                # 1. calculate piece_value for first array 0-5, 2. calaculate color 0-1, 3. get the value from the initialized
                # zobrist_values
                zobrist_key ^= zobrist_values.pieces[piece_value][color_value][row][col]

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

    if state.color == COLOR_WHITE:
        zobrist_key ^= zobrist_values.side
    return zobrist_key

# Updates the zobrist key for a given move - zobristKey XOR old_position_of_piece XOR new_position_of_piece
def update_key_for_move(state, old_col, old_row, new_col, new_row):
    if state.board[old_row][old_col] != EMPTY:
        old_piece_value = pieces_to_value[state.board[old_row][old_col].upper()]
        state.zobristKey ^= _get_zobrist_values_entry_for_square(state, old_piece_value, old_row, old_col)
        state.zobristKey ^= _get_zobrist_values_entry_for_square(state, old_piece_value, new_row, new_col)

def update_zobrist_for_castling(state, move: str):
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
    pawn_piece_to_value = 0
    queen_piece_to_value = 5

    state.zobristKey ^= _get_zobrist_values_entry_for_square(state, pawn_piece_to_value, old_row, old_col)
    state.zobristKey ^= _get_zobrist_values_entry_for_square(state, queen_piece_to_value, new_row, new_col)

def _get_zobrist_values_entry_for_square(state, piece_value, row, col):
    zobrist_values = ZobristRandomValues()
    color_value = color_to_value[state.color]
    return zobrist_values.pieces[piece_value][color_value][row][col]

def update_color_in_zobrist_key(state):
    zobrist_values = ZobristRandomValues()
    state.zobristKey ^= zobrist_values.side
