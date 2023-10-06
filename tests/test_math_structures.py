import unittest
from unittest import mock

from src.math_structures import MathList


class TestMathList(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.expression_one = MathList(['+', '2', '1'])
        self.expression_two = MathList(['-', '4', '3'])

    def test_validation_expression(self):
        self.assertRaises(ValueError, lambda: MathList._validate_expression(['+', '1']))
        self.assertRaises(ValueError, lambda: MathList._validate_expression(['+', '1', '1', '1']))

    def test_evaluate_expression(self):
        self.assertEqual(MathList._evaluate_expression(['+', '2', '1']), 3)
        self.assertEqual(MathList._evaluate_expression(['-', '4', '3']), 1)

    def test_addition(self):
        result = self.expression_one + self.expression_two
        self.assertListEqual(result.expression,
                             ['+', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_one.result + self.expression_two.result)

    def test_subtraction(self):
        result = self.expression_one - self.expression_two
        self.assertListEqual(result.expression,
                             ['-', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_one.result - self.expression_two.result)

    def test_multiplication(self):
        result = self.expression_one * self.expression_two
        self.assertListEqual(result.expression,
                             ['*', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_one.result * self.expression_two.result)

    def test_division(self):
        result = self.expression_one / self.expression_two
        self.assertListEqual(result.expression,
                             ['/', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_one.result / self.expression_two.result)

    def test_infix_conversion(self):
        self.assertEqual(MathList._from_math_list(['2'], 2).to_infix(), '2')
        self.assertEqual(self.expression_one.to_infix(), '2 + 1')
        self.assertEqual((self.expression_one + self.expression_two).to_infix(), '(2 + 1) + (4 - 3)')
