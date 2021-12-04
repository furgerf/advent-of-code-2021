#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from day import Day


class DayXXX(Day):
    def __init__(self) -> None:
        super().__init__(XXX)

    def parse_data(self) -> np.ndarray:
        return np.array(self.raw_data)

    def part_1(self) -> int:
        pass

    @property
    def part_1_solution(self) -> int:
        return None

    def part_2(self) -> int:
        pass

    @property
    def part_2_solution(self) -> int:
        return None
