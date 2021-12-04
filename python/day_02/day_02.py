#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Tuple
import numpy as np

from day import Day


class Day02(Day):
    def __init__(self) -> None:
        super().__init__(2)

    def parse_data(self) -> np.ndarray:
        def parse_line(line: str) -> Tuple[int, int]:
            direction, amount_str = line.split()
            amount = int(amount_str)
            if direction == "forward":
                return (amount, 0)
            if direction == "down":
                return (0, amount)
            if direction == "up":
                return (0, -amount)
            assert False

        return np.array([parse_line(line) for line in self.raw_data])

    def part_1(self) -> int:
        return self.data.sum(axis=0).prod()

    @property
    def part_1_solution(self) -> int:
        return 2147104

    def part_2(self) -> int:
        aim = 0
        depth = 0
        for command in self.data:
            aim += command[1]
            depth += aim * command[0]
        return depth * self.data[:, 0].sum()

    @property
    def part_2_solution(self) -> int:
        return 2044620088
