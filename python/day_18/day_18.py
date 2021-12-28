#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from math import ceil, floor
from typing import List, Optional, Tuple, Union

from day import Day


class SnailfishNumber:
    def __init__(self, left: Union["SnailfishNumber" , int], right: Union["SnailfishNumber" , int]) -> None:
        self.left = left
        self.right = right
        self._parent: Optional[SnailfishNumber] = None

    @property
    def magnitude(self) -> int:
        magnitude_left = self.left if isinstance(self.left, int) else self.left.magnitude
        magnitude_right = self.right if isinstance(self.right, int) else self.right.magnitude
        return 3 * magnitude_left + 2 * magnitude_right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_value):
        self._left = new_value
        if isinstance(self._left, SnailfishNumber):
            self._left.set_parent(self)

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_value):
        self._right = new_value
        if isinstance(self._right, SnailfishNumber):
            self._right.set_parent(self)

    def set_parent(self, parent: "SnailfishNumber") -> None:
        self._parent = parent

    def reduce(self) -> None:
        while True:
            if self.try_explode(0):
                continue
            if self.try_split():
                continue
            break

    def try_explode(self, level: int) -> bool:
        if level != 3:
            if isinstance(self.left, SnailfishNumber):
                if self.left.try_explode(level+1):
                    return True
            if isinstance(self.right, SnailfishNumber):
                if self.right.try_explode(level+1):
                    return True
            return False

        if isinstance(self.left, SnailfishNumber):
            self.explode_left()
            return True
        if isinstance(self.right, SnailfishNumber):
            self.explode_right()
            return True

        return False

    def explode_left(self):
        assert isinstance(self.left.left, int) and isinstance(self.left.right, int)
        # search for first parent where we're the right child
        parent = self
        while parent._parent is not None:
            is_right_child_of_parent = parent == parent._parent.right
            parent = parent._parent
            if not is_right_child_of_parent:
                continue

            # increase the value of the first right that's an int
            # `parent` is now the parent node where we need to add
            if isinstance(parent.left, int):
                # the parent's left node is already an int, add here
                parent.left += self.left.left
            else:
                # we'll look for the rightmost integer that's to the parent's left
                parent = parent.left
                while not isinstance(parent.right, int):
                    parent = parent.right
                parent.right += self.left.left
            break

        # increase the value of the first left to our right that's an int
        if isinstance(self.right, int):
            # our right node is already an int, add here
            self.right += self.left.right
        else:
            # we'll look for the leftmost integer that's to our right
            parent = self.right
            while not isinstance(parent.left, int):
                parent = parent.left
            parent.left += self.left.right
        self.left = 0

    def explode_right(self):
        assert isinstance(self.right.right, int) and isinstance(self.right.left, int)
        # search for first parent where we're the left child
        parent = self
        while parent._parent is not None:
            is_left_child_of_parent = parent == parent._parent.left
            parent = parent._parent
            if not is_left_child_of_parent:
                continue

            # increase the value of the first left that's an int
            # `parent` is now the parent node where we need to add
            if isinstance(parent.right, int):
                # the parent's right node is already an int, add here
                parent.right += self.right.right
            else:
                # we'll look for the leftmost integer that's to the parent's right
                parent = parent.right
                while not isinstance(parent.left, int):
                    parent = parent.left
                parent.left += self.right.right
            break

        # increase the value of the first right to our left that's an int
        if isinstance(self.left, int):
            # our left node is already an int, add here
            self.left += self.right.left
        else:
            # we'll look for the rightmost integer that's to our left
            parent = self.left
            while not isinstance(parent.right, int):
                parent = parent.right
            parent.right += self.right.left
        self.right = 0

    def try_split(self) -> bool:
        if isinstance(self.left, int) and self.left > 9:
            self.left = SnailfishNumber(floor(self.left/2), ceil(self.left/2))
            return True
        if isinstance(self.left, SnailfishNumber) and self.left.try_split():
            return True
        if isinstance(self.right, int) and self.right > 9:
            self.right = SnailfishNumber(floor(self.right/2), ceil(self.right/2))
            return True
        if isinstance(self.right, SnailfishNumber) and self.right.try_split():
            return True
        return False

    def __add__(self, other: "SnailfishNumber") -> "SnailfishNumber":
        assert self._parent is None and other._parent is None
        result = SnailfishNumber(self, other)
        result.reduce()
        return result

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"

    def clone(self) -> "SnailfishNumber":
        return SnailfishNumber.parse(str(self))

    @staticmethod
    def parse(line: str) -> "SnailfishNumber":
        raw_fish = Union[SnailfishNumber , Optional[int]]
        open_numbers: List[Tuple[raw_fish, raw_fish]] = []
        result = None
        for character in line:
            assert result is None
            match character:
                case "[":
                    # start of new SN
                    open_numbers.append((None, None))
                case ",":
                    assert open_numbers[-1][0] is not None
                case "]":
                    left, right = open_numbers.pop()
                    new_number = SnailfishNumber(left, right)
                    if not open_numbers:
                        result = new_number
                    elif open_numbers[-1][0] is None:
                        open_numbers[-1] = (new_number, None)
                    else:
                        open_numbers[-1] = (open_numbers[-1][0], new_number)
                case _:
                    if open_numbers[-1][0] is None:
                        open_numbers[-1] = (int(character), None)
                    else:
                        open_numbers[-1] = (open_numbers[-1][0], int(character))

        assert not open_numbers and result is not None
        return result

class Day18(Day):
    def __init__(self) -> None:
        super().__init__(18)

    def parse_data(self) -> List[SnailfishNumber]:
        return [SnailfishNumber.parse(line) for line in self.raw_data]

    def part_1(self) -> int:
        result = self.data[0].clone()
        for i in range(1, len(self.data)):
            result += self.data[i].clone()
        return result.magnitude

    @property
    def part_1_solution(self) -> int:
        return 4235

    def part_2(self) -> int:
        max_magnitude = 0
        for a, b in itertools.product(self.data, self.data):
            if a == b:
                continue
            max_magnitude = max(max_magnitude, (a.clone() + b.clone()).magnitude)
        return max_magnitude

    @property
    def part_2_solution(self) -> int:
        return 4659
