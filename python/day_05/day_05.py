#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Set, Tuple

from day import Day


class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def is_aligned(self) -> bool:
        return self.x1 == self.x2 or self.y1 == self.y2

    @property
    def points(self) -> Set[Tuple[int, int]]:
        points = set()
        min_x = min(self.x1, self.x2)
        max_x = max(self.x1, self.x2)
        min_y = min(self.y1, self.y2)
        max_y = max(self.y1, self.y2)
        if self.is_aligned:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    points.add((x, y))
        else:
            dx = (self.x2 - self.x1) / (max_x - min_x)
            dy = (self.y2 - self.y1) / (max_y - min_y)
            for i in range(max_x - min_x + 1):
                points.add((self.x1 + dx * i, self.y1 + dy * i))
        return points

    @staticmethod
    def parse(line: str) -> "Line":
        coordinates = line.split(" -> ")
        start = coordinates[0].split(",")
        end = coordinates[1].split(",")
        return Line(int(start[0]), int(start[1]), int(end[0]), int(end[1]))


class Day05(Day):
    def __init__(self) -> None:
        super().__init__(5)

    def parse_data(self) -> List[Line]:
        return [Line.parse(line) for line in self.raw_data]

    def part_1(self) -> int:
        covered_points = set()
        multiple_covered_points = set()
        for line in self.data:
            if not line.is_aligned:
                continue
            new_points = line.points
            multiple_covered_points.update(covered_points.intersection(new_points))
            covered_points.update(new_points)

        return len(multiple_covered_points)

    @property
    def part_1_solution(self) -> int:
        return 5585

    def part_2(self) -> int:
        covered_points = set()
        multiple_covered_points = set()
        for line in self.data:
            new_points = line.points
            multiple_covered_points.update(covered_points.intersection(new_points))
            covered_points.update(new_points)

        return len(multiple_covered_points)

    @property
    def part_2_solution(self) -> int:
        return 17193
