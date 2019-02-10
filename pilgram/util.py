# Copyright 2019 Akiomi Kamakura
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

import numpy as np
from PIL import Image


def fill(shape, color):
    assert len(shape) == 2
    assert len(color) == 3

    r = Image.new('L', shape, color[0])
    g = Image.new('L', shape, color[1])
    b = Image.new('L', shape, color[2])

    return Image.merge('RGB', (r, g, b))


def linear_gradient_mask(shape, start=1, end=0, is_horizontal=True):
    assert len(shape) == 2

    if is_horizontal:
        row = np.linspace(start, end, shape[0])
        mask = np.tile(row, (shape[1], 1))
    else:
        row = np.linspace(start, end, shape[1])
        mask = np.tile(row, (shape[0], 1)).T

    mask *= 255
    mask = np.clip(mask, 0, 255)

    return Image.fromarray(np.uint8(mask.round()))


def linear_gradient(shape, start, end, is_horizontal=True):
    assert len(shape) == 2
    assert len(start) == 3
    assert len(end) == 3

    im_start = fill(shape, start)
    im_end = fill(shape, end)
    mask = linear_gradient_mask(shape, is_horizontal=is_horizontal)

    return Image.composite(im_start, im_end, mask)


# TODO: add start and end value as parameters
def radial_gradient_mask(shape, length=0, scale=1, position=(.5, .5)):
    # TODO: support scale <= length
    assert scale != length

    if (length >= 1):
        return Image.new('L', shape, 255)

    w, h = shape
    x, y = np.ogrid[:w, :h]
    cx = w * position[0]
    cy = h * position[1]

    # TODO: r_scale is unknown factor for mayfair filter
    r_scale = 1 + abs(.5 - position[0]) + abs(.5 - position[1])
    r = math.sqrt((w / 2) ** 2 + (h / 2) ** 2) * r_scale

    def adjust_length(x):
        return ((x / r) - length) / (scale - length)

    mask = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)  # distance from center
    mask = np.apply_along_axis(adjust_length, 0, mask)
    mask = 1 - mask  # invert: distance to center
    mask *= 255
    mask = mask.clip(0, 255)

    return Image.fromarray(np.uint8(mask.round()))


# TODO: support multiple color stops
def radial_gradient(shape, start, end, **kwargs):
    assert len(shape) == 2
    assert len(start) == 3 and len(end) == 3

    im_start = fill(shape, start)
    im_end = fill(shape, end)
    mask = radial_gradient_mask(shape, **kwargs)

    return Image.composite(im_start, im_end, mask)
