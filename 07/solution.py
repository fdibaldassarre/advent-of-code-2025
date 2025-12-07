#!/usr/bin/env python
from collections import defaultdict


class Solver:

    def __init__(self) -> None:
        self.__start = -1
        self.__map: list[str] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                if self.__start == -1:
                    self.__start = line.find("S")
                self.__map.append(line)

    def solve1(self) -> int:
        beams = {self.__start}
        num_splits = 0
        for i in range(1, len(self.__map)):
            new_beams: set[int] = set()
            for beam in beams:
                if self.__map[i][beam] == "^":
                    num_splits += 1
                    new_beams.add(beam-1)
                    new_beams.add(beam+1)
                else:
                    new_beams.add(beam)
            beams = new_beams
        return num_splits

    def solve2(self) -> int:
        beams = {self.__start: 1}
        for i in range(1, len(self.__map)):
            new_beams: dict[int, int] = defaultdict(int)
            for beam, num_paths in beams.items():
                if self.__map[i][beam] == "^":
                    new_beams[beam - 1] += num_paths
                    new_beams[beam + 1] += num_paths
                else:
                    new_beams[beam] += num_paths
            beams = new_beams
        return sum(beams.values())


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
