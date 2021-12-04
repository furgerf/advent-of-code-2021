#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from day import Day


class Day03(Day):
    def __init__(self) -> None:
        super().__init__(3)

    def parse_data(self) -> np.ndarray:
        return np.array([list(line) for line in self.raw_data], dtype=int)

    def part_1(self) -> int:
        bits = np.median(self.data, axis=0).astype(int)
        gamma = Day03._parse_binary(bits)
        epsilon = Day03._parse_binary(np.bitwise_xor(bits, np.ones_like(bits)))
        return gamma * epsilon

    @property
    def part_1_solution(self) -> int:
        return 2648450

    def part_2(self) -> int:
        oxygen_values = self.data
        co2_values = self.data
        for i in range(self.data.shape[1]):
            if len(oxygen_values) > 1:
                target_value = np.ceil(np.median(oxygen_values[:, i]))
                oxygen_values = oxygen_values[oxygen_values[:, i] == target_value]
            if len(co2_values) > 1:
                target_value = 1 - np.ceil(np.median(co2_values[:, i]))
                co2_values = co2_values[co2_values[:, i] == target_value]
        return Day03._parse_binary(oxygen_values[0]) * Day03._parse_binary(co2_values[0])

    @property
    def part_2_solution(self) -> int:
        return 2845944

    @staticmethod
    def _parse_binary(bits: np.ndarray) -> int:
        return int("".join(bits.astype(str).tolist()), 2)
