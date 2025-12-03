#!/usr/bin/env python


class Solver:

    def __init__(self) -> None:
        self.banks: list[list[int]] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                self.banks.append([int(el) for el in line])

    def solve1(self) -> int:
        tot_joltage = 0
        for bank in self.banks:
            arg_max = 0
            for i in range(1, len(bank) - 1):
                if bank[i] > bank[arg_max]:
                    arg_max = i
            arg_max2 = arg_max + 1
            for i in range(arg_max2 + 1, len(bank)):
                if bank[i] > bank[arg_max2]:
                    arg_max2 = i
            tot_joltage += (bank[arg_max] * 10 + bank[arg_max2])
        return tot_joltage

    def solve2(self) -> int:
        tot_joltage = 0
        for bank in self.banks:
            arg_max = 0
            for idx in range(12):
                for i in range(arg_max + 1, len(bank) - 11 + idx):
                    if bank[i] > bank[arg_max]:
                        arg_max = i
                tot_joltage += (bank[arg_max] * 10 ** (11 - idx))
                arg_max += 1
        return tot_joltage


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
