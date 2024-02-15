# This class does all the calculations regarding the zobrist keys that represent the state of the board

from Constants.pieceConstants import *

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
def get_zobrist_key_of_board(state, zobrist_values):
    zobrist_key = 0
    for x in range(8):
        for y in range(8):
            if state.board[x][y] != EMPTY:
                piece_value = pieces_to_value[state.board[x][y].upper()]
                color_value = color_to_value[state.color]
                # General idea for every calculation here:
                # 1. calculate piece_value for first array 0-5, 2. calaculate color 0-1, 3. get the value from the initialized
                # zobrist_values
                zobrist_key ^= zobrist_values.pieces[piece_value][color_value][x][y]

    # TODO - This isnt right I think
    if state.castle_rights == "-":
        w_castling_rights_value = 0
        b_castling_rights_value = 0
    else:
        w_castling_rights_value = castling_to_value["" . join(s for s in state.castle_rights if s.isupper())]
        b_castling_rights_value = castling_to_value[("".join(s for s in state.castle_rights if s.islower())).upper()]
    zobrist_key ^= zobrist_values.w_castling_rights[w_castling_rights_value]
    zobrist_key ^= zobrist_values.b_castling_rights[b_castling_rights_value]

    # TODO Enpassant

    if state.color == COLOR_WHITE:
        zobrist_key ^= zobrist_values.side
    return zobrist_key

# Updates the zobrist key for a given move - zobristKey XOR old_position_of_piece XOR new_position_of_piece
def update_key_for_move(state, old_x, old_y, new_x, new_y, zobrist_values):
    if state.board[old_y][old_x] != EMPTY:
        old_piece_value = pieces_to_value[state.board[old_y][old_x].upper()]
        state.zobristKey ^= _get_zobrist_values_entry_for_square(state, old_piece_value, old_y, old_x, zobrist_values)
        state.zobristKey ^= _get_zobrist_values_entry_for_square(state, old_piece_value, new_y, new_x, zobrist_values)

def _get_zobrist_values_entry_for_square(state, piece_value, y, x, zobrist_values):
    color_value = color_to_value[state.color]
    return zobrist_values.pieces[piece_value][color_value][y][x]

def update_color_in_zobrist_key(state, zobrist_values):
    state.zobristKey ^= zobrist_values.side
