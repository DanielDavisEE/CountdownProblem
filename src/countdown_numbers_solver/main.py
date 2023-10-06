"""
bruteforce_solutions22 (which uses dynamic programming and exclusively operates
on binary maths trees) has been improved to almost parity with bruteforce_solutions2
(which uses a greedy approach, operating on prefix expressions)


"""
import itertools
import random
from os import system, name
from math_structures import MathList, OPERATORS

DEBUG = False

TOTAL_NUMBERS = 6
SMALL_NUMBERS = sorted([x for x in range(1, 11)] * 2)
LARGE_NUMBERS = [25, 50, 75, 100]


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
    small_count = 0
    while small_count < 2:
        try:
            small_count = int(input('How many small numbers? (At least 2): '))
        except ValueError:
            print('Must be an integer, try again.', end='\r')
        # clear() # For clearing output when run in cmd

    large_count = TOTAL_NUMBERS - small_count

    numbers = []

    for _ in range(large_count):
        tmp = None
        while tmp is None:
            index = random.randint(0, len(LARGE_NUMBERS) - 1)
            tmp = LARGE_NUMBERS[index]
            LARGE_NUMBERS[index] = None
        numbers.append(tmp)

    for _ in range(small_count):
        tmp = None
        while tmp is None:
            index = random.randint(0, len(SMALL_NUMBERS) - 1)
            tmp = SMALL_NUMBERS[index]
            SMALL_NUMBERS[index] = None
        numbers.append(tmp)

    target_number = random.randint(100, 999)

    print(f'Target number: {target_number}')
    print(*numbers)
    return numbers, target_number


# ---------------
# Calculate numbers
# ---------------

class EquationGenerator():

    def __init__(self, numbers):
        """
        Attributes:
         - numbers
         - structure
        """

        self.numbers = numbers
        self.generate_structure()

    def _recurse(self, group, options):
        if len(group) == len(options):
            return None

        for option in options:
            if option not in group:
                new_group = tuple(sorted(list(group) + [option], key=int, reverse=True))

                self.structure[new_group] = self.structure.get(new_group, (set(), {}))
                self.structure[group][0].add(new_group)
                self._recurse(new_group, options)

    def generate_structure(self):
        """
        # self.structure = {
        #     (operands): ({combinations of n-1 operands}, {result: {expressions, ...}}),
        #     tuple(str(), ...): tuple(set(tuple(), ...), dict(int(): set(MathTree(), ...))),
        #     ('1,'): ({set()}, {1: [1]}),
        #     ...
        # }
        structure = {
            ('operands'): (
                {'combinations of n-1 operands'},
                {'result': {'expressions', '...'}}
            ),
            tuple[str]: (
                set[tuple],
                {int: set[MathList]}
            ),
            ('1',): (
                {set()},
                {1: {MathList(['1'])}}
            ),
            ('1', '2'): (
                {('1',), ('2',)},
                {1: {MathList(['1']),
                     MathList(['-', '2', '1'])},
                 2: {MathList(['2']),
                     MathList(['*', '2', '1']),
                     MathList(['*', '1', '2']),
                     },
                 3: {MathList(['+', '2', '1']),
                     MathList(['+', '1', '2']),
                     }
                 }
            ),
        }
        """
        self.structure = {tuple(): (set(), {})}

        self._recurse(tuple(), self.numbers)

        for number_group in self.structure[tuple()][0]:
            result = int(number_group[0])
            self.structure[number_group][1][result] = set([MathList(number_group, result)])

    def generate_expressions(self):

        def add_components(self, branch1, branch2):
            viable_trees = []
            # for f in [MathList.__add__,
            # MathList.__sub__]:
            for f in [MathList.__add__,
                      MathList.__sub__,
                      MathList.__mul__,
                      MathList.__truediv__]:
                tree = f(branch1, branch2)
                if tree is not None and tree.result > 0:
                    viable_trees.append(tree)

            return viable_trees

        def generate_components(operands):
            for i in range(1, len(operands)):
                yield operands[:i], operands[i:]

        queue = [tuple([n]) for n in self.numbers]
        processed = []

        while queue != []:
            operands = queue.pop(0)
            if operands in processed:
                continue
            queue.extend(self.structure[operands][0])
            n = len(operands)
            m = (n - 1) // 2
            # print(f"{operands}")

            components = generate_components(operands)
            for component, complement in components:
                # print(f"\t{component} - {complement}")

                # Iterate results found with numbers in components
                for i in self.structure[component][1]:

                    # Iterate results found with numbers in complement
                    for j in self.structure[complement][1]:

                        # Iterate expressions that give results in component
                        for x in self.structure[component][1][i]:

                            # Iterate expressions that give results in complement
                            for y in self.structure[complement][1][j]:
                                # Make sure that expressions are accurately assigned results
                                # assert i == x.result and j == y.result

                                if i > j:
                                    viable_trees = add_components(self, x, y)
                                elif j > i:
                                    viable_trees = add_components(self, y, x)
                                else:
                                    viable_trees = add_components(self, x, y)

                                for new_tree in viable_trees:
                                    # Test whether tree is already in structure here
                                    existing_trees = self.structure[operands][1].get(new_tree.result, set())
                                    if new_tree in existing_trees:
                                        print(new_tree.result, new_tree)
                                    else:
                                        existing_trees.add(new_tree)
                                        self.structure[operands][1][new_tree.result] = existing_trees

                                    # self.structure[operands][1][new_tree.result] = self.structure[operands][1].get(new_tree.result, set())

                                    # self.structure[operands][1][new_tree.result].add(new_tree)
            processed.append(operands)


