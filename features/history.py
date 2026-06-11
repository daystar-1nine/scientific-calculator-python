"""
Stores calculation history.
"""


class History:
    def __init__(self):
        self._history = []

    def add_entry(self, expression, result):
        self._history.append(f"{expression} = {result}")

    def get_history(self):
        return self._history.copy()

    def clear_history(self):
        self._history.clear()

    def get_last_entry(self):
        if self._history:
            return self._history[-1]
        return None