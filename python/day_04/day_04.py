#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Set, Tuple

import numpy as np

from day import Day


class Board:
    def __init__(self, all_numbers: Set[int], rows_columns: List[Set[int]]):
        self.all_numbers = all_numbers
        self.rows_columns = rows_columns

    @property
    def score(self):
        return np.sum(list(self.all_numbers))

    @staticmethod
    def parse(lines: List[str]) -> "Board":
        numbers = np.array([[int(number) for number in line.split()] for line in lines])
        rows_columns = []
        for i in range(numbers.shape[0]):
            rows_columns.append(set(numbers[i]))
            rows_columns.append(set(numbers[:, i]))
        return Board(set(numbers.flatten()), rows_columns)

    def check_number(self, number: int) -> bool:
        has_won = False
        self.all_numbers.discard(number)
        for row_column in self.rows_columns:
            row_column.discard(number)
            if not row_column:
                has_won = True
        return has_won


class Day04(Day):
    def __init__(self) -> None:
        super().__init__(4)

    def parse_data(self) -> Tuple[List[int], List[Board]]:
        numbers = [int(number) for number in self.raw_data[0].split(",")]
        boards = []
        for i in range(2, len(self.raw_data), 6):
            boards.append(Board.parse(self.raw_data[i : i + 5]))
        return (numbers, boards)

    def part_1(self) -> int:
        numbers, boards = self.data
        for number in numbers:
            for board in boards:
                if board.check_number(number):
                    return number * board.score

    @property
    def part_1_solution(self) -> int:
        return 71708

    def part_2(self) -> int:
        numbers, boards = self.data
        boards_indexes = set(range(len(boards)))
        for number in numbers:
            for index, board in enumerate(boards):
                if index not in boards_indexes:
                    continue

                if board.check_number(number):
                    boards_indexes.remove(index)
                    if not boards_indexes:
                        return number * board.score

    @property
    def part_2_solution(self) -> int:
        return 34726
