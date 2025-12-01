#!/usr/bin/env python

class Solver:

    def __init__(self):
        self.moves: list[tuple[str, int]] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for el in hand:
                raw = el.strip()
                value = int(raw[1:])
                self.moves.append((raw[0], value))

    def solve1(self) -> int:
        pwd = 0
        current = 50
        for direction, val in self.moves:
            sign = 1 if direction == 'R' else -1
            current = (current + sign * val) % 100
            if current == 0:
                pwd += 1
        return pwd

    def solve2(self) -> int:
        pwd = 0
        current = 50
        for direction, val in self.moves:
            sign = 1 if direction == 'R' else -1
            new_current = current + sign * val
            if new_current >= 100:
                pwd += new_current // 100
                new_current = new_current % 100
            elif new_current <= 0:
                pwd += abs(new_current) // 100
                if current != 0:
                    pwd += 1
                new_current = new_current % 100
            current = new_current
        return pwd


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
