# Taken from https://mediocrechess.sourceforge.net/guides/transpositiontables.html
# Data Class for HashEntries used in the transposition table

class HashEntry:
    def __init__(self, zobrist, depth, flag, evaluation, ancient):
        self.zobrist = zobrist
        self.depth = depth
        self.flag = flag
        self.evaluation = evaluation
        self.ancient = ancient
