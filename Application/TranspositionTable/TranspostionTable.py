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
        """
        Returns the transposition table
        """
        return self._transpositionTable

    def get_index(self, zobristKey):
        """
        Returns the index corresponding to the given zobristKey
        :param zobristKey: The zobristKey
        """
        return zobristKey % len(self._transpositionTable)

    def reset_transposition_table(self):
        """
        Emptys the transposition table
        """
        self._transpositionTable = [None] * 1048583

    def delete_entry(self, index):
        """
        Deletes the entry at the given index
        :param index: The index
        """
        self._transpositionTable[index] = None

def create_entry_in_transpos_table_if_better(state, depth, flag, evaluation):
    """
    Creates an entry in the transposition table if given parameters are better than the current entry
    or if the entry is empty
    :param state: The BoardState
    :param depth: The depth to which was searched
    :param flag: The flag of the entry
    :param evaluation: The evaluation for the position
    """
    transpositionTable = TranspositionTable().get_transposition_table()
    index = TranspositionTable().get_index(state.zobristKey)
    already_existing_entry = transpositionTable[index]

    if already_existing_entry is None or already_existing_entry.depth < depth:
        entry = HashEntry(state.zobristKey, depth, flag, evaluation, state.color)
        transpositionTable[index] = entry

def check_transpos_table_if_useable(state, depth, alpha, beta):
    """
    Checks if the trabsposition table entry is useable.
    This is the case if:

    - There is an entry
    - The depth of the entry is higher than the depth of the method
    - The flag is HASH_EXACT or
    - The flag is HASH_BETA and the evaluation is greater than beta or
    - The flag is HASH_ALPHA and the evaluation is smaller than alpha
    :param state: The BoardState
    :param depth: The depth
    :param alpha: The alpha
    :param beta: The beta
    """
    transpositionTable = TranspositionTable().get_transposition_table()
    hash_entry = transpositionTable[state.zobristKey % len(transpositionTable)]

    if hash_entry is not None and state.zobristKey == hash_entry.zobrist:
        # As we are saving relative evaluations we have to swap the value if color is not matching
        evaluation = hash_entry.evaluation
        if state.color != hash_entry.color:
            evaluation = - evaluation


        if hash_entry.depth >= depth:
            if hash_entry.flag == HASH_EXACT:
                return True
            if hash_entry.flag == HASH_BETA and evaluation >= beta:
                return True
            if hash_entry.flag == HASH_ALPHA and evaluation < alpha:
                return True
    return False


def get_eval_of_transpos_table(state):
    """
    Returns the saved evaluation for a BoardState
    :param state: The BoardState
    """
    transpositionTable = TranspositionTable().get_transposition_table()
    hash_entry = transpositionTable[state.zobristKey % len(transpositionTable)]
    evaluation = hash_entry.evaluation
    if state.color != hash_entry.color:
        evaluation = - evaluation
    return evaluation

def sort_for_transpos_table(state, moves):
    """
    Sorts the moves in descending order based on the evaluation of the transposition entries.
    If for a state there is no evaluation saved the evaluation is set to 0
    :param state: The BoardState
    :param moves: The list of moves
    """
    move_evaluations = {move: _get_move_evaluation(state, move) for move in moves}
    return sorted(move_evaluations, key=move_evaluations.get, reverse=True)

def _get_move_evaluation(state, move):
    """
    Retrurns the evaluation of given BoardState after the move
    :param state: The BoardState
    :param move: The move
    """
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
    return evaluation