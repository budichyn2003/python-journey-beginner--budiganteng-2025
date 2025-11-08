import unittest
from calculator import add, subtract, multiply, divide, power, modulus

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 5), 8)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(1, 1), 0)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(3, 5), 15)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(-2, -3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 2), 3)
        self.assertEqual(divide(-6, 2), -3)
        self.assertEqual(divide(0, 5), 0)
        self.assertEqual(divide(5, 2), 2.5)
        self.assertEqual(divide(5, 0), "Error: Pembagian dengan nol tidak diperbolehkan!")

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(2, 0), 1)
        self.assertEqual(power(0, 0), 1)
        self.assertEqual(power(-2, 2), 4)

    def test_modulus(self):
        self.assertEqual(modulus(5, 2), 1)
        self.assertEqual(modulus(4, 2), 0)
        self.assertEqual(modulus(0, 5), 0)
        self.assertEqual(modulus(5, 0), "Error: Modulus dengan nol tidak diperbolehkan!")

if __name__ == '__main__':
    unittest.main()