#!/usr/bin/env python
from typing import Generator


class Solver:

    def __init__(self):
        self.ranges: list[tuple[str, str]] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            line = hand.readline().strip()
            for el in line.split(","):
                fst, snd = el.split("-")
                self.ranges.append((fst, snd))

    def _find_invalid_in_range(self, start: str, end: str) -> Generator[int, None, None]:
        if len(start) < len(end):
            yield from self._find_invalid_in_range(start, "9" * len(start))
            yield from self._find_invalid_in_range("1" + "0" * len(start), end)
            return
        N = len(start)
        if N % 2 == 1:
            return
        start_1 = int(start[:N//2])
        end_1 = int(end[:N // 2])
        limit_1 = int(str(start_1) * 2)
        if int(start) <= limit_1 <= int(end):
            yield limit_1
        for invalid_id in range(start_1 + 1, end_1):
            yield int(str(invalid_id) * 2)
        limit_2 = int(str(end_1) * 2)
        if int(start) <= limit_2 <= int(end) and limit_1 != limit_2:
            yield limit_2

    def _find_invalid_in_range_v2(self, start: str, end: str) -> set[int]:
        if len(start) < len(end):
            p1 = self._find_invalid_in_range_v2(start, "9" * len(start))
            p2 = self._find_invalid_in_range_v2("1" + "0" * len(start), end)
            return p1.union(p2)
        N = len(start)
        patterns: set[int] = set()
        for size in range(1, N//2 + 1):
            if N % size != 0:
                continue
            repeats = N // size
            # Get patterns of given size
            start_1 = int(start[:size])
            end_1 = int(end[:size])
            limit_1 = int(str(start_1) * repeats)
            if int(start) <= limit_1 <= int(end):
                patterns.add(limit_1)
            for invalid_id in range(start_1 + 1, end_1):
                patterns.add(int(str(invalid_id) * repeats))
            limit_2 = int(str(end_1) * repeats)
            if int(start) <= limit_2 <= int(end) and limit_1 != limit_2:
                patterns.add(limit_2)
        return patterns

    def solve1(self) -> int:
        total = 0
        for value in self.ranges:
            for invalid_id in self._find_invalid_in_range(value[0], value[1]):
                total += invalid_id
        return total

    def solve2(self) -> int:
        total = 0
        for value in self.ranges:
            for invalid_id in self._find_invalid_in_range_v2(value[0], value[1]):
                total += invalid_id
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
