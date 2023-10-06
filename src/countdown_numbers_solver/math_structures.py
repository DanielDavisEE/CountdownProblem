from typing import Self

OPERATORS = {'+', '-', '*', '/'}
DEBUG = False


class MathList:

    def __init__(self, expression: list[str] = None):
        """

        Args:
            expression: A prefix expression represented as a list of strings
                e.g.: ['+', '2', '1']
            result: The result of the expression
        """
        self.expression = expression

        if self.expression is not None:
            self._validate_expression(expression)
            self.result = self._evaluate_expression(expression)
        else:
            self.result = None

    @classmethod
    def _from_math_list(cls, expression, result):
        inst = MathList()
        inst.expression = expression
        inst.result = result
        return inst

    def __add__(self, other: Self) -> Self:
        new_expression = ['+'] + self.expression + other.expression
        new_result = self.result + other.result

        return MathList._from_math_list(new_expression, new_result)

    def __sub__(self, other: Self) -> Self:
        new_expression = ['-'] + self.expression + other.expression
        new_result = self.result - other.result

        return MathList._from_math_list(new_expression, new_result)

    def __mul__(self, other: Self) -> Self:
        new_expression = ['*'] + self.expression + other.expression
        new_result = self.result * other.result

        return MathList._from_math_list(new_expression, new_result)

    def __truediv__(self, other: Self) -> Self:
        if other.result == 0:
            raise ZeroDivisionError
        if self.result % other.result != 0:
            raise ValueError(f'{self.result} is not divisible by {other.result}')

        new_expression = ['/'] + self.expression + other.expression
        new_result = int(self.result / other.result)

        return MathList._from_math_list(new_expression, new_result)

    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.result == other
        if isinstance(other, float):
            return self.result == other
        elif isinstance(other, MathList):
            return self.result == other.result
        raise NotImplementedError(f"Equality not implemented for MathList and {type(other)}")

    def __hash__(self):
        return tuple(self.expression).__hash__()

    def __str__(self):
        return f"{self.to_infix()}={self.result}"

    def __repr__(self):
        return self.expression, self.result

    @staticmethod
    def _validate_expression(expression) -> None:
        num_operators = sum(item in OPERATORS for item in expression)
        num_digits = sum(item.isdigit() for item in expression)
        if num_operators != num_digits - 1:
            raise ValueError(f"Expression '{expression}' does not have the correct ratio of numbers and operators.")

    @classmethod
    def break_down_expression(cls, expression):
        operator = expression[0]
        assert operator in OPERATORS, f"{operator} must be in {OPERATORS}"

        index, count = 1, 0
        while True:
            if expression[index] in OPERATORS:
                count += 1
            elif expression[index].isdigit():
                count -= 1

            index += 1
            if count < 0:
                break

        return operator, expression[1:index], expression[index:]

    @classmethod
    def _evaluate_expression(cls, expression) -> int:
        if len(expression) == 1:
            return int(expression[0])

        operator, sub_expression_a, sub_expression_b = cls.break_down_expression(expression)

        return eval(
            f"{cls._evaluate_expression(sub_expression_a)}{operator}{cls._evaluate_expression(sub_expression_b)}")

    def sort(self) -> None:
        pass

    def iterate_bottom_up(self, func):
        pass

    @classmethod
    def _to_infix_list(cls, expression) -> list[str]:
        if len(expression) == 1:
            return expression

        operator, sub_expression_a, sub_expression_b = cls.break_down_expression(expression)

        return ['('] + cls._to_infix_list(sub_expression_a) + [' ', operator, ' '] + cls._to_infix_list(
            sub_expression_b) + [')']

    def to_infix(self) -> str:
        infix_list = self._to_infix_list(self.expression)
        if len(infix_list) > 1:
            infix_list = infix_list[1:-1]
        return ''.join(infix_list)
