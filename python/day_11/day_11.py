#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple

import numpy as np

from day import Day


class Day11(Day):
    def __init__(self) -> None:
        super().__init__(11)

    def parse_data(self) -> np.ndarray:
        return np.array([list(line) for line in self.raw_data], dtype=int)

    @staticmethod
    def _flash(own_data: np.ndarray, x: int, y: int) -> List[Tuple[int, int]]:
        triggered_flashes = []
        for i in range(max(x - 1, 0), min(x + 2, own_data.shape[0])):
            for j in range(max(y - 1, 0), min(y + 2, own_data.shape[1])):
                if own_data[i, j] == 9:
                    triggered_flashes.append((i, j))
                own_data[i, j] += 1
        return triggered_flashes

    def part_1(self) -> int:
        flash_count = 0
        own_data = np.array(self.data)
        for _ in range(100):
            for index, _ in np.ndenumerate(own_data):
                own_data[index] += 1
                if own_data[index] == 10:
                    additional_flashes = Day11._flash(own_data, *index)
                    flash_count += 1 + len(additional_flashes)
                    while additional_flashes:
                        even_more_flashes = Day11._flash(own_data, *additional_flashes.pop())
                        flash_count += len(even_more_flashes)
                        additional_flashes.extend(even_more_flashes)

            own_data[np.where(own_data > 9)] = 0
        return flash_count

    @property
    def part_1_solution(self) -> int:
        return 1591

    def part_2(self) -> int:
        step = 0
        own_data = np.array(self.data)
        while own_data.max() > 0:
            for index, _ in np.ndenumerate(own_data):
                own_data[index] += 1
                if own_data[index] == 10:
                    additional_flashes = Day11._flash(own_data, *index)
                    while additional_flashes:
                        even_more_flashes = Day11._flash(own_data, *additional_flashes.pop())
                        additional_flashes.extend(even_more_flashes)

            own_data[np.where(own_data > 9)] = 0
            step += 1
        return step

    @property
    def part_2_solution(self) -> int:
        return 314
