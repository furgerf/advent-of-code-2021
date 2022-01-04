#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from day import Day


class Day20(Day):
    def __init__(self) -> None:
        super().__init__(20)

    def parse_data(self) -> Tuple[List[bool], np.ndarray]:
        pixel_lookup = [character == "#" for character in self.raw_data[0]]
        pixels = np.array([[character == "#" for character in line] for line in self.raw_data[2:]], dtype=bool)
        return pixel_lookup, pixels

    def _enhance_pixel(self, pixel_bits: np.ndarray) -> bool:
        assert len(pixel_bits) == 9
        index = 0
        for bit in pixel_bits:
            index *= 2
            if bit:
                index += 1
        return self.pixel_lookup[index]

    def enhance_image(self, pixels: np.ndarray, background_pixel: bool) -> Tuple[np.ndarray, bool]:
        new_background_pixel = self._enhance_pixel(np.array([background_pixel] * 9))
        expanded_pixels = np.full((pixels.shape[0] + 4, pixels.shape[1] + 4), background_pixel)
        expanded_pixels[2 : expanded_pixels.shape[0] - 2, 2 : expanded_pixels.shape[1] - 2] = pixels
        new_pixels = np.full((pixels.shape[0] + 2, pixels.shape[1] + 2), new_background_pixel)

        for (x, y), _ in np.ndenumerate(new_pixels):
            pixel_bits = expanded_pixels[x : x + 3, y : y + 3].reshape(-1)
            new_pixels[x, y] = self._enhance_pixel(pixel_bits)

        return new_pixels, new_background_pixel

    def part_1(self) -> int:
        self.pixel_lookup, pixels = self.data
        background_pixel = False
        output, background_pixel = self.enhance_image(pixels, background_pixel)
        return len(np.where(self.enhance_image(output, background_pixel)[0] == True)[0])

    @property
    def part_1_solution(self) -> int:
        return 4964

    def part_2(self) -> int:
        self.pixel_lookup, pixels = self.data
        background_pixel = False
        # target_shape = (200, 200)
        for _ in range(50):
            # expanded_pixels = np.full(target_shape, background_pixel)
            # offset = (target_shape[0] - pixels.shape[0]) // 2
            # expanded_pixels[offset : offset + pixels.shape[0], offset : offset + pixels.shape[1]] = pixels
            # plt.imsave(f"foo-{_:02}.png", expanded_pixels)
            pixels, background_pixel = self.enhance_image(pixels, background_pixel)

        # plt.imsave("foo-50.png", pixels)
        return len(np.where(pixels == True)[0])

    @property
    def part_2_solution(self) -> int:
        return 13202
