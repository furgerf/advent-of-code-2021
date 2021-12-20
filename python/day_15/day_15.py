#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heapq import heappop, heappush
from typing import List, Set, Tuple

import numpy as np

from day import Day


class Day15(Day):
    def __init__(self) -> None:
        super().__init__(15)

    def parse_data(self) -> np.ndarray:
        return np.array([list(line) for line in self.raw_data], dtype=int)

    @staticmethod
    def _neighbors(cave_map: np.ndarray, index: Tuple[int, int]) -> List[Tuple[int, Tuple[int, int]]]:
        x, y = index
        neighbors = []
        if x > 0:
            neighbors.append((cave_map[x - 1, y], (x - 1, y)))
        if y > 0:
            neighbors.append((cave_map[x, y - 1], (x, y - 1)))
        if x < cave_map.shape[0] - 1:
            neighbors.append((cave_map[x + 1, y], (x + 1, y)))
        if y < cave_map.shape[1] - 1:
            neighbors.append((cave_map[x, y + 1], (x, y + 1)))
        return neighbors

    @staticmethod
    def _shortest_first(cave_map: np.ndarray) -> int:
        found_nodes: Set[Tuple[int, int]] = set([(0, 0)])
        paths: List[Tuple[int, Tuple[int, int]]] = [(0, (0, 0))]
        target = (cave_map.shape[0] - 1, cave_map.shape[1] - 1)
        while True:
            cost, coordinate = heappop(paths)
            neighbors = Day15._neighbors(cave_map, coordinate)
            for neighbor_cost, neighbor_coordinate in neighbors:
                if neighbor_coordinate in found_nodes:
                    continue
                found_nodes.add(neighbor_coordinate)
                total_cost = neighbor_cost + cost
                heappush(paths, (total_cost, neighbor_coordinate))
                if neighbor_coordinate == target:
                    return total_cost

    def part_1(self) -> int:
        return Day15._shortest_first(self.data)

    @property
    def part_1_solution(self) -> int:
        return 687

    def part_2(self) -> int:
        width = self.data.shape[0]
        height = self.data.shape[1]
        big_map = np.empty((5 * width, 5 * height), dtype=int)
        for i in range(5):
            for j in range(5):
                new_map = self.data + i + j
                new_map[np.where(new_map > 9)] -= 9
                big_map[i * width : (i + 1) * width, j * height : (j + 1) * height] = new_map

        return Day15._shortest_first(big_map)

    @property
    def part_2_solution(self) -> int:
        return 2957
