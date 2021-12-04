#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from day import Day


class Day01(Day):
    def __init__(self) -> None:
        super().__init__(1)

    def parse_data(self) -> np.ndarray:
        return np.array(self.raw_data, dtype=np.int)

    def part_1(self) -> int:
        return Day01._count_increases(self.data)

    @property
    def part_1_solution(self) -> int:
        return 1390

    def part_2(self) -> int:
        windows = sliding_window_view(self.data, 3)
        summed_windows = windows.sum(axis=1)
        return Day01._count_increases(summed_windows)

    @property
    def part_2_solution(self) -> int:
        return 1457

    @staticmethod
    def _count_increases(data: np.ndarray) -> int:
        return len(np.where(np.diff(data) > 0)[0])
