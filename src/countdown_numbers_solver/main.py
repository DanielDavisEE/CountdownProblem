"""
bruteforce_solutions22 (which uses dynamic programming and exclusively operates
on binary maths trees) has been improved to almost parity with bruteforce_solutions2
(which uses a greedy approach, operating on prefix expressions)


"""
import itertools
import random
from os import system, name
from math_structures import MathList, OPERATORS
import bisect

DEBUG = False

TOTAL_NUMBERS = 6
SMALL_NUMBERS = sorted([x for x in range(1, 11)] * 2)
LARGE_NUMBERS = [25, 50, 75, 100]


class TreeRecursionGenerator:
    operator_methods = {
        '+': MathList.__add__,
        '-': MathList.__sub__,
        '*': MathList.__mul__,
        '/': MathList.__truediv__}

    def __init__(self, values: list[int]):
        self.operands = tuple([MathList([str(value)]) for value in sorted(values)])
        self.results = {}
        self._found_values = set([None])

        self.generate_recurse(list(self.operands))

    def _combine_operands(self, op: str, a: MathList, b: MathList) -> MathList | None:
        try:
            return self.operator_methods[op](a, b)
        except (ValueError, ZeroDivisionError):
            return None

    def _get_complement(self, operands, used):
        return [operands[i] for i in range(len(operands)) if i not in used]

    def generate_recurse(self, operands):
        for a, b in itertools.combinations(range(len(operands)), 2):
            complement_list = self._get_complement(operands, {a, b})
            for op in OPERATORS:
                # operands are switched here so that the left is always greater than the right
                new_expression = self._combine_operands(op, operands[b], operands[a])

                if new_expression not in self._found_values and new_expression.result > 0:
                    self._found_values.add(new_expression)
                    self.results.setdefault(new_expression.result, []).append(new_expression)

                    if complement_list:
                        _complement = complement_list.copy()
                        bisect.insort(_complement, new_expression)

                        self.generate_recurse(_complement)


# ---------------
# Random Utility
# ---------------
def clear():
    """clear cmd output
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

    # ---------------


# Choose numbers
# ---------------
def choose_numbers():
    target_number = random.randint(100, 999)

    small_count = 0
    while small_count < 2:
        try:
            small_count = int(input('How many small numbers? (Between 2 and 6 inclusive): '))
        except ValueError:
            print('Must be an integer, try again.', end='\r')
        # clear() # For clearing output when run in cmd

    large_count = TOTAL_NUMBERS - small_count

    numbers = random.sample(SMALL_NUMBERS, small_count) + random.sample(LARGE_NUMBERS, large_count)

    print(f'Target number: {target_number}')
    print('Numbers: ', numbers)
    print()
    return numbers, target_number


def print_closest_answers(results_dict, target):
    """Find and print the result closest to the target, and all workings for
          this number. For ties, the first encountered is selected.
    """
    results = results_dict.keys()
    closest_results = [list(results)[0]]

    for result in results:
        if abs(target - closest_results[0]) > abs(target - result):
            closest_results = [result]
        if (abs(target - closest_results[0]) == abs(target - result)
                and closest_results[0] != result):
            closest_results.append(result)

    for result in closest_results:
        print(f'Possible solutions for: {result}')
        print(*results_dict[result], sep='\n')


def main():
    quit = False
    while not quit:
        numbers, target_number = choose_numbers()

        results_dict = TreeRecursionGenerator(numbers).results
        if DEBUG:
            print(*results_dict.items(), sep='\n')

        print_closest_answers(results_dict, target_number)
        print(f'\n{len(results_dict.keys())} distinct numbers found.')
        tmp = 0
        for num in range(100, 1000):
            if results_dict.get(num, None) is None:
                tmp += 1
        print(f'{tmp} numbers between 100 and 999 (inclusive) were unable to be found.')

        tmp = input('Restart? [y/n]: ')
        quit = None
        while quit is None:
            if tmp.lower() == 'n':
                quit = True
            elif tmp.lower() == 'y':
                quit = False
            else:
                tmp = input('What was that? [y/n]: ')


if __name__ == '__main__':
    main()
