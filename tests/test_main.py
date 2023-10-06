import unittest
from unittest import mock
from countdown_numbers_solver.main import choose_numbers, print_closest_answers, main


class TestTreeRecursionGenerator(unittest.TestCase):
    pass


class TestFunctions(unittest.TestCase):
    def test_choose_numbers(self):
        with mock.patch('countdown_numbers_solver.main.input', return_value='4'):
            numbers, target_number = choose_numbers()

            self.assertTrue(len(numbers) == 6)
            self.assertTrue(sum(number <= 10 for number in numbers) == 4)

    def test_print_closest_answers(self):
        pass

    def test_main(self):
        pass
