from Application.MoveGeneration.moveChecks import check_if_king_is_in_check, check_if_square_is_empty
from Application.Constants.pieceConstants import *


class CastlingRights:
    """
    This class defines the castling rights for the BoardState
    """
    def __init__(self):
        self.white_castle_short = True
        self.white_castle_long = True
        self.black_castle_short = True
        self.black_castle_long = True

    def update_castling(self, move):
        """
        Updates the castling rights based on the move. If the king or rooks move
        or a castling is executed the castling rights will be gone
        :param move: The move
        """
        old_col = ord(move[0]) - 97
        old_row = int(move[1]) - 1

        if old_row == 0:
            if old_col == 4:
                self.white_castle_long = False
                self.white_castle_short = False
            if old_col == 0:
                self.white_castle_long = False
            if old_col == 7:
                self.white_castle_short = False

        if old_row == 7:
            if old_col == 4:
                self.black_castle_long = False
                self.black_castle_short = False
            if old_col == 0:
                self.black_castle_long = False
            if old_col == 7:
                self.black_castle_short = False

    def get_castling_string(self):
        """
        Returns the castling string which is used in the FEN string of the position
        """
        castling_string = ""
        if self.white_castle_long:
            castling_string += "Q"
        if self.white_castle_short:
            castling_string += "K"
        if self.black_castle_long:
            castling_string += "q"
        if self.black_castle_short:
            castling_string += "k"
        if castling_string == "":
            castling_string = "-"
        return castling_string

    def get_castling_from_string(self, castling_string):
        """
        Converts a castling string to the corresponding CastlingRights
        :param castling_string: The string that correspons to the castling rights
        """
        temp_str = castling_string
        self.white_castle_short = False
        self.white_castle_long = False
        self.black_castle_short = False
        self.black_castle_long = False
        while len(temp_str) > 0 and temp_str != "-":
            match temp_str[0]:
                case "Q":
                    self.white_castle_long = True
                case "K":
                    self.white_castle_short = True
                case "q":
                    self.black_castle_long = True
                case "k":
                    self.black_castle_short = True
            temp_str = temp_str[1:]