# ------------------------------
# Functions
# ------------------------------

# def bruteforce_solutions(numbers, n=None):
#     """list, int -> dict
#        Using a recursion tree, bruteforce all possible workings using the given
#           numbers, then evaluate and store their results.
#     """
#     results_dict = {}  # {key: None for key in range(100, 1000)}
#     if n is None:
#         n = 2 * len(numbers) - 1
#     operator_limit = len(numbers) - 1
#     operand_limit = len(numbers)
#     buffer_length = (len(numbers) + len(OPERATORS)) * len(OPERATORS)
#     buffer_progress = [0]
#
#     def recurse(expression, operator_count, operand_count, options, max_length=n):
#         # Catch final recursion. A finished expression always ends with None.
#         if len(expression) > 0 and expression[-1] is None:
#             expression = MathTree(expression[:-1], sort=True, prefix=True)
#             result = expression.result
#             if not result is None and not expression.redundant and result >= 0:
#                 if result not in results_dict.keys():
#                     results_dict[result] = []
#
#                 if expression not in results_dict[result]:
#                     results_dict[result] += [expression]
#
#         # Continue recursion
#         else:
#             # If it gives a proper expression, terminate
#             if operand_count - 1 == operator_count:
#                 recurse(expression + [None], operator_count,
#                         operand_count, options)
#             else:
#                 for i in options:
#                     if len(expression) == 1:
#                         buffer_progress[0] += 1
#                         # print(f'|{"."*buffer_progress[0]}{" "*(buffer_length - buffer_progress[0])}|')
#
#                     # If it is an operator, check it is within limits
#                     if i in OPERATORS:
#                         if operator_count < operator_limit:
#                             recurse(expression + [i], operator_count + 1,
#                                     operand_count, options)
#
#                     # Check the number of operands is within limits before
#                     #    adding one.
#                     elif (operand_count < 2 * operator_count
#                           and operand_count < operand_limit):
#                         # Is this a leaf node with a sibling?
#                         if (len(expression) > 2
#                                 and expression[-1].isdigit()):
#                             # Ensure the subtraction doesn't give a negative number
#                             if (expression[-2] == '-'
#                                     and int(i) > int(expression[-1])):
#                                 return None
#                             # Ensure a division gives a whole number
#                             if (expression[-2] == '/'
#                                     and (int(expression[-1])) % int(i) != 0
#                                     or int(expression[-1]) / int(i) == 0):
#                                 return None
#                         options_tmp = options.copy()
#                         options_tmp.remove(i)
#                         recurse(expression + [i], operator_count,
#                                 operand_count + 1, options_tmp)
#
#     # Run bruteforce recursion to find all operations using the given numbers
#     options = [str(x) for x in numbers]
#     options.extend(OPERATORS)
#     recurse([], 0, 0, options)
#     return results_dict, {}


