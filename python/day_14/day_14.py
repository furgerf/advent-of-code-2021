#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Dict, Tuple

from day import Day


class Day14(Day):
    def __init__(self) -> None:
        super().__init__(14)

    def parse_data(self) -> Tuple[str, Dict[str, str]]:
        template = self.raw_data[0]
        rules = dict(tuple(line.split(" -> ")) for line in self.raw_data[2:])  # type: ignore
        return template, rules

    def _apply_steps(self, step_count: int) -> int:
        template, rules = self.data
        combinations = defaultdict(int)
        for pair in zip(template, template[1:]):
            combinations["".join(pair)] += 1
        for _ in range(step_count):
            new_combinations = defaultdict(int)
            for combination, count in combinations.items():
                middle = rules[combination]
                new_combinations[combination[0] + middle] += count
                new_combinations[middle + combination[1]] += count
            combinations = new_combinations

        character_counts = defaultdict(int)
        for combination, count in combinations.items():
            character_counts[combination[0]] += count
        character_counts[template[-1]] += 1
        counts = sorted(character_counts.values())
        return counts[-1] - counts[0]

    def part_1(self) -> int:
        return self._apply_steps(10)

    @property
    def part_1_solution(self) -> int:
        return 2170

    def part_2(self) -> int:
        return self._apply_steps(40)

    @property
    def part_2_solution(self) -> int:
        return 2422444761283
