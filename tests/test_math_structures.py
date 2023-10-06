import unittest
from unittest import mock

from src.math_structures import MathList


class TestMathList(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.expression_one = MathList(['+', '2', '1'], 3)
        self.expression_two = MathList(['-', '4', '3'], 1)

    def test_addition(self):
        self.assertEqual(self.expression_one + self.expression_two,
                         self.expression_one.result + self.expression_two.result)

    def test_subtraction(self):
        self.assertEqual(self.expression_one - self.expression_two,
                         self.expression_one.result - self.expression_two.result)

    def test_multiplication(self):
        self.assertEqual(self.expression_one * self.expression_two,
                         self.expression_one.result * self.expression_two.result)

    def test_division(self):
        self.assertEqual(self.expression_one / self.expression_two,
                         self.expression_one.result / self.expression_two.result)

    def test_infix_conversion(self):
        self.assertEqual(self.expression_one.to_infix(), '4 - 3')
        self.assertEqual((self.expression_one.result + self.expression_two.result).to_infix(), '(2 + 1) + (4 - 3)')
