#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import lru_cache
import numpy as np

from day import Day


class Day07(Day):
    def __init__(self) -> None:
        super().__init__(7)

    def parse_data(self) -> np.ndarray:
        return np.array(self.raw_data[0].split(","), dtype=int)

    def part_1(self) -> int:
        position = np.median(self.data)
        costs = np.abs(position - self.data)
        return costs.sum()

    @property
    def part_1_solution(self) -> int:
        return 356958

    def part_2(self) -> int:
        def calculate_cost(position: int) -> int:
            distance = np.abs(position - self.data)
            return int(sum([Day07.crab_cost(cost) for cost in distance]))

        position = np.median(self.data)
        previous_cost = calculate_cost(position - 1)
        cost = calculate_cost(position)
        direction = 1 if cost < previous_cost else -1
        previous_cost = cost
        while True:
            position += direction
            cost = calculate_cost(position)
            if cost > previous_cost:
                break
            previous_cost = cost

        return previous_cost

    @staticmethod
    @lru_cache
    def crab_cost(distance: int) -> int:
        if distance % 2 == 0:
            return (distance + 1) * distance // 2
        return (distance + 1) * (distance // 2) + int(np.ceil(distance / 2))

    @property
    def part_2_solution(self) -> int:
        return 105461913
