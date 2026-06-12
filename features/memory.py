"""
Improved Memory Manager - Safe, Extendable, Persistent
"""

import os
import json


class Memory:
    def __init__(self, filename=".calculator_memory.json"):
        self.filename = os.path.join(os.path.expanduser("~"), filename)
        self._memory = 0.0
        self._load()

    # ---------------------------
    # VALIDATION
    # ---------------------------
    def _validate(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Memory only supports numeric values")

    # ---------------------------
    # LOAD / SAVE
    # ---------------------------
    def _load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self._memory = float(data.get("memory", 0.0))
        except Exception:
            self._memory = 0.0

    def _save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump({"memory": self._memory}, f)
        except Exception:
            pass

    # ---------------------------
    # OPERATIONS
    # ---------------------------
    def add(self, value):
        self._validate(value)
        self._memory += value
        self._save()

    def subtract(self, value):
        self._validate(value)
        self._memory -= value
        self._save()

    def multiply(self, value):
        self._validate(value)
        self._memory *= value
        self._save()

    def divide(self, value):
        self._validate(value)
        if value == 0:
            raise ZeroDivisionError("Cannot divide memory by zero")
        self._memory /= value
        self._save()

    def set(self, value):
        self._validate(value)
        self._memory = value
        self._save()

    def recall(self):
        return self._memory

    def clear(self):
        self._memory = 0.0
        self._save()

    # ---------------------------
    # EXTRA
    # ---------------------------
    def is_empty(self):
        return self._memory == 0.0

    def __str__(self):
        return f"Memory({self._memory})"