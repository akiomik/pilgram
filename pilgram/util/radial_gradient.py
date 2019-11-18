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
from functools import reduce

import numpy as np
from PIL import Image

from pilgram.util import fill, invert


def _prepared_radial_gradient_mask(size, scale=1):
    """Returns prepared radial gradient mask"""

    mask = invert(Image.radial_gradient('L'))

    w, h = mask.size
    xoffset = round((w - w / scale) / 2)
    yoffset = round((h - h / scale) / 2)
    box = (xoffset, yoffset, w - xoffset, h - yoffset)

    return mask.resize(size, box=box)


def radial_gradient_mask(size, length=0, scale=1, center=(.5, .5)):
    """Creates mask image for radial gradient image.

    Arguments:
        size: A tuple/list of 2 integers. The size of mask image.
        length: An optional integer/float. The percentage of inner color stop.
            Defaults to 0.
        scale: An optional integer/float. The percentage of ending shape.
            Defaults to 1.
        center: An optional tuple/list of two floats.
            The percentage of center position for the circle.
            Defaults to the center (0.5, 0.5).

    Returns:
        The mask image.
    """

    if length >= 1:
        return Image.new('L', size, 255)

    if scale <= 0:
        return Image.new('L', size, 0)

    w, h = size
    cx, cy = center

    # use faster method if possible
    if length == 0 and scale >= 1 and w == h and center == (.5, .5):
        return _prepared_radial_gradient_mask(size, scale)

    rw_left = w * cx
    rw_right = w * (1 - cx)
    rh_top = h * cy
    rh_bottom = h * (1 - cy)

    x = np.linspace(-rw_left, rw_right, w)
    y = np.linspace(-rh_top, rh_bottom, h)[:, None]

    # r is a radius to the farthest-corner
    r = math.sqrt(max(rw_left, rw_right) ** 2 + max(rh_top, rh_bottom) ** 2)
    base = max(scale - length, 0.001)  # avoid a division by zero

    mask = np.sqrt(x ** 2 + y ** 2) / r  # distance from center
    mask = (mask - length) / base  # adjust ending shape
    mask = 1 - mask  # invert: distance to center
    mask *= 255
    mask = mask.clip(0, 255)

    return Image.fromarray(np.uint8(mask.round()))


def radial_gradient(size, colors, positions=None, **kwargs):
    """Creates radial gradient image.

    Arguments:
        size: A tuple/list of 2 integers. The size of output image.
        colors: A tuple/list of RGB colors.
        positions: An optional tuple/list of floats.
            The position of color stops.
            If omitted, the positions are equal spacing.

    Returns:
        The output image.

    Raises:
        AssertionError: if `size`, `colors` or `positions` have invalid size.
    """

    assert len(size) == 2
    assert len(colors) >= 2
    for color in colors:
        assert len(color) == 3

    if positions is None:
        positions = np.linspace(0, 1, len(colors))
    else:
        assert len(positions) >= 2
        assert len(colors) == len(positions)

    colors = [fill(size, color) for color in colors]

    def compose(x, y):
        kwargs_ = kwargs.copy()
        kwargs_['length'] = x[1]
        kwargs_['scale'] = y[1]
        mask = radial_gradient_mask(size, **kwargs_)
        return (Image.composite(x[0], y[0], mask), y[1])

    return reduce(compose, zip(colors, positions))[0]
