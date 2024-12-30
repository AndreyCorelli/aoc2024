from typing import List

FILE_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day07/input.txt"


class MathExpression:
    def __init__(self):
        self.result: int = 0
        self.operands: List[int] = []

    def _calculate(self):
        pass

    def __str__(self):
        return f"{self.result}: " + " ".join(map(str, self.operands))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def parse_line(cls, line: str) -> 'MathExpression':
        expression = cls()
        parts = line.split(":")
        expression.result = int(parts[0])
        expression.operands = list(map(int, parts[1].split()))
        return expression

    def check_feasibility(self) -> bool:
        def apply_concat_operator(a: int, b: int) -> int:
            num_digits_b = len(str(b))
            return a * (10 ** num_digits_b) + b

        def try_operator(operator: str, index: int, accumulated: int) -> bool:
            if index == len(self.operands):
                return accumulated == self.result

            a, b = accumulated, self.operands[index]
            next_accumulated = a + b if operator == '+' \
                else a * b if operator == '*' \
                else apply_concat_operator(a, b)

            if next_accumulated <= self.result:
                return try_operator("+", index + 1, next_accumulated) or \
                    try_operator("*", index + 1, next_accumulated) or \
                    try_operator("|", index + 1, next_accumulated)
            return False
        return try_operator("+", 0, 0)


def read_expressions() -> List[MathExpression]:
    with open(FILE_PATH, 'r') as file:
        content = file.read()
    lines = content.strip().split("\n")
    expressions = [MathExpression.parse_line(line) for line in lines]
    return expressions


def solution_1():
    expressions = read_expressions()
    sum_feasible_results = 0
    for expression in expressions:
        if expression.check_feasibility():
            sum_feasible_results += expression.result
    print(f"Sum of feasible results: {sum_feasible_results}")


if __name__ == "__main__":
    solution_1()