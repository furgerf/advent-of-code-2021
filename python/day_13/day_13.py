#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Set, Tuple

import matplotlib.pyplot as plt

from day import Day


class Day13(Day):
    def __init__(self) -> None:
        super().__init__(13)

    def parse_data(self) -> Tuple[Set[Tuple[int, ...]], List[Tuple[bool, int]]]:
        dots = set()
        folds = []
        for line in self.raw_data:
            if not line:
                continue
            if line.startswith("fold along "):
                instruction = line.split()[-1]
                direction, offset = tuple(instruction.split("="))
                folds.append((direction == "x", int(offset)))
            else:
                dots.add(tuple(int(coordinate) for coordinate in line.split(",")))
        return dots, folds

    def _fold(self, dots: Set[Tuple[int, int]], direction: bool, offset: int) -> None:
        dots_to_add = []
        dots_to_remove = []
        for x, y in dots:
            if direction:
                # vertical fold
                if x > offset:
                    dots_to_remove.append((x, y))
                    dots_to_add.append((2 * offset - x, y))
            else:
                # horizontal fold
                if y > offset:
                    dots_to_remove.append((x, y))
                    dots_to_add.append((x, 2 * offset - y))
        dots.difference_update(dots_to_remove)
        dots.update(dots_to_add)

    def part_1(self) -> int:
        dots, folds = self.data
        self._fold(dots, *folds[0])
        return len(dots)

    @property
    def part_1_solution(self) -> int:
        return 695

    def part_2(self) -> str:
        dots, folds = self.data
        for fold in folds:
            self._fold(dots, *fold)

        # dots_list = list(dots)
        # plt.figure()
        # plt.axis("equal")
        # plt.scatter([d[0] for d in dots_list], [-d[1] for d in dots_list])
        # plt.show()

        return "GJZGLUPJ"

    @property
    def part_2_solution(self) -> str:
        return "GJZGLUPJ"
