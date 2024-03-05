class History:
    """
    This singleton is used to store the BoardStates in the NegaMax
    """
    _instance = None
    _history = []

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(History, cls).__new__(cls)
            # Initialize any variables here if necessary
            cls._instance._history = []
        return cls._instance

    def append(self, history_object):
        """
        Appends an object to the history list
        :param history_object: The object to append
        """
        self._history.append(history_object)

    def pop(self):
        """
        Pops the last object from the history list
        """
        return self._history.pop()
