#!/usr/bin/env python


Point = tuple[int, int]


class Solver:

    def __init__(self) -> None:
        self._red_tiles: list[Point] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                val_raw = line.strip().split(",")
                self._red_tiles.append(tuple(map(int, val_raw)))

    def solve1(self) -> int:
        max_area = 0
        for i in range(len(self._red_tiles)):
            a = self._red_tiles[i]
            for j in range(i + 1, len(self._red_tiles)):
                b = self._red_tiles[j]
                area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
                max_area = max(area, max_area)
        return max_area

    def __check_valid(self, a: Point, b: Point,  segments_v: list[tuple[int, int, int]], segments_h: list[tuple[int, int, int]]) -> bool:
        a_n = (min(a[0], b[0]), min(a[1], b[1]))
        b_n = (max(a[0], b[0]), max(a[1], b[1]))
        for segment in segments_h:
            y, x1, x2 = segment
            if a_n[1] < y < b_n[1] and x1 < b_n[0] and x2 > a_n[0]:
                return False
        for segment in segments_v:
            x, y1, y2 = segment
            if a_n[0] < x < b_n[0] and y1 < b_n[1] and y2 > a_n[1]:
                return False
        return True

    def solve2(self) -> int:
        segments_h: list[tuple[int, int, int]] = []
        segments_v: list[tuple[int, int, int]] = []

        for i in range(len(self._red_tiles)):
            a = self._red_tiles[i]
            b = self._red_tiles[(i+1) % len(self._red_tiles)]
            if a[0] == b[0]:
                segments_v.append((a[0], min(a[1], b[1]), max(a[1], b[1])))
            else:
                segments_h.append((a[1], min(a[0], b[0]), max(a[0], b[0])))

        max_area = 0
        for i in range(len(self._red_tiles)):
            a = self._red_tiles[i]
            for j in range(i + 1, len(self._red_tiles)):
                b = self._red_tiles[j]
                if self.__check_valid(a, b, segments_v, segments_h):
                    area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
                    max_area = max(max_area, area)

        return max_area


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
