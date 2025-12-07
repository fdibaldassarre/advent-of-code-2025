#!/usr/bin/env python
import functools


class Solver:

    class Problem:

        def __init__(self) -> None:
            self.operation = "?"
            self.values: list[int] = []

        def add_value(self, value: int) -> None:
            self.values.append(value)

        def evaluate(self) -> int:
            if self.operation == "+":
                return sum(self.values)
            elif self.operation == "*":
                return functools.reduce(lambda x, y: x * y, self.values, 1)

    def __init__(self) -> None:
        self._problems: list[Solver.Problem] = []
        self._problems_v2: list[Solver.Problem] = []

    def parse(self, path: str) -> None:
        full_text: list[str] = []
        max_width = 0
        with open(path) as hand:
            for line in hand:
                full_text.append(line.rstrip())
                max_width = max(max_width, len(full_text[-1]))
                line = line.strip()
                problem_num = 0
                for el in line.split(" "):
                    if not el:
                        continue
                    if len(self._problems) <= problem_num:
                        self._problems.append(Solver.Problem())
                    if el in {"+", "*"}:
                        self._problems[problem_num].operation = el
                    else:
                        self._problems[problem_num].add_value(int(el))
                    problem_num += 1

        self._problems_v2 = []

        for column in range(max_width):
            number: list[str] = []
            for i in range(len(full_text) - 1):
                if column < len(full_text[i]) and full_text[i][column] != " ":
                    number.append(full_text[i][column])
            operation = full_text[-1][column] if column < len(full_text[-1]) else " "
            if operation != " ":
                self._problems_v2.append(Solver.Problem())
                self._problems_v2[-1].operation = operation
            if number:
                self._problems_v2[-1].add_value(int("".join(number)))

    def solve1(self) -> int:
        total = 0
        for problem in self._problems:
            total += problem.evaluate()
        return total

    def solve2(self) -> int:
        total = 0
        for problem in self._problems_v2:
            total += problem.evaluate()
        return total


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
