import unittest

from Application.BoardModel.history import History


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.history = History()
        self.history._history = []


    def test_singleton(self):
        newHistory = History()
        self.assertEqual(newHistory, self.history)

    def test_append(self):
        newHistory = History()
        self.history.append("Test1")
        newHistory.append("Test2")
        self.assertEqual(self.history, newHistory)
        self.assertEqual(len(self.history._history), 2)

    def test_pop(self):
        newHistory = History()
        self.history._history.append("Test1")
        self.history._history.append("Test2")
        self.assertEqual(self.history, newHistory)
        self.assertEqual(len(self.history._history), 2)

        self.history.pop()
        self.history.pop()
        self.assertEqual(self.history, newHistory)
        self.assertEqual(len(self.history._history), 0)