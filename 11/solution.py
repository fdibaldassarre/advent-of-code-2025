#!/usr/bin/env python

Path = tuple[str,bool,bool]

class Solver:

    def __init__(self) -> None:
        self.__paths: dict[str, list[str]] = {}

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip()
                source, targets_raw = line.split(": ", maxsplit=2)
                targets = targets_raw.split(" ")
                self.__paths[source] = targets

    def solve1(self) -> int:
        border = {"you": 1}
        out_paths = 0
        while len(border) > 0:
            current = next(iter(border))
            num_paths = border[current]
            del border[current]
            if current == "out":
                out_paths += num_paths
                continue
            for target in self.__paths[current]:
                if target not in border:
                    border[target] = 0
                border[target] += num_paths
        return out_paths

    def solve2(self) -> int:
        border: dict[Path, int] = {("svr",False,False): 1}
        out_paths = 0
        while len(border) > 0:
            path = next(iter(border))
            last_el, visited_dac, visited_fft = path
            num_paths = border[path]
            del border[path]
            if last_el == "out":
                if visited_dac and visited_fft:
                    out_paths += num_paths
                continue
            if last_el == "dac":
                visited_dac = True
            if last_el == "fft":
                visited_fft = True
            for target in self.__paths[last_el]:
                path_idx = (target, visited_dac, visited_fft)
                if path_idx not in border:
                    border[path_idx] = 0
                border[path_idx] += num_paths
        return out_paths


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
