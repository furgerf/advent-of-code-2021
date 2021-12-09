#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple
import numpy as np

from day import Day


class Day09(Day):
    def __init__(self) -> None:
        super().__init__(9)

    def parse_data(self) -> np.ndarray:
        return np.array([list(line) for line in self.raw_data], dtype=int)

    def part_1(self) -> int:
        risk_level = 0
        for index, value in np.ndenumerate(self.data):
            if value < min(self._neighbors(index)[0]):
                risk_level += value + 1
        return risk_level

    def _neighbors(self, index: Tuple[int, int]) -> Tuple[List[int], List[Tuple[int, int]]]:
        x, y = index
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if x < self.data.shape[0] - 1:
            neighbors.append((x + 1, y))
        if y < self.data.shape[1] - 1:
            neighbors.append((x, y + 1))
        return [self.data[index] for index in neighbors], neighbors

    @property
    def part_1_solution(self) -> int:
        return 500

    def part_2(self) -> int:
        basin_sizes = []
        for index, value in np.ndenumerate(self.data):
            neighbors, indexes = self._neighbors(index)
            if value >= min(neighbors):
                continue

            basin = set()
            neighbors_to_check = set()
            for i in range(len(neighbors)):
                if neighbors[i] == 9:
                    continue

                basin.add(indexes[i])
                neighbors_to_check.add(indexes[i])

            while neighbors_to_check:
                neighbor_index = neighbors_to_check.pop()
                new_neighbors, new_indexes = self._neighbors(neighbor_index)
                for i in range(len(new_neighbors)):
                    if new_neighbors[i] == 9:
                        continue
                    if new_indexes[i] in basin:
                        continue

                    neighbors_to_check.add(new_indexes[i])
                    basin.add(new_indexes[i])

            basin_sizes.append(len(basin))

        return np.prod(sorted(basin_sizes, reverse=True)[:3])

    @property
    def part_2_solution(self) -> int:
        return 970200
