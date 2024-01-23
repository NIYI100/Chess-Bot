class BoardState:
    def __init__(self, board, color, castleRights, enPassant, halfmoves, fullmoves):
        self.board = board
        self.color = color
        self.castleRights = castleRights
        self.enPassant = enPassant
        self.halfmoves = halfmoves
        self.fullmoves = fullmoves