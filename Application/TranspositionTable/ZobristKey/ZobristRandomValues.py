# A Zobrist Key is a 64bit number that is calculated by XORing different values. In the case of chess this is
# an number for the piece / position, the white and black castling rights, enPassant rights and the side to play

import random
from enum import Enum


class ZobristRandomValues:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ZobristRandomValues, cls).__new__(cls)
            cls._generate_initial_zobrist_key()
        return cls._instance

    @classmethod
    def _generate_initial_zobrist_key(cls):
        # [6 - piece type][2 - side to play][8 - xAxis][8 - yAxis]
        cls.pieces = [[[[random.getrandbits(64) for _ in range(8)]
                    for _ in range(8)]
                   for _ in range(2)]
                  for _ in range(6)]  # Piece_type / Side_to_move / Squares
        # [4 - as there are 4 possibilities ( -,Q,K,QK]
        cls.w_castling_right = [random.getrandbits(64) for _ in range(4)]
        # [4 - as there are 4 possibilities ( -,q,k,qk]
        cls.b_castling_right = [random.getrandbits(64) for _ in range(4)]
        # [8][8] - enPassant for every square (It is only possible for 16 squares but still works)
        cls.en_passant = [[random.getrandbits(64) for _ in range(8)]
                      for _ in range(8)]
        # 64bit - side to play
        cls.side = random.getrandbits(64)
