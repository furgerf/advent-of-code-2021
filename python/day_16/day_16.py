#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from day import Day
import numpy as np


class Packet(ABC):
    def __init__(self, version: int, type: int) -> None:
        self._version = version
        self._type = type

    @property
    @abstractmethod
    def version_sum(self) -> int:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @staticmethod
    def parse(version: int, bits: str) -> Tuple["Packet", int]:
        raise NotImplemented


class LiteralPacket(Packet):
    def __init__(self, version: int, number: int) -> None:
        super().__init__(version, 4)
        self._number = number

    @property
    def version_sum(self) -> int:
        return self._version

    @property
    def value(self) -> int:
        return self._number

    @staticmethod
    def parse(version: int, bits: str) -> Tuple["LiteralPacket", int]:
        number = 0
        index = 6
        while True:
            number <<= 4
            number += int(bits[index + 1 : index + 5], 2)
            if bits[index] == "0":
                index += 5
                break
            index += 5

        return (LiteralPacket(version, number), index)


class OperatorPacket(Packet):
    def __init__(self, version: int, type: int, sub_packets: List[Packet]) -> None:
        super().__init__(version, type)
        self._sub_packets = sub_packets

    @property
    def version_sum(self) -> int:
        return self._version + sum(packet.version_sum for packet in self._sub_packets)

    @property
    def value(self) -> int:
        match self._type:
            case 0:
                return sum(packet.value for packet in self._sub_packets)
            case 1:
                return np.prod(list(packet.value for packet in self._sub_packets))
            case 2:
                return min(packet.value for packet in self._sub_packets)
            case 3:
                return max(packet.value for packet in self._sub_packets)
            case 5:
                assert len(self._sub_packets) == 2
                return int(self._sub_packets[0].value > self._sub_packets[1].value)
            case 6:
                assert len(self._sub_packets) == 2
                return int(self._sub_packets[0].value < self._sub_packets[1].value)
            case 7:
                assert len(self._sub_packets) == 2
                return int(self._sub_packets[0].value == self._sub_packets[1].value)
            case _:
                assert False

    @staticmethod
    def parse(version: int, type: int, bits: str) -> Tuple["OperatorPacket", int]:
        packets = []
        index = 7
        if bits[6] == "0":
            # number of bits
            number_of_bits = int(bits[index : index + 15], 2)
            index += 15
            packets.extend(parse_packets(bits[index : index + number_of_bits])[0])
            index += number_of_bits
        else:
            # number of sub packets
            number_of_sub_packets = int(bits[index : index + 11], 2)
            index += 11
            sub_packets, bits_read = parse_packets(bits[index:], number_of_sub_packets)
            packets.extend(sub_packets)
            index += bits_read

        return (OperatorPacket(version, type, packets), index)


def parse_packets(bits: str, max_packet_count: Optional[int] = None) -> Tuple[List[Packet], int]:
    packets = []
    total_bits_read = 0
    while True:
        packet_version = int(bits[:3], 2)
        packet_type = int(bits[3:6], 2)
        if packet_type == 4:
            packet, bits_read = LiteralPacket.parse(packet_version, bits)
        else:
            packet, bits_read = OperatorPacket.parse(packet_version, packet_type, bits)
        packets.append(packet)
        total_bits_read += bits_read
        if bits_read == len(bits):
            break
        assert bits_read < len(bits)
        bits = bits[bits_read:]
        if len(packets) == max_packet_count:
            break
        if "1" not in bits:
            break
    return packets, total_bits_read


class Day16(Day):
    def __init__(self) -> None:
        super().__init__(16)

    def parse_data(self) -> List[Packet]:
        bits = "".join([f"{int(letter, 16):04b}" for letter in self.raw_data[0]])
        return parse_packets(bits)[0]

    def part_1(self) -> int:
        return self.data[0].version_sum

    @property
    def part_1_solution(self) -> int:
        return 986

    def part_2(self) -> int:
        return self.data[0].value

    @property
    def part_2_solution(self) -> int:
        return 18234816469452
