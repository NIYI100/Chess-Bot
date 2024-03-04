import math

from Application.Constants.HashEntryFlags import *
from Application.TranspositionTable.HashEntry import HashEntry

class TranspositionTable:
    _instance = None
    _transpositionTable = None
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TranspositionTable, cls).__new__(cls)
            # Initialize any variables here if necessary
            cls._instance._transpositionTable = [None] * 1048583
        return cls._instance

    def get_transposition_table(self):
        return self._transpositionTable

    def reset_transposition_table(self):
        self._transpositionTable = [None] * 1048583

# Creates an entry in the transpostion table
def create_entry_in_transpos_table_if_better(state, depth, flag, evaluation):
    transpositionTable = TranspositionTable().get_transposition_table()
    already_existing_entry = transpositionTable[state.zobristKey % len(transpositionTable)]

    if already_existing_entry is None or already_existing_entry.depth < depth:
        entry = HashEntry(state.zobristKey, depth, flag, evaluation, state.color)
        transpositionTable[state.zobristKey % len(transpositionTable)] = entry

# Checks if a transposition entry is valid and should be used or if the algorithm can not use the entry
# for example if the searched depth of the saved position is 1 but we have to search to a depth of 3
def check_transpos_table_if_useable(state, depth, alpha, beta):
    transpositionTable = TranspositionTable().get_transposition_table()
    hash_entry = transpositionTable[state.zobristKey % len(transpositionTable)]

    if hash_entry is not None and state.zobristKey == hash_entry.zobrist:
        # As we are saving relative evaluations we have to swap the value if color is not matching
        evaluation = hash_entry.evaluation
        if state.color != hash_entry.color:
            evaluation = - evaluation


        if hash_entry.depth >= depth:
            # Definite value of the position
            if hash_entry.flag == HASH_EXACT:
                return True
            # Move is too good for minimizing player
            if hash_entry.flag == HASH_BETA and evaluation >= beta:
                return True
            # Move is worse than already calculated evaluation player
            if hash_entry.flag == HASH_ALPHA and evaluation < alpha:
                return True
    return False


# returns the saved evaluation of a position
def get_eval_of_transpos_table(state):
    transpositionTable = TranspositionTable().get_transposition_table()
    hash_entry = transpositionTable[state.zobristKey % len(transpositionTable)]
    evaluation = hash_entry.evaluation
    if state.color != hash_entry.color:
        evaluation = - evaluation
    return evaluation

def sort_for_transpos_table(state, moves):
    move_evaluations = {move: _get_move_evaluation(state, move) for move in moves}
    return sorted(move_evaluations, key=move_evaluations.get, reverse=True)

def _get_move_evaluation(state, move):
    transpositionTable = TranspositionTable().get_transposition_table()
    state.push(move)

    entry = transpositionTable[state.zobristKey % len(transpositionTable)]
    if entry is not None:
        evaluation = entry.evaluation
        # Here we have to change the evaluation the other way around as we did push() which changes the color
        if entry.color == state.color:
            evaluation = - evaluation
    else:
        # TODO: Check what the best value for unexplored moves is
        evaluation = 0
    state.pop()
    # Fetch the evaluation from the transposition table; use a default if not found
    return evaluation