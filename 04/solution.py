#!/usr/bin/env python
import heapq
from typing import Generator

Point = tuple[int, int]


class Solver:

    class PaperMap:

        def __init__(self) -> None:
            self.__values: dict[Point, int] = dict()
            self.__accessible: set[Point] = set()

        def add(self, x: int, y: int, papers: int) -> None:
            self.__values[(x, y)] = papers
            if papers < 4:
                self.__accessible.add((x, y))

        def pop(self, x: int, y: int) -> None:
            point = (x, y)
            if point in self.__values:
                self.__values[point] -= 1
                if self.__values[point] < 4:
                    self.__accessible.add(point)

        def get_accessible(self) -> Point | None:
            if len(self.__accessible) > 0:
                point = self.__accessible.pop()
                del self.__values[point]
                return point
            return None

    def __init__(self) -> None:
        self._map: list[str] = []
        self._width = -1
        self._height = -1

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for i, line in enumerate(hand):
                self._map.append(line.strip())
        self._width = len(self._map[0])
        self._height = len(self._map)

    def _get_neighbours(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        for dx, dy in [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self._width and 0 <= ny < self._height:
                yield nx, ny

    def __get_neighbour_papers(self, x: int, y: int) -> int:
        papers = 0
        for nx, ny in self._get_neighbours(x, y):
            if self._map[ny][nx] == "@":
                papers += 1
        return papers

    def solve1(self) -> int:
        accessible = 0
        for y in range(self._height):
            for x in range(self._width):
                if self._map[y][x] == "@":
                    papers = self.__get_neighbour_papers(x, y)
                    if papers < 4:
                        accessible += 1
        return accessible

    def solve2(self) -> int:
        rolls = Solver.PaperMap()
        for y in range(self._height):
            for x in range(self._width):
                if self._map[y][x] == "@":
                    papers = self.__get_neighbour_papers(x, y)
                    rolls.add(x, y, papers=papers)
        removable = 0
        while (next_accessible := rolls.get_accessible()) is not None:
            for nx, ny in self._get_neighbours(*next_accessible):
                rolls.pop(nx, ny)
            removable += 1
        return removable


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
