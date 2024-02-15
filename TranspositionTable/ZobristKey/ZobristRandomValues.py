# A Zobrist Key is a 64bit number that is calculated by XORing different values. In the case of chess this is
# an number for the piece / position, the white and black castling rights, enPassant rights and the side to play

import random
class ZobristRandomValues:
    def __init__(self):
        self.pieces, self.w_castling_rights, self.b_castling_rights, self.en_passant, self.side = self._generate_initial_zobrist_key()

    def _generate_initial_zobrist_key(self):
        # [6 - piece type][2 - side to play][8 - xAxis][8 - yAxis]
        pieces = [[[[random.getrandbits(64) for _ in range(8)]
                    for _ in range(8)]
                   for _ in range(2)]
                  for _ in range(6)]  # Piece_type / Side_to_move / Squares
        # [4 - as there are 4 possibilities ( -,Q,K,QK]
        w_castling_right = [random.getrandbits(64) for _ in range(4)]
        # [4 - as there are 4 possibilities ( -,q,k,qk]
        b_castling_right = [random.getrandbits(64) for _ in range(4)]
        # [8][8] - enPassant for every square (It is only possible for 16 squares but still works)
        en_passant = [[random.getrandbits(64) for _ in range(8)]
                      for _ in range(8)]
        # 64bit - side to play
        side = random.getrandbits(64)

        return pieces, w_castling_right, b_castling_right, en_passant, side
