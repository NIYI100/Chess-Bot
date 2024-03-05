import random


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
        """
        Generates the random values used to calculate the zobrist key for the positions
        """
        # [6][2][8][8] - [piece type][side to play][row][column]
        cls.pieces = [[[[random.getrandbits(64) for _ in range(8)]
                    for _ in range(8)]
                   for _ in range(2)]
                  for _ in range(6)]
        # [4] - as there are 4 possibilities [-,Q,K,QK]
        cls.w_castling_right = [random.getrandbits(64) for _ in range(4)]
        # [4] - as there are 4 possibilities [-,q,k,qk]
        cls.b_castling_right = [random.getrandbits(64) for _ in range(4)]
        # [8][8] - enPassant for every square (It is only possible for 16 squares but still works)
        cls.en_passant = [[random.getrandbits(64) for _ in range(8)]
                      for _ in range(8)]
        # 64bit - side to play
        cls.side = random.getrandbits(64)
