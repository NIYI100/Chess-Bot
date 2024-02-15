white_castle_short = True
white_castle_long = True
black_castle_short = True
black_castle_long = True
def update_castling_rights(move):
    old_x = ord(move[0]) - 97
    old_y = 8 - int(move[1])
    global white_castle_long, white_castle_short, black_castle_long, black_castle_short

    if old_y == 0:
        if old_x == 4:
            white_castle_long = False
            white_castle_short = False
        if old_x == 0:
            white_castle_long = False
        if old_x == 7:
            white_castle_short = False

    if old_y == 7:
        if old_x == 4:
            black_castle_long = False
            black_castle_short = False
        if old_x == 0:
            black_castle_long = False
        if old_x == 7:
            black_castle_short = False

