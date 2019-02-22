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
from PIL import Image, ImageChops


def or_convert(im, mode):
    """Converts image to mode if necessary

    Arguments:
        im: An input image.
        mode: A string. The requested mode.

    Returns:
        The output image.
    """

    return im if im.mode == mode else im.convert(mode)


def fill(shape, color):
    """Fills new image with the color.

    Arguments:
        shape: A tuple/list of 2 integers. The shape of output image.
        color: A tuple/list of 3 or 4 integers. The fill color.

    Returns:
        The output image.

    Raises:
        AssertionError: if `shape` and/or `color` have invalid size.
    """

    assert len(shape) == 2
    assert len(color) in [3, 4]

    if len(color) == 4:
        color[3] = round(color[3] * 255)  # alpha

    uniqued = list(set(color))
    cmap = {c: Image.new('L', shape, c) for c in uniqued}

    if len(color) == 3:
        r, g, b = color
        return Image.merge('RGB', (cmap[r], cmap[g], cmap[b]))
    else:
        r, g, b, a = color
        return Image.merge('RGBA', (cmap[r], cmap[g], cmap[b], cmap[a]))


def _prepared_linear_gradient_mask(shape, start, end, is_horizontal=True):
    """Returns prepared linear gradient mask."""
    assert end >= 1

    mask = ImageChops.invert(Image.linear_gradient('L'))
    w, h = mask.size
    box = (0, round(h * start), w, round(h / end))
    resized_mask = mask.resize(shape, box=box)

    if is_horizontal:
        return resized_mask.rotate(90)
    else:
        return resized_mask


def linear_gradient_mask(shape, start=0, end=1, is_horizontal=True):
    """Creates mask image for linear gradient image.

    Arguments:
        shape: A tuple/list of 2 integers. The shape of output image.
        start: An optional integer/float. The starting point start.
            The point is left-side when `is_horizontal` is True, top otherwise.
            Defaults to 0.
        end: An optional integer/float. The ending point.
            The point is right-side when `is_horizontal` is True,
            bottom otherwise. Defaults to 1.
        is_horizontal: A optional boolean. The direction of gradient line.
            Left to right if True, top to bottom else.

    Returns:
        The mask image.

    Raises:
        AssertionError: if `shape`, `start` and/or `end` have invalid size.
    """

    assert len(shape) == 2

    if end >= 1:
        return _prepared_linear_gradient_mask(
                shape, start, end, is_horizontal)

    w, h = shape

    if is_horizontal:
        row = np.linspace(start, end, w)
        mask = np.tile(row, (h, 1))
    else:
        row = np.linspace(start, end, h)
        mask = np.tile(row, (w, 1)).T

    mask *= 255
    mask = np.clip(mask, 0, 255)

    return Image.fromarray(np.uint8(mask.round()))


def linear_gradient(shape, start, end, is_horizontal=True):
    """Creates linear gradient image.

    Arguments:
        shape: A tuple/list of 2 integers. The shape of output image.
        start: A tuple/list of 3 integers. The starting point color.
            The point is left-side when `is_horizontal` is True, top otherwise.
        end: A tuple/list of 3 integers. The ending point color.
            The point is right-side when `is_horizontal` is True,
            the bottom otherwise.
        is_horizontal: An optional boolean. The direction of gradient line.
            Left to right if True, top to bottom else.

    Returns:
        The output image.

    Raises:
        AssertionError: if `shape`, `start` and/or `end` have invalid size.
    """

    assert len(shape) == 2
    assert len(start) == 3
    assert len(end) == 3

    im_start = fill(shape, start)
    im_end = fill(shape, end)
    mask = linear_gradient_mask(shape, is_horizontal=is_horizontal)

    return Image.composite(im_start, im_end, mask)


def _prepared_radial_gradient_mask(shape, scale=1):
    """Returns prepared radial gradient mask"""

    mask = ImageChops.invert(Image.radial_gradient('L'))

    w, h = mask.size
    xoffset = round((w - w / scale) / 2)
    yoffset = round((h - h / scale) / 2)
    box = (xoffset, yoffset, w - xoffset, h - yoffset)

    return mask.resize(shape, box=box)


def radial_gradient_mask(shape, length=0, scale=1, position=(.5, .5)):
    """Creates mask image for radial gradient image.

    Arguments:
        shape: A tuple/list of 2 integers. The shape of mask image.
        length: An optional integer/float. The percentage of inner color stop.
            Defaults to 0.
        scale: An optional integer/float. The percentage of ending shape.
            Defaults to 1.
        position: An optional tuple/list of two floats.
            The percentage of center position for the circle.
            Defaults to the center (0.5, 0.5).

    Returns:
        The mask image.
    """

    if length >= 1:
        return Image.new('L', shape, 255)

    if scale <= 0:
        return Image.new('L', shape, 0)

    w, h = shape

    # use faster method if possible
    if length == 0 and scale >= 1 and w == h and position == (.5, .5):
        return _prepared_radial_gradient_mask(shape, scale)

    y, x = np.ogrid[:h, :w]
    cx = (w - 1) * position[0]
    cy = (h - 1) * position[1]

    # rw (or rh) is a width (height) from cx (cy) to farthest side
    rw_factor = max(position[0], 1 - position[0])
    rh_factor = max(position[1], 1 - position[1])
    rw = (w - 1) * rw_factor
    rh = (h - 1) * rh_factor
    r = math.sqrt(rw ** 2 + rh ** 2)

    def adjust_length(x):
        base = max(scale - length, 0.001)  # avoid a division by zero
        return (x - length) / base

    mask = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r  # distance from center
    mask = np.apply_along_axis(adjust_length, 0, mask)
    mask = 1 - mask  # invert: distance to center
    mask *= 255
    mask = mask.clip(0, 255)

    return Image.fromarray(np.uint8(mask.round()))


# TODO: improve reproduction of gradient when multiple color stops
def radial_gradient(shape, *color_stops, **kwargs):
    """Creates radial gradient image.

    Arguments:
        shape: A tuple/list of 2 integers. The shape of output image.
        color_stops: A tuple/list of color stops.
            The color stop is a pair of RGB color and length.

    Returns:
        The output image.

    Raises:
        AssertionError: if `shape` and/or `color_stop` have invalid size.
    """

    assert len(shape) == 2
    assert len(color_stops) >= 2
    for color_stop in color_stops:
        assert len(color_stop) == 2
        assert len(color_stop[0]) == 3

    scale = color_stops[-1][1]  # use length of the last color stop as scale
    color_stops = [(fill(shape, c), l) for c, l in color_stops]

    def compose(x, y):
        kwargs_ = kwargs.copy()
        kwargs_['length'] = x[1]
        kwargs_['scale'] = scale
        mask = radial_gradient_mask(shape, **kwargs_)
        return (Image.composite(x[0], y[0], mask), y[1])

    return reduce(compose, color_stops)[0]


def scale_color(im, scale=1):
    """Scales colors of input image.

    Arguments:
        im: An input image.
        scale: An optional integer or float. The scaling factor.
            Defaults to 1.

    Returns:
        The output image.
    """

    return im.point(lambda x: round(x * scale))
