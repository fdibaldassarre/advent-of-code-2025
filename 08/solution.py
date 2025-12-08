#!/usr/bin/env python
import heapq

Point = tuple[int, int, int]


def l2_distance(a: Point, b: Point) -> int:
    return sum((a[i] - b[i]) ** 2 for i in range(3))


class Solver:

    def __init__(self) -> None:
        self.__boxes: list[Point] = []
        self.__distances: list[tuple[int, Point, Point]] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip().split(",")
                self.__boxes.append(tuple(map(int, line)))

        self.__distances = []
        for i in range(len(self.__boxes)):
            a = self.__boxes[i]
            for j in range(i + 1, len(self.__boxes)):
                b = self.__boxes[j]
                d = l2_distance(a, b)
                self.__distances.append((d, a, b))
        self.__distances.sort(key=lambda el: el[0])

    def _get_connected_components(self, num_to_connect: int) -> tuple[list[set[Point]], tuple[Point, Point]]:
        distances = []
        heapq.heapify(distances)
        for i in range(len(self.__boxes)):
            a = self.__boxes[i]
            for j in range(i + 1, len(self.__boxes)):
                b = self.__boxes[j]
                d = l2_distance(a, b)
                heapq.heappush(distances, (d, a, b))

        connections: dict[Point, set[Point]] = dict()
        last_connected: tuple[Point, Point]

        for i in range(num_to_connect):
            _, a, b = self.__distances[i]
            if a not in connections:
                connections[a] = set()
            if b not in connections:
                connections[b] = set()
            connections[a].add(b)
            connections[b].add(a)
            last_connected = (a, b)

        components: list[set[Point]] = []
        remaining_boxes: set[Point] = set(self.__boxes)
        while len(remaining_boxes) > 0:
            # Extract a new component
            box = remaining_boxes.pop()
            current_component = {box}
            current_component_border = {box}
            while len(current_component_border) > 0:
                source = current_component_border.pop()
                if source not in connections:
                    continue
                for target in connections[source]:
                    if target not in current_component:
                        current_component.add(target)
                        current_component_border.add(target)
                        remaining_boxes.remove(target)
            components.append(current_component)

        return components, last_connected

    def solve1(self) -> int:
        components, _ = self._get_connected_components(1000)
        components.sort(key=lambda el: len(el), reverse=True)
        total = 1
        for component in components[:3]:
            total *= len(component)
        return total

    def solve2(self) -> int:
        left = 0
        right = (len(self.__boxes) * len(self.__boxes) - 1) // 2
        while left < right - 1:
            mid = (left + right) // 2
            connected, _ = self._get_connected_components(mid)
            if len(connected) > 1:
                left = mid
            else:
                right = mid
        _, last_connected = self._get_connected_components(right)
        a, b = last_connected

        return a[0] * b[0]


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()  # 28th iteration
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
