#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from typing import List, Optional, Tuple

from day import Day


class Day17(Day):
    def __init__(self) -> None:
        super().__init__(17)

    def parse_data(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        _, x_part, y_part = self.raw_data[0].split("=")
        target_x = tuple(int(x) for x in x_part.split(",")[0].split(".."))
        target_y = tuple(int(y) for y in y_part.split(".."))
        return target_x, target_y

    def _trajectory_to_target_area(self, x_velocity: int, y_velocity: int) -> Optional[List[Tuple[int, int]]]:
        assert x_velocity > 0
        trajectory = []
        x_position, y_position = (0, 0)
        while x_position <= self.data[0][1] and y_position >= self.data[1][0]:
            x_position += x_velocity
            y_position += y_velocity
            x_velocity = max(x_velocity - 1, 0)
            y_velocity -= 1
            trajectory.append((x_position, y_position))
            if self.data[0][0] <= x_position <= self.data[0][1] and self.data[1][0] <= y_position <= self.data[1][1]:
                return trajectory
        return None

    def part_1(self) -> int:
        min_x = int((-1 + math.sqrt(1 + 8 * self.data[0][0])) / 2)
        max_y = 0
        for x in range(min_x, 2 * min_x):
            for y in range(100):
                trajectory = self._trajectory_to_target_area(x, y)
                if not trajectory:
                    continue
                max_y = max([point[1] for point in trajectory] + [max_y])
        return max_y

    @property
    def part_1_solution(self) -> int:
        return 4186

    def part_2(self) -> int:
        min_x = int((-1 + math.sqrt(1 + 8 * self.data[0][0])) / 2)
        trajectory_count = 0
        for x in range(min_x, 20 * min_x):
            for y in range(-200, 200):
                trajectory = self._trajectory_to_target_area(x, y)
                if not trajectory:
                    continue
                trajectory_count += 1
        return trajectory_count

    @property
    def part_2_solution(self) -> int:
        return 2709
