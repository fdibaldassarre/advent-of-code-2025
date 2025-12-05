#!/usr/bin/env python


class Solver:

    def __init__(self) -> None:
        self._fresh: list[tuple[int, int]] = []
        self._ingredients: list[int] = []

    def parse(self, path: str) -> None:
        parse_ingredients = False
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                if line == "":
                    parse_ingredients = True
                    continue
                if parse_ingredients:
                    self._ingredients.append(int(line))
                else:
                    start, end = line.split("-")
                    self._fresh.append((int(start), int(end)))

    def solve1(self) -> int:
        fresh_ingredients = 0
        for ingredient in self._ingredients:
            for start, end in self._fresh:
                if start <= ingredient <= end:
                    fresh_ingredients += 1
                    break
        return fresh_ingredients

    def solve2(self) -> int:
        ranges_sorted = sorted(self._fresh)
        non_overlapping = [list(ranges_sorted[0])]
        for i in range(1, len(ranges_sorted)):
            start, end = ranges_sorted[i]
            if start <= non_overlapping[-1][1]:
                # Extend the existing interval
                non_overlapping[-1][1] = max(non_overlapping[-1][1], end)
            else:
                non_overlapping.append([start, end])
        total_fresh = 0
        for start, end in non_overlapping:
            total_fresh += end - start + 1
        return total_fresh


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
