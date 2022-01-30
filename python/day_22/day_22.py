#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple

import numpy as np

from day import Day

Index = Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]
Instruction = Tuple[int, Index]


class Cube:
    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int) -> None:
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_z = min_z
        self.max_z = max_z

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    @property
    def size(self) -> int:
        return abs(self.max_x + 1 - self.min_x) * abs(self.max_y + 1 - self.min_y) * abs(self.max_z + 1 - self.min_z)

    def get_remainder(self, other: "Cube") -> Optional[List["Cube"]]:
        overlap = self._get_overlap(other)
        if overlap is None or overlap.is_empty:
            return None

        remainder = []

        x_left = (other.min_x, overlap.min_x - 1)
        x_same = (overlap.min_x, overlap.max_x)
        x_right = (overlap.max_x + 1, other.max_x)
        y_front = (other.min_y, overlap.min_y - 1)
        y_same = (overlap.min_y, overlap.max_y)
        y_back = (overlap.max_y + 1, other.max_y)
        z_under = (other.min_z, overlap.min_z - 1)
        z_same = (overlap.min_z, overlap.max_z)
        z_above = (overlap.max_z + 1, other.max_z)

        # below
        remainder.append(Cube(other.min_x, other.max_x, other.min_y, other.max_y, *z_under))
        # above
        remainder.append(Cube(other.min_x, other.max_x, other.min_y, other.max_y, *z_above))
        # edges
        remainder.append(Cube(*x_left, *y_same, *z_same))
        remainder.append(Cube(*x_right, *y_same, *z_same))
        remainder.append(Cube(*x_same, *y_front, *z_same))
        remainder.append(Cube(*x_same, *y_back, *z_same))
        # corners
        remainder.append(Cube(*x_left, *y_front, *z_same))
        remainder.append(Cube(*x_left, *y_back, *z_same))
        remainder.append(Cube(*x_right, *y_front, *z_same))
        remainder.append(Cube(*x_right, *y_back, *z_same))

        result = [r for r in remainder if not r.is_empty]
        return result

    def _get_overlap(self, other: "Cube") -> Optional["Cube"]:
        if self.min_x > other.max_x or self.max_x < other.min_x:
            return None
        if self.min_y > other.max_y or self.max_y < other.min_y:
            return None
        if self.min_z > other.max_z or self.max_z < other.min_z:
            return None
        return Cube(
            max(self.min_x, other.min_x),
            min(self.max_x, other.max_x),
            max(self.min_y, other.min_y),
            min(self.max_y, other.max_y),
            max(self.min_z, other.min_z),
            min(self.max_z, other.max_z),
        )

    def __repr__(self) -> str:
        return f"Cube(x={self.min_x}..{self.max_x}, y={self.min_y}..{self.max_y}, z={self.min_z}..{self.max_z})"


class Day22(Day):
    def __init__(self) -> None:
        super().__init__(22)

    def parse_data(self) -> List[Instruction]:
        def parse_line(line: str) -> Instruction:
            state = int(line.startswith("on "))
            split = line[line.index(" ") + 1 :].split(",")

            def parse_coordinate(coordinate) -> Tuple[int, int]:
                min_c, max_c = coordinate[coordinate.index("=") + 1 :].split("..")
                return int(min_c), int(max_c)

            return state, tuple(parse_coordinate(coordinate) for coordinate in split)

        return [parse_line(line) for line in self.raw_data]

    def part_1(self) -> int:
        reactor = np.full((100, 100, 100), 0, dtype=np.uint8)
        for state, ((min_x, max_x), (min_y, max_y), (min_z, max_z)) in self.data:
            reactor[min_x + 50 : max_x + 50 + 1, min_y + 50 : max_y + 50 + 1, min_z + 50 : max_z + 50 + 1] = state

        return reactor.sum()

    @property
    def part_1_solution(self) -> int:
        return 583641

    def part_2(self) -> int:
        cubes = []
        for i, (state, (x, y, z)) in enumerate(self.data):
            current_cube = Cube(*x, *y, *z)
            if state:
                current_cubes = [current_cube]
                while current_cubes:
                    current_cube = current_cubes.pop()
                    for cube in cubes:
                        remainder = cube.get_remainder(current_cube)
                        if remainder is None:
                            continue
                        current_cubes.extend(remainder)
                        break
                    else:
                        cubes.append(current_cube)
            else:
                new_cubes = []
                for cube in cubes:
                    remainder = current_cube.get_remainder(cube)
                    if remainder is None:
                        new_cubes.append(cube)
                        continue
                    new_cubes.extend(remainder)
                cubes = new_cubes

        return sum(cube.size for cube in cubes)

    @property
    def part_2_solution(self) -> int:
        return 1182153534186233
