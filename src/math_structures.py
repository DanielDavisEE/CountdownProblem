OPERATORS = ['+', '-', '*', '/']
DEBUG = False


class MathList:

    def __init__(self, expression: list[str], result: int):
        """

        Args:
            expression: A prefix expression represented as a list of strings
                e.g.: ['+', '2', '1']
            result: The result of the expression
        """
        self.expression = expression
        self.result = result

    def __add__(self, other_expression):
        new_expression = ['+'] + self.expression + other_expression

        assert self.result >= other_expression.result
        new_result = self.result + other_expression.result

        return MathList(new_expression, new_result)

    def __sub__(self, other_expression):
        new_expression = ['-'] + self.expression + other_expression

        if self.result == other_expression.result:
            return None

        assert self.result >= other_expression.result
        new_result = self.result - other_expression.result

        return MathList(new_expression, new_result)

    def __mul__(self, other_expression):
        new_expression = ['*'] + self.expression + other_expression

        if self.result == 1 or other_expression.result == 1:
            return None

        assert self.result >= other_expression.result
        new_result = self.result * other_expression.result

        return MathList(new_expression, new_result)

    def __truediv__(self, other_expression):
        new_expression = ['/'] + self.expression + other_expression

        if self.result == 1 or other_expression.result == 1:
            return None
        if self.result % other_expression.result != 0:
            return None

        assert self.result >= other_expression.result

        new_result = int(self.result / other_expression.result)

        return MathList(new_expression, new_result)

    def __hash__(self):
        return tuple(self.expression).__hash__()

    def sort_atom(self):
        pass

    def verify_atom(self):
        pass

    def evaluate_atom(self):
        pass

    def iterate_bottom_up(self, func):
        pass

    def iterate_top_down(self, func):
        raise NotImplementedError
        # tmp1, tmp2 = 0, 0
        # while tmp2 < 99:  # Just in case, should be impossible
        #     if sub_expression[tmp2] in OPERATORS:
        #         tmp1 += 1
        #     elif sub_expression[tmp2].isdigit():
        #         tmp1 -= 1
        #     if tmp1 <= 0:
        #         break
        #     tmp2 += 1
        #
        # index = tmp2 + 1

    def recurse_bottom_up(self, func):
        pass

    def recurse_top_down(self, func, sub_expression=None, i=0):
        """Recursively breaks down a prefix expression in more basic expressions
           to be evaluated.
        """
        if sub_expression is None:
            sub_expression = self.expression
        # Return if all that is left is a single number
        if len(sub_expression) == 1:
            func(self, i)
        else:
            # Find index of point between two operands in expression
            tmp1, tmp2 = 0, 0
            while tmp2 < 99:  # Just in case, should be impossible
                if sub_expression[tmp2] in OPERATORS:
                    tmp1 += 1
                elif sub_expression[tmp2].isdigit():
                    tmp1 -= 1
                if tmp1 <= 0:
                    break
                tmp2 += 1

            index = tmp2 + 1

            # Recurse after dividing into operator, operand a and operand b
            operand_a = self.recurse_top_down(func, sub_expression[1:index], 1)
            operand_b = self.recurse_top_down(func, sub_expression[index:], index)

            func(self, i)

            # Check if an input was erroneus
            if operand_a is '' or operand_b is '':
                return ''

            # return func([sub_expression[0],
            # operand_a,
            # operand_b])

    def to_infix(self):

        def recurse(sub_expression=None):
            if sub_expression is None:
                sub_expression = list(self)
            # Return if all that is left is a single number
            if len(sub_expression) == 1:
                return sub_expression
            else:
                # Find index of point between two operands in expression
                tmp1, tmp2 = 0, 0
                while tmp2 < 99:  # Just in case, should be impossible
                    if sub_expression[tmp2] in OPERATORS:
                        tmp1 += 1
                    elif sub_expression[tmp2].isdigit():
                        tmp1 -= 1
                    if tmp1 <= 0:
                        break
                    tmp2 += 1

                index = tmp2 + 1

                # Recurse after dividing into operator, operand a and operand b
                operand_a = recurse(sub_expression[1:index])
                operand_b = recurse(sub_expression[index:])

                # Check if an input was erroneous
                if operand_a is '' or operand_b is '':
                    return ''

                return ['('] + operand_a + [' ', sub_expression[0], ' '] + operand_b + [')']

        expression = ''.join(recurse())

        return expression[1:-1] if len(self.expression) > 1 else expression


if __name__ == "__main__":
    # a = MathTree(['+', '2', '1'], prefix=True, sort=True)
    a = MathList(['+', '2', '1'], 3)
    b = MathList(['-', '4', '3'], 1)
    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)
    print((a + b).to_infix())
    print(b.to_infix())
