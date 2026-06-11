"""
Stores calculation history.
"""


import os
from utils.constants import MAX_HISTORY_SIZE


class History:
    def __init__(self, filename=".calculator_history"):
        # Save history in the user's home directory to guarantee write permissions
        self.filename = os.path.join(os.path.expanduser("~"), filename)
        self._history = []
        self._load_history()

    def _load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self._history = [line.strip() for line in f if line.strip()]
            except Exception:
                self._history = []

    def _save_history(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for entry in self._history:
                    f.write(entry + "\n")
        except Exception:
            pass

    def add_entry(self, expression, result):
        entry = f"{expression} = {result}"
        self._history.append(entry)
        if len(self._history) > MAX_HISTORY_SIZE:
            self._history = self._history[-MAX_HISTORY_SIZE:]
        self._save_history()

    def get_history(self):
        return self._history.copy()

    def clear_history(self):
        self._history.clear()
        if os.path.exists(self.filename):
            try:
                os.remove(self.filename)
            except Exception:
                pass

    def get_last_entry(self):
        if self._history:
            return self._history[-1]
        return None