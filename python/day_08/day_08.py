#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
import numpy as np

from day import Day


class Display:
    def __init__(self, patterns: List[str], outputs: List[str]) -> None:
        self.patterns = patterns
        self.outputs = outputs
        self.wire_to_segment = {}
        self.digit_to_pattern: List[str] = [None] * 10
        self.pattern_to_digit = {}

    def assign_segments_to_digit(self):
        one_pattern = self._get_patterns_by_length(2)[0]
        self.digit_to_pattern[1] = one_pattern
        seven_pattern = self._get_patterns_by_length(3)[0]
        self.digit_to_pattern[7] = seven_pattern
        all_segments = set("abcdefg")
        self.digit_to_pattern[8] = "".join(all_segments)
        self.wire_to_segment["a"] = set(seven_pattern).difference(one_pattern)

        four_pattern = self._get_patterns_by_length(4)[0]
        self.digit_to_pattern[4] = four_pattern
        zero_six_nine_patterns = self._get_patterns_by_length(6)
        four_seven_segments = set(four_pattern).union(seven_pattern)
        nine_pattern = [pattern for pattern in zero_six_nine_patterns if set(pattern).issuperset(four_seven_segments)][
            0
        ]
        zero_six_patterns = set(zero_six_nine_patterns).difference([nine_pattern])
        self.digit_to_pattern[9] = nine_pattern
        self.wire_to_segment["g"] = set(nine_pattern).difference(four_seven_segments)
        self.wire_to_segment["e"] = all_segments.difference(nine_pattern)

        two_three_five_patterns = self._get_patterns_by_length(5)
        three_pattern_without_d = set(one_pattern).union(self.wire_to_segment["a"]).union(self.wire_to_segment["g"])
        three_pattern = [
            pattern for pattern in two_three_five_patterns if set(pattern).issuperset(three_pattern_without_d)
        ][0]
        self.digit_to_pattern[3] = three_pattern
        two_five_patterns = set(two_three_five_patterns).difference([three_pattern])
        self.wire_to_segment["d"] = set(three_pattern).difference(three_pattern_without_d)

        zero_pattern = [pattern for pattern in zero_six_patterns if "".join(self.wire_to_segment["d"]) not in pattern][
            0
        ]
        self.digit_to_pattern[0] = zero_pattern
        six_pattern = [pattern for pattern in zero_six_patterns if "".join(self.wire_to_segment["d"]) in pattern][0]
        self.digit_to_pattern[6] = six_pattern

        two_pattern_without_c = set().union(*self.wire_to_segment.values())
        two_pattern = [pattern for pattern in two_five_patterns if set(pattern).issuperset(two_pattern_without_c)][0]
        self.digit_to_pattern[2] = two_pattern
        self.wire_to_segment["c"] = set(two_pattern).difference(two_pattern_without_c)

        five_pattern = two_five_patterns.difference([two_pattern])
        self.digit_to_pattern[5] = "".join(five_pattern)

        self.wire_to_segment["f"] = set(one_pattern).difference(self.wire_to_segment["c"])
        self.wire_to_segment["b"] = all_segments.difference(*self.wire_to_segment.values())

        for i, pattern in enumerate(self.digit_to_pattern):
            self.pattern_to_digit["".join(sorted(pattern))] = i

    def calculate_output(self):
        digits = [str(self.pattern_to_digit["".join(sorted(pattern))]) for pattern in self.outputs]
        return int("".join(digits))

    def _get_patterns_by_length(self, length: int) -> List[str]:
        return [pattern for pattern in self.patterns if length == len(pattern)]

    @staticmethod
    def parse(line: str) -> "Display":
        patterns, outputs = line.split(" | ")
        return Display(patterns.split(), outputs.split())


class Day08(Day):
    def __init__(self) -> None:
        super().__init__(8)

    def parse_data(self) -> List[Display]:
        return [Display.parse(line) for line in self.raw_data]

    def part_1(self) -> int:
        count = 0
        for display in self.data:
            for digit in display.outputs:
                if len(digit) in [2, 3, 4, 7]:
                    count += 1
        return count

    @property
    def part_1_solution(self) -> int:
        return 294

    def part_2(self) -> int:
        total_sum = 0
        for display in self.data:
            display.assign_segments_to_digit()
            total_sum += display.calculate_output()
        return total_sum

    @property
    def part_2_solution(self) -> int:
        return 973292