def bruteforce_solutions2(numbers):
    generator = EquationGenerator([str(x) for x in numbers])
    # [print(f"{x}{' '*(20-len(str(x)))}{y}") for x, y in generator.structure.items()]
    generator.generate_expressions()
    values = {}
    for i in generator.structure.values():
        i = i[1]
        for j in i:
            values[j] = values.get(j, []) + list(i[j])
    # for value in values:
    # print(value)
    # for expression in values[value]:
    # print(expression)
    return values, {}


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
        print(f'\t{result}')
        [print(' '.join(x)) for x in results_dict[result]]
        # [print(' '.join(x.extract_expression(prefix=True)),'\t', ''.join(x.extract_expression(infix=True))) for x in results_dict[result]]


# class ExpressionGenerator:
#     def __init__(self, values: list[int]):
#         self.operands = tuple(values)
#         self.num_operators = 0
#         self.num_operands = 0
#
#     def __iter__(self):
#         self.num_operators = 0
#         self.num_operands = 0
#         return self
#
#     def __next__(self):
#         if self.num_operands >= len(self.operands) - 1:
#             options = self.operands
#         elif self.num_operands <= self.num_operators:
#             options = self.operands

def generate_expressions(values: list[int]):
    operands = tuple(sorted(values, reverse=True))
    num_operators = 0
    num_operands = 0

    while num_operands < len(operands):
        if num_operands >= len(operands) - 1:
            options = operands
        elif num_operands <= num_operators:
            options = operands

class TreeRecursionGenerator:
    def __init__(self, values: list[int]):
        self.operands = tuple(sorted(values, reverse=True))
        self.found_values = {}

        self.generate_recurse(self.operands)

    def _combine_operands(self, op, a, b):
        operator_methods = {
            '+': int.__add__,
            '-': int.__sub__,
            '*': int.__mul__,
            '/': int.__truediv__}

        return operator_methods[op](a, b)

    def generate_recurse(self, operands):
        for a, b in itertools.combinations(operands, 2):
            for op in OPERATORS:
                result = self._combine_operands(op, a, b)
                # self.generate_recurse(operands - {a, b} + {result})


def main():
    numbers, target_number = [2, 3], 10
    results_dict = {}
    quit = False
    while not quit:
        numbers, target_number = [100, 1, 9, 10, 25], 364

        # [100, 1, 9, 10], 364
        # [100, 25, 8, 1, 9, 10], 364
        # choose_numbers()

        results_dict, repeats_dict = bruteforce_solutions2(numbers)
        if DEBUG:
            [print(x) for x in results_dict.items()]

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

    return results_dict


if __name__ == '__main__':

    numbers = [2, 10, 7, 5]  # , 25, 75]

    dict_b, _ = bruteforce_solutions2(numbers)

    print(f'\n{len(dict_b.keys())} unique numbers were found.')
    tmp = 0
    for v in dict_b.values():
        tmp += len(v)
    print(f'{tmp} unique expressions were found.')

    for i in dict_b:
        if i not in numbers:
            print('\n\t', i)
            for j in dict_b[i]:
                print(f"{j.to_infix():32}\t##########\t{' '.join(j)}")
