#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

import numpy as np

from day import Day

brackets = {")": "(", "]": "[", "}": "{", ">": "<"}


class Day10(Day):
    def __init__(self) -> None:
        super().__init__(10)

    def parse_data(self) -> List[str]:
        return self.raw_data

    def part_1(self) -> int:
        score = 0
        points = {")": 3, "]": 57, "}": 1197, ">": 25137}
        for line in self.data:
            open_brackets = []
            for character in line:
                if character not in brackets:
                    open_brackets.append(character)
                    continue

                last_open_bracket = open_brackets.pop()
                if brackets[character] != last_open_bracket:
                    score += points[character]
                    break

        return score

    @property
    def part_1_solution(self) -> int:
        return 392043

    def part_2(self) -> int:
        scores = []
        points = {"(": 1, "[": 2, "{": 3, "<": 4}
        for line in self.data:
            open_brackets = []
            for character in line:
                if character not in brackets:
                    open_brackets.append(character)
                    continue

                last_open_bracket = open_brackets.pop()
                if brackets[character] != last_open_bracket:
                    break
            else:
                score = 0
                for bracket in reversed(open_brackets):
                    score *= 5
                    score += points[bracket]
                scores.append(score)

        return int(np.median(scores))

    @property
    def part_2_solution(self) -> int:
        return 1605968119
