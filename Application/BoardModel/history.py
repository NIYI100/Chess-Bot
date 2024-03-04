class History:
    _instance = None
    _history = []

    def __init__(self):
        pass
        #self.instance()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(History, cls).__new__(cls)
            # Initialize any variables here if necessary
            cls._instance._history = []
        return cls._instance

    #@classmethod
    #def instance(cls):
    #    if cls._instance is None:
    #        cls._instance = cls.__new__(History)
    #    return cls._instance

    def append(self, history_object):
        self._history.append(history_object)

    def pop(self):
        return self._history.pop()
