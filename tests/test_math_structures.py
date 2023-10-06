import unittest
from unittest import mock

from countdown_numbers_solver.math_structures import MathList


class TestMathList(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.expression_3 = MathList(['+', '2', '1'])  # 3
        self.expression_1 = MathList(['-', '4', '3'])  # 1
        self.expression_3_cp = self.expression_3.copy()  # 3

    def test_validation_expression(self):
        self.assertRaises(ValueError, lambda: MathList._validate_expression(['+', '1']))
        self.assertRaises(ValueError, lambda: MathList._validate_expression(['+', '1', '1', '1']))

    def test_evaluate_expression(self):
        self.assertEqual(MathList._evaluate_expression(['+', '2', '1']), 3)
        self.assertEqual(MathList._evaluate_expression(['-', '4', '3']), 1)

    def test_addition(self):
        result = self.expression_3 + self.expression_1
        self.assertListEqual(result.expression,
                             ['+', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_3.result + self.expression_1.result)

    def test_subtraction(self):
        result = self.expression_3 - self.expression_1
        self.assertListEqual(result.expression,
                             ['-', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_3.result - self.expression_1.result)

    def test_multiplication(self):
        result = self.expression_3 * self.expression_1
        self.assertListEqual(result.expression,
                             ['*', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_3.result * self.expression_1.result)

    def test_division(self):
        result = self.expression_3 / self.expression_1
        self.assertListEqual(result.expression,
                             ['/', '+', '2', '1', '-', '4', '3'])
        self.assertEqual(result.result,
                         self.expression_3.result / self.expression_1.result)

    def test_copy(self):
        self.assertFalse(self.expression_3 is self.expression_3_cp)

        self.assertEqual(self.expression_3.expression, self.expression_3_cp.expression)
        self.assertEqual(self.expression_3.result, self.expression_3_cp.result)

    def test_comparison(self):
        with self.subTest('equal'):
            self.assertTrue(self.expression_3 == self.expression_3_cp)
            self.assertFalse(self.expression_3 == self.expression_1)

        with self.subTest('not_equal'):
            self.assertTrue(self.expression_3 != self.expression_1)
            self.assertFalse(self.expression_3 != self.expression_3_cp)

        with self.subTest('less_than'):
            self.assertTrue(self.expression_1 < self.expression_3)
            self.assertFalse(self.expression_3_cp < self.expression_3)
            self.assertFalse(self.expression_3 < self.expression_1)

        with self.subTest('greater_than'):
            self.assertFalse(self.expression_1 > self.expression_3)
            self.assertFalse(self.expression_3_cp > self.expression_3)
            self.assertTrue(self.expression_3 > self.expression_1)

        with self.subTest('less_than_equal'):
            self.assertTrue(self.expression_1 <= self.expression_3)
            self.assertTrue(self.expression_3_cp <= self.expression_3)
            self.assertFalse(self.expression_3 <= self.expression_1)

        with self.subTest('greater_equal'):
            self.assertFalse(self.expression_1 >= self.expression_3)
            self.assertTrue(self.expression_3_cp >= self.expression_3)
            self.assertTrue(self.expression_3 >= self.expression_1)

    def test_infix_conversion(self):
        self.assertEqual(MathList._from_math_list(['2'], 2).to_infix(), '2')
        self.assertEqual(self.expression_3.to_infix(), '2 + 1')
        self.assertEqual((self.expression_3 + self.expression_1).to_infix(), '(2 + 1) + (4 - 3)')
