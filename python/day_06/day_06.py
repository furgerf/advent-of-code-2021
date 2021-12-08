#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import Dict

from day import Day


class Day06(Day):
    def __init__(self) -> None:
        super().__init__(6)

    def parse_data(self) -> Dict[int, int]:
        grouped_timers = defaultdict(int)
        for timer in self.raw_data[0].split(","):
            grouped_timers[int(timer)] += 1
        return grouped_timers

    def part_1(self) -> int:
        return self.simulate_lanternfish(80)

    @property
    def part_1_solution(self) -> int:
        return 394994

    def part_2(self) -> int:
        return self.simulate_lanternfish(256)

    @property
    def part_2_solution(self) -> int:
        return 1765974267455

    def simulate_lanternfish(self, generations: int):
        population = self.data
        for _ in range(generations):
            new_generation = defaultdict(int)
            for timer, count in population.items():
                if timer == 0:
                    new_generation[6] += count
                    new_generation[8] += count
                else:
                    new_generation[timer - 1] += count
            population = new_generation
        return sum(population.values())
