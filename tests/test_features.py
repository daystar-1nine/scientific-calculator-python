import unittest
import os
from features.memory import Memory
from features.history import History


class TestFeatures(unittest.TestCase):

    def test_memory_operations(self):
        mem = Memory()
        self.assertEqual(mem.recall(), 0.0)

        mem.add(10.5)
        self.assertEqual(mem.recall(), 10.5)

        mem.subtract(3.5)
        self.assertEqual(mem.recall(), 7.0)

        mem.clear()
        self.assertEqual(mem.recall(), 0.0)

    def test_history_operations(self):
        test_file = ".test_calculator_history"
        # Ensure it starts clean
        if os.path.exists(test_file):
            os.remove(test_file)

        hist = History(filename=test_file)
        self.assertEqual(hist.get_history(), [])
        self.assertIsNone(hist.get_last_entry())

        hist.add_entry("2 + 3", "5")
        self.assertEqual(hist.get_history(), ["2 + 3 = 5"])
        self.assertEqual(hist.get_last_entry(), "2 + 3 = 5")

        hist.add_entry("10 / 2", "5")
        self.assertEqual(hist.get_history(), ["2 + 3 = 5", "10 / 2 = 5"])
        self.assertEqual(hist.get_last_entry(), "10 / 2 = 5")

        hist.clear_history()
        self.assertEqual(hist.get_history(), [])
        self.assertIsNone(hist.get_last_entry())

        # Final cleanup
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
