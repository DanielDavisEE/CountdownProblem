import itertools
import random
from countdown_numbers_solver.math_structures import MathList, OPERATORS
import bisect

TOTAL_NUMBERS = 6
SMALL_NUMBERS = sorted([x for x in range(1, 11)] * 2)
LARGE_NUMBERS = [25, 50, 75, 100]


class TreeRecursionGenerator:
    """
    A class which attempts to generate all possible answers from combining a list of
    values. Not guaranteed to find all unique expressions for a particular value as it considers
    expressions identical if they use the same numbers and have the same answer, and discards
    duplicates. For example (2 + 2) and (2 * 2) would be considered identical.
    """
    operator_methods = {
        '+': MathList.__add__,
        '-': MathList.__sub__,
        '*': MathList.__mul__,
        '/': MathList.__truediv__}

    def __init__(self, values: list[int]):
        self.operands = tuple([MathList([str(value)]) for value in sorted(values)])
        self.results = {}
        self._found_values = {None}

        self.generate_recurse(list(self.operands))

    def _combine_operands(self, op: str, a: MathList, b: MathList) -> MathList | None:
        try:
            return self.operator_methods[op](a, b)
        except (ValueError, ZeroDivisionError):
            return None

    @staticmethod
    def _get_complement(operands, used):
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


def choose_numbers() -> tuple[list[int], int]:
    target_number = random.randint(100, 999)

    while True:
        try:
            small_count = int(input('How many small numbers? (Between 2 and 6, inclusive): '))
            assert 2 <= small_count <= 6
        except (ValueError, AssertionError):
            continue
        break

    large_count = TOTAL_NUMBERS - small_count

    numbers = random.sample(SMALL_NUMBERS, small_count) + random.sample(LARGE_NUMBERS, large_count)

    print(f'Target number: {target_number}')
    print('Numbers: ', numbers)
    print()
    return numbers, target_number


def print_closest_answers(results_dict: dict[int, list[MathList]], target: int):
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
    running = True
    while running:
        numbers, target_number = choose_numbers()

        results_dict = TreeRecursionGenerator(numbers).results

        print_closest_answers(results_dict, target_number)
        print(f'\n{len(results_dict.keys())} distinct numbers found.')
        tmp = 0
        for num in range(100, 1000):
            if results_dict.get(num, None) is None:
                tmp += 1
        print(f'{tmp} numbers between 100 and 999 (inclusive) were unable to be found.')

        tmp = input('Restart? [y/n]: ')
        running = None
        while running is None:
            if tmp.lower() in ['n', 'no']:
                running = False
            elif tmp.lower() in ['y', 'yes']:
                running = True
            else:
                tmp = input('What was that? [y/n]: ')


if __name__ == '__main__':
    main()
