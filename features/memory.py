"""
Handles calculator memory operations:
M+, M-, MR, MC
"""


class Memory:
    def __init__(self):
        self._memory = 0.0

    def add(self, value):
        self._memory += value

    def subtract(self, value):
        self._memory -= value

    def recall(self):
        return self._memory

    def clear(self):
        self._memory = 0.0