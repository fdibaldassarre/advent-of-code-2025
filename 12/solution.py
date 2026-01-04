#!/usr/bin/env python

Grid = tuple[tuple[int, int], list[int]]

class Solver:

    def __init__(self) -> None:
        self.__shapes_weights = [0] * 6
        self.__grids: list[Grid] = []

    def parse(self, path: str) -> None:
        read_shapes = True
        shape_id = 0
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                if line == "":
                    shape_id += 1
                    if shape_id == 6:
                        read_shapes = False
                    continue
                if read_shapes:
                    for el in line:
                        if el == "#":
                            self.__shapes_weights[shape_id] += 1
                else:
                    size_r, expected_r = line.split(": ")
                    size = tuple(map(int, size_r.split("x", maxsplit=1)))
                    expected = list(map(int, expected_r.split(" ", maxsplit=5)))
                    self.__grids.append((size, expected))

    def __can_trivially_fit(self, grid: Grid) -> bool:
        size, expected = grid
        num_w = size[0] // 3
        num_h = size[1] // 3
        can_slot = num_w * num_h
        tot_expected = sum(expected)
        return can_slot >= tot_expected

    def _cannot_trivally_fit(self, grid: Grid) -> bool:
        size, expected = grid
        space = size[0] * size[1]
        expected_occupied = 0
        for shape_id in range(6):
            expected_occupied += self.__shapes_weights[shape_id] * expected[shape_id]
        return expected_occupied > space

    def solve1(self) -> int:
        can_fit = 0
        for grid in self.__grids:
            if self.__can_trivially_fit(grid):
                can_fit += 1
            elif not self._cannot_trivally_fit(grid):
                raise Exception(f"Cannot check grid: {grid}")
        return can_fit


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)


if __name__ == "__main__":
    main()
