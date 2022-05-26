#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum
from typing import Dict, List, Optional, Tuple

import numpy as np

from day import Day


class AmphipodType(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3

    def __repr__(self) -> str:
        return self.name


class Amphipod:
    _created_amphipod_types = set()

    def __init__(self, amphipod_type: AmphipodType) -> None:
        self.amphipod_type = amphipod_type
        self.name = (
            self.amphipod_type.name
            if amphipod_type in Amphipod._created_amphipod_types
            else self.amphipod_type.name.lower()
        )
        Amphipod._created_amphipod_types.add(amphipod_type)

    def __repr__(self) -> str:
        return self.name


class Map:
    def __init__(self):
        self.spots_left: List[Optional[Amphipod]] = [None, None]
        self.spots_right: List[Optional[Amphipod]] = [None, None]
        self.spots_middle: List[Optional[Amphipod]] = [None, None, None]
        self.rooms: List[List[Optional[Amphipod]]] = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ]

    def all_amphipods(self) -> List[Amphipod]:
        return list(
            filter(
                None,
                self.spots_left
                + self.spots_middle
                + self.spots_right
                + [item for sublist in self.rooms for item in sublist],
            )
        )

    def find_amphipod_in_room(self, amphipod: Amphipod) -> Optional[Tuple[int, int]]:
        for i, room in enumerate(self.rooms):
            if amphipod in room:
                return (i, room.index(amphipod))
        return None

    def amphipods_for_type(self, amphipod_type: AmphipodType) -> List[Amphipod]:
        result = []
        for room in self.rooms:
            for amphipod in room:
                if amphipod_type == amphipod.amphipod_type:
                    result.append(amphipod)
        return result

    def collisions_for_type(self, amphipod_type: AmphipodType) -> Dict[Amphipod, List[Amphipod]]:
        amphipods = self.amphipods_for_type(amphipod_type)
        return {amphipod: self.collisions_for_amphipod(amphipod) for amphipod in amphipods}

    def collisions_for_amphipod(self, amphipod: Amphipod) -> List[Amphipod]:
        room_location = self.find_amphipod_in_room(amphipod)
        if room_location is not None:
            room_index, position = room_location
            # collisions in target room
            collisions = [
                collision
                for collision in filter(None, self.rooms[amphipod.amphipod_type.value])
                if collision.amphipod_type != amphipod.amphipod_type
            ]
            # collisions in hallway
            collisions.extend(
                filter(
                    None,
                    self.spots_middle[
                        min(room_index, amphipod.amphipod_type.value) : max(room_index, amphipod.amphipod_type.value)
                    ],
                )
            )
            assert amphipod.amphipod_type not in [collision.amphipod_type for collision in collisions]
            # collision in own room
            if position == 0 and self.rooms[room_index][1] is not None:
                collisions.append(self.rooms[room_index][1])
            return collisions

        # collisions in target room
        collisions = [
            collision
            for collision in filter(None, self.rooms[amphipod.amphipod_type.value])
            if collision.amphipod_type != amphipod.amphipod_type
        ]
        # # collisions in hallway
        # collisions.extend(
        #     filter(
        #         None,
        #         self.spots_middle[
        #             min(room_index, amphipod.amphipod_type.value) : max(
        #                 room_index, amphipod.amphipod_type.value
        #             )
        #         ],
        #     )
        # )
        # raise NotImplementedError()
        return []

    def _remove_amphipod(self, amphipod: Amphipod) -> None:
        for room in self.rooms:
            for i, current_amphipod in enumerate(room):
                if current_amphipod == amphipod:
                    room[i] = None
                    return

        for i, current_amphipod in enumerate(self.spots_left):
            if current_amphipod == amphipod:
                self.spots_left[i] = None
                return

        for i, current_amphipod in enumerate(self.spots_middle):
            if current_amphipod == amphipod:
                self.spots_middle[i] = None
                return

        for i, current_amphipod in enumerate(self.spots_right):
            if current_amphipod == amphipod:
                self.spots_right[i] = None
                return

        assert False

    def can_move_amphipod_to_target(self, amphipod: Amphipod) -> bool:
        bottom_spot_in_target = self.rooms[amphipod.amphipod_type.value][0]
        return (
            not self.collisions_for_amphipod(amphipod)
            and amphipod not in self.rooms[amphipod.amphipod_type.value]
            and (bottom_spot_in_target is None or bottom_spot_in_target.amphipod_type == amphipod.amphipod_type)
        )

    def move_amphipod_to_target_or_leftmost_spot(self, amphipod: Amphipod) -> int:
        if self.can_move_amphipod_to_target(amphipod):
            for i, spot in enumerate(self.rooms[amphipod.amphipod_type.value]):
                if spot is None:
                    room_location = self.find_amphipod_in_room(amphipod)
                    if room_location is None:
                        distance_exit = 0
                        if amphipod in self.spots_left:
                            distance_hall = 1 - self.spots_left.index(amphipod) + 1 + 2 * amphipod.amphipod_type.value
                        elif amphipod in self.spots_right:
                            distance_hall = (
                                1 - self.spots_right.index(amphipod) + 1 + 2 * (3 - amphipod.amphipod_type.value)
                            )
                        elif amphipod in self.spots_middle:
                            dx = amphipod.amphipod_type.value - self.spots_middle.index(amphipod)
                            if dx >= 0:
                                distance_hall = abs(dx * 2 - 1)
                            else:
                                distance_hall = -dx * 2 + 1
                        else:
                            assert False
                    else:
                        distance_exit = 2 - room_location[1]
                        distance_hall = 1 + 2 * abs(amphipod.amphipod_type.value - room_location[0])
                    distance_enter = 2 - i
                    distance = distance_exit + distance_hall + distance_enter
                    self._remove_amphipod(amphipod)
                    self.rooms[amphipod.amphipod_type.value][i] = amphipod
                    return distance * 10**amphipod.amphipod_type.value
            assert False

        # we can't move to the target room, move to the leftmost free spot
        self._remove_amphipod(amphipod)
        for i, spot in enumerate(self.spots_left):
            if spot is None:
                self.spots_left[i] = amphipod
                return 1

        for i, spot in enumerate(self.spots_middle):
            if spot is None:
                self.spots_middle[i] = amphipod
                return 1

        for i, spot in enumerate(self.spots_right):
            if spot is None:
                self.spots_right[i] = amphipod
                return 1

        assert False

    def __repr__(self) -> str:
        def spot(spot: Optional[Amphipod]) -> str:
            return " " if spot is None else spot.name

        return "\n".join(
            [
                "#############",
                f"#{spot(self.spots_left[0])}{spot(self.spots_left[1])}.{spot(self.spots_middle[0])}.{spot(self.spots_middle[1])}.{spot(self.spots_middle[2])}.{spot(self.spots_right[1])}{spot(self.spots_right[0])}#",
                f"###{spot(self.rooms[0][1])}#{spot(self.rooms[1][1])}#{spot(self.rooms[2][1])}#{spot(self.rooms[3][1])}###",
                f"  #{spot(self.rooms[0][0])}#{spot(self.rooms[1][0])}#{spot(self.rooms[2][0])}#{spot(self.rooms[3][0])}#",
                "  #########",
            ]
        )


