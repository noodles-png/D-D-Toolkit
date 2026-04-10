import unittest
from dice.roller import roll_dice

class TestRollDice(unittest.TestCase):
    def test_single_d6(self):
        result = roll_dice("1d6")
        self.assertGreaterEqual(result["total"], 1)
        self.assertLessEqual(result["total"], 6)

    def test_2d6_plus_3(self):
        result = roll_dice("2d6+3")
        self.assertGreaterEqual(result["total"], 5)
        self.assertLessEqual(result["total"], 15)

    def test_3d20_plus_10(self):
        result = roll_dice("3d20+10")
        self.assertGreaterEqual(result["total"], 13)
        self.assertLessEqual(result["total"], 70)
    def test_invalid_notation(self):
        with self.assertRaises(ValueError):
            roll_dice("abc")
