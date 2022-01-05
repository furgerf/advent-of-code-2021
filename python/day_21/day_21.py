#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from day import Day


class DeterministicDie:
    SIDE_COUNT = 100

    def __init__(self):
        self._roll_count = 0

    @property
    def roll_count(self):
        return self._roll_count

    def roll(self) -> int:
        try:
            return 1 + self._roll_count % DeterministicDie.SIDE_COUNT
        finally:
            self._roll_count += 1


@dataclass
class PlayerState:
    position: int
    score: int

    def __hash__(self) -> int:
        return hash((self.position, self.score))


class Day21(Day):
    def __init__(self) -> None:
        super().__init__(21)

    def parse_data(self) -> List[int]:
        return [int(line.split(": ")[1]) - 1 for line in self.raw_data]

    def part_1(self) -> int:
        player_positions = self.data[:]
        scores = [0] * len(player_positions)
        die = DeterministicDie()
        field_count = 10
        while True:
            for i, position in enumerate(player_positions):
                dice_count = die.roll() + die.roll() + die.roll()
                player_positions[i] = (position + dice_count) % field_count
                scores[i] += player_positions[i] + 1
                if scores[i] >= 1000:
                    return scores[(i + 1) % 2] * die.roll_count

    @property
    def part_1_solution(self) -> int:
        return 513936

    def part_2(self) -> int:
        field_count = 10
        universes = {tuple(PlayerState(position, 0) for position in self.data): 1}
        dice_sums = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
        universe_win_counts = [0] * len(self.data)
        while universes:
            new_universes = {}
            for universe, universe_count in universes.items():
                # play player 1
                for dice_sum, count in dice_sums.items():
                    position = (universe[0].position + dice_sum) % field_count
                    score = universe[0].score + position + 1
                    if score >= 21:
                        universe_win_counts[0] += count * universe_count
                        continue
                    new_universe = (PlayerState(position, score), universe[1])
                    if new_universe not in new_universes:
                        new_universes[new_universe] = 0
                    new_universes[new_universe] += count * universe_count

            universes = new_universes
            new_universes = {}
            for universe, universe_count in universes.items():
                # play player 2
                for dice_sum, count in dice_sums.items():
                    position = (universe[1].position + dice_sum) % field_count
                    score = universe[1].score + position + 1
                    if score >= 21:
                        universe_win_counts[1] += count * universe_count
                        continue
                    new_universe = (universe[0], PlayerState(position, score))
                    if new_universe not in new_universes:
                        new_universes[new_universe] = 0
                    new_universes[new_universe] += count * universe_count
            universes = new_universes

        return max(universe_win_counts)

    @property
    def part_2_solution(self) -> int:
        return 105619718613031