class Day23(Day):
    def __init__(self) -> None:
        super().__init__(23)

    def parse_data(self) -> Map:
        world = Map()
        for i, character in enumerate(self.raw_data[2].replace("#", "").strip()):
            world.rooms[i][1] = Amphipod(AmphipodType[character])
        for i, character in enumerate(self.raw_data[3].replace("#", "").strip()):
            world.rooms[i][0] = Amphipod(AmphipodType[character])
        return world

    def part_1(self) -> int:
        print(self.data)

        move_order = []
        amphipods_to_move = self.data.amphipods_for_type(AmphipodType.D)
        while True:
            move_out_of_the_way = set()
            for amphipod in amphipods_to_move:
                move_out_of_the_way.update(
                    collision
                    for collision in self.data.collisions_for_amphipod(amphipod)
                    if collision.amphipod_type < amphipod.amphipod_type
                )
            if not move_out_of_the_way:
                break
            move_order.append(move_out_of_the_way)
            amphipods_to_move = move_out_of_the_way
        print(move_order)

        cost = 0
        for order in move_order[::-1]:
            print(order)
            while order:
                for amphipod in order:
                    if order.intersection(self.data.collisions_for_amphipod(amphipod)):
                        continue

                    print("Moving", amphipod, "out of the way")
                    cost += self.data.move_amphipod_to_target_or_leftmost_spot(amphipod)
                    print(self.data)
                    order.remove(amphipod)
                    print(order)
                    break

        moved = True
        while moved:
            moved = False
            for amphipod in self.data.all_amphipods():
                if not self.data.can_move_amphipod_to_target(amphipod):
                    continue
                new_cost = self.data.move_amphipod_to_target_or_leftmost_spot(amphipod)
                if new_cost:
                    print("Moving", amphipod, "to target")
                    cost += new_cost
                    moved = True
                    print(self.data)

        return cost

    @property
    def part_1_solution(self) -> int:
        return None

    def part_2(self) -> int:
        pass

    @property
    def part_2_solution(self) -> int:
        return None
