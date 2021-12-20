#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import DefaultDict, List, Set, Tuple

from day import Day


class Day12(Day):
    def __init__(self) -> None:
        super().__init__(12)

    def parse_data(self) -> DefaultDict[str, List[str]]:
        result = defaultdict(list)
        for line in self.raw_data:
            key, value = tuple(line.split("-"))
            result[key].append(value)
            result[value].append(key)

        return result

    def part_1(self) -> int:
        open_paths = [["start", dest] for dest in self.data["start"]]
        closed_paths = []
        while open_paths:
            current_path = open_paths.pop()
            for dest in self.data[current_path[-1]]:
                if dest.islower() and dest in current_path:
                    continue

                new_path = current_path + [dest]
                if dest == "end":
                    closed_paths.append(new_path)
                else:
                    open_paths.append(new_path)
        return len(closed_paths)

    @property
    def part_1_solution(self) -> int:
        return 4720

    def part_2(self) -> int:
        open_paths: List[Tuple[Set[str], str, bool]] = [
            (set(["start", dest]), dest, False) for dest in self.data["start"]
        ]
        path_count = 0
        while open_paths:
            current_path, current_location, has_visited_small_cave_twice = open_paths.pop()

            for dest in self.data[current_location]:
                if dest == "end":
                    path_count += 1
                    continue
                if dest == "start":
                    continue

                if has_visited_small_cave_twice and dest.islower() and dest in current_path:
                    continue

                new_path = set(current_path)
                new_path.add(dest)
                open_paths.append(
                    (new_path, dest, has_visited_small_cave_twice or (dest.islower() and dest in current_path))
                )

        return path_count

    @property
    def part_2_solution(self) -> int:
        return 147848
