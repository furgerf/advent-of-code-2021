#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from typing import Dict, Iterator, List, Optional, Tuple

import numpy as np

from day import Day


class Scanner:
    def __init__(self, number: int, beacons: List[np.ndarray]) -> None:
        self._number = number
        self._beacons = beacons
        self._absolute_position: Optional[np.ndarray] = None
        self._relative_beacon_positions = self._calculate_relative_beacon_positions()

    @property
    def beacons(self):
        return self._beacons

    @property
    def has_known_absolute_position(self) -> bool:
        return self.absolute_position is not None

    @property
    def absolute_position(self) -> Optional[np.ndarray]:
        return self._absolute_position

    @property
    def relative_beacon_positions(self) -> Dict:
        return self._relative_beacon_positions

    @absolute_position.setter
    def absolute_position(self, new_value: np.ndarray) -> None:
        self._absolute_position = new_value

    def distance_to_scanner(self, other_scanner: "Scanner") -> int:
        return abs(self.absolute_position - other_scanner.absolute_position).sum()

    @staticmethod
    def parse(lines: List[str]) -> Iterator["Scanner"]:
        current_scanner_number = 0
        current_beacons = []

        def build_scanner():
            nonlocal current_scanner_number, current_beacons
            scanner = Scanner(current_scanner_number, current_beacons)
            current_scanner_number += 1
            current_beacons = []
            return scanner

        for line in lines:
            if "scanner" in line:
                continue
            if not line:
                yield build_scanner()
                continue
            current_beacons.append(np.array([int(coordinate) for coordinate in line.split(",")]))
        yield build_scanner()

    @staticmethod
    def _rotate_coordinate(
        coordinate: np.ndarray, sign: np.ndarray, permutation: Tuple[int, int, int]
    ) -> Tuple[int, int, int]:
        modified_coordinate = sign * coordinate
        return (
            modified_coordinate[permutation[0]].item(),
            modified_coordinate[permutation[1]].item(),
            modified_coordinate[permutation[2]].item(),
        )

    def try_correlate(self, other: "Scanner") -> bool:
        other_relative_beacon_positions = set(other.relative_beacon_positions.keys())
        for permutation in itertools.permutations(range(3)):
            for sign_tuple in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]:
                sign = np.array(sign_tuple)
                own_relative_positions_that_match = [
                    k
                    for k in self.relative_beacon_positions.keys()
                    if Scanner._rotate_coordinate(k, sign, permutation) in other_relative_beacon_positions
                ]

                if len(own_relative_positions_that_match) < 132:
                    continue

                different_absolute_positions = set()
                for own_relative_position in own_relative_positions_that_match[:3]:
                    own_a, own_b = self.relative_beacon_positions[own_relative_position]
                    cs_other_own_a = np.array(Scanner._rotate_coordinate(own_a, sign, permutation))
                    cs_other_own_b = np.array(Scanner._rotate_coordinate(own_b, sign, permutation))
                    cs_other_other_a, cs_other_other_b = other.relative_beacon_positions[
                        Scanner._rotate_coordinate(own_relative_position, sign, permutation)
                    ]
                    if all(cs_other_own_b - cs_other_own_a == cs_other_other_a - cs_other_other_b):
                        cs_other_other_a, cs_other_other_b = cs_other_other_b, cs_other_other_a
                    different_absolute_positions.add(tuple((cs_other_other_a - cs_other_own_a).tolist()))

                if len(different_absolute_positions) == 1:
                    self.absolute_position = np.array(different_absolute_positions.pop())
                else:
                    sign *= -1
                    self.absolute_position = cs_other_other_a + cs_other_own_b

                self._rotate_beacons(sign, permutation)

                return True

        return False

    def _calculate_relative_beacon_positions(self) -> Dict:
        relative_beacon_positions = {}
        for a, b in itertools.combinations(self._beacons, 2):
            relative_beacon_positions[tuple((a - b).tolist())] = (a, b)
            relative_beacon_positions[tuple((b - a).tolist())] = (a, b)
        return relative_beacon_positions

    def _rotate_beacons(self, sign: np.ndarray, permutation: Tuple[int, int, int]) -> None:
        rotated_beacons = []
        for beacon in self._beacons:
            rotated_beacons.append(
                np.array(Scanner._rotate_coordinate(beacon, sign, permutation)) + self.absolute_position
            )
        self._beacons = rotated_beacons
        self._relative_beacon_positions = self._calculate_relative_beacon_positions()


class Day19(Day):
    def __init__(self) -> None:
        super().__init__(19)

    def parse_data(self) -> List[Scanner]:
        return list(Scanner.parse(self.raw_data))

    def _determine_absolute_positions(self) -> None:
        self.data[0].absolute_position = (0, 0, 0)
        known_scanners = [self.data[0]]

        for _ in range(len(self.data)):
            for scanner in self.data:
                if scanner.has_known_absolute_position:
                    continue

                for known_scanner in known_scanners:
                    if scanner.try_correlate(known_scanner):
                        known_scanners.append(scanner)
                        break

            if len(known_scanners) == len(self.data):
                break

        assert len(known_scanners) == len(self.data), "the absolute position of every scanner was determined"

    def part_1(self) -> int:
        self._determine_absolute_positions()
        absolute_beacon_positions = set()
        for scanner in self.data:
            for beacon in scanner.beacons:
                absolute_beacon_positions.add(tuple(beacon.tolist()))

        return len(absolute_beacon_positions)

    @property
    def part_1_solution(self) -> int:
        return 332

    def part_2(self) -> int:
        if not all(scanner.has_known_absolute_position for scanner in self.data):
            self._determine_absolute_positions()
        max_distance = 0
        for a, b in itertools.product(self.data, self.data):
            if a == b:
                continue

            max_distance = max(max_distance, a.distance_to_scanner(b))
        return max_distance

    @property
    def part_2_solution(self) -> int:
        return 8507
