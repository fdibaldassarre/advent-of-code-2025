#!/usr/bin/env python
from scipy.optimize import linprog


def get_all_combinations(elements: list[int], n_samples: int) -> list[list[int]]:
    if n_samples > len(elements):
        return []
    if n_samples == 0:
        return [[]]
    elif n_samples == 1:
        return [[n] for n in elements]
    else:
        all_combs: list[list[int]] = []
        for i in range(len(elements)):
            sub_combs = get_all_combinations(elements[i+1:], n_samples=n_samples-1)
            for c in sub_combs:
                c.append(elements[i])
            all_combs.extend(sub_combs)
        return all_combs


class Solver:

    class Machine:
        def __init__(self, diagram: list[int], buttons: list[tuple[int, ...]], joltage: list[int]) -> None:
            self.diagram = diagram
            self.buttons = buttons
            self.joltage = joltage

            self.diagram_to_btns: list[list[int]] = [list() for _ in range(len(self.diagram))]
            for i, btn in enumerate(self.buttons):
                for diagram in btn:
                    self.diagram_to_btns[diagram].append(i)


    def __init__(self) -> None:
        self.__machines: list[Solver.Machine] = []

    def parse(self, path: str) -> None:
        with open(path) as hand:
            for line in hand:
                line = line.strip().split(" ")
                diagram_r = line[0][1:-1]
                diagram = [1 if el == "#" else 0 for el in diagram_r]
                buttons_r = line[1:-1]
                buttons = [tuple(map(int, line[1:-1].split(","))) for line in buttons_r]
                joltage_r = line[-1][1:-1]
                joltage = list(map(int, joltage_r.split(",")))
                self.__machines.append(Solver.Machine(diagram, buttons, joltage))

    def _get_min_presses(self, machine: Machine) -> int:
        solutions: list[list[int]] = [[-1] * len(machine.buttons)]
        for i, el in enumerate(machine.diagram):
            bts = machine.diagram_to_btns[i]

            all_combs: list[list[int]] = []
            for n_btns in range(el, len(bts) + 1, 2):
                # Pick n_btns different buttons
                combs = get_all_combinations(bts, n_btns)
                for comb in combs:
                    press = [-1] * len(machine.buttons)
                    for btn in bts:
                        press[btn] = 0
                    for pressed_btn in comb:
                        press[pressed_btn] = 1
                    all_combs.append(press)

            new_solutions: list[list[int]] = []
            for solution in solutions:
                for comb in all_combs:
                    can_be_applied = True
                    for btn, val in enumerate(comb):
                        if val == -1 or solution[btn] == -1:
                            continue
                        if solution[btn] != val:
                            can_be_applied = False
                            break
                    if can_be_applied:
                        new_solution = solution.copy()
                        for btn, val in enumerate(comb):
                            if val != -1:
                                new_solution[btn] = val
                        new_solutions.append(new_solution)
            solutions = new_solutions

        min_cost = None
        for solution in solutions:
            for i in range(len(solution)):
                if solution[i] == -1:
                    solution[i] = 0
            cost = sum(solution)
            if min_cost is None or cost < min_cost:
                min_cost = cost

        return min_cost

    def _get_min_presses_v2(self, machine: Machine) -> int:
        c = [1] * len(machine.buttons)
        A: list[list[int]] = []
        for i in range(len(machine.diagram)):
            row = [0] * len(machine.buttons)
            for btn in machine.diagram_to_btns[i]:
                row[btn] = 1
            A.append(row)
        b = machine.joltage
        res = linprog(c, A_ub=A, b_ub=b, A_eq=A, b_eq=b, method='highs', integrality=1)
        return int(res["fun"])

    def solve1(self) -> int:
        tot_cost = 0
        for machine in self.__machines:
            min_cost = self._get_min_presses(machine)
            tot_cost += min_cost
        return tot_cost

    def solve2(self) -> int:
        tot_cost = 0
        for i, machine in enumerate(self.__machines):
            min_cost = self._get_min_presses_v2(machine)
            tot_cost += min_cost
        return tot_cost


def main():
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)


if __name__ == "__main__":
    main()
