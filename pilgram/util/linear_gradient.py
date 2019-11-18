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

import numpy as np
from PIL import Image

from pilgram.util import fill, invert


def _prepared_linear_gradient_mask(size, start, end, is_horizontal=True):
    """Returns prepared linear gradient mask."""
    assert end >= 1

    mask = invert(Image.linear_gradient('L'))
    w, h = mask.size
    box = (0, round(h * start), w, round(h / end))
    resized_mask = mask.resize(size, box=box)

    if is_horizontal:
        return resized_mask.rotate(90)
    else:
        return resized_mask


def linear_gradient_mask(size, start=0, end=1, is_horizontal=True):
    """Creates mask image for linear gradient image.

    Arguments:
        size: A tuple/list of 2 integers. The size of output image.
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
        AssertionError: if `size`, `start` and/or `end` have invalid size.
    """

    assert len(size) == 2

    if end >= 1:
        return _prepared_linear_gradient_mask(
                size, start, end, is_horizontal)

    w, h = size
    start *= 255
    end *= 255

    if is_horizontal:
        row = np.linspace(start, end, num=w, dtype=np.uint8)
        mask = np.tile(row, (h, 1))
    else:
        row = np.linspace(start, end, num=h, dtype=np.uint8)
        mask = np.tile(row, (w, 1)).T

    return Image.fromarray(mask)


def linear_gradient(size, start, end, is_horizontal=True):
    """Creates linear gradient image.

    Arguments:
        size: A tuple/list of 2 integers. The size of output image.
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
        AssertionError: if `size`, `start` and/or `end` have invalid size.
    """

    assert len(size) == 2
    assert len(start) == 3
    assert len(end) == 3

    im_start = fill(size, start)
    im_end = fill(size, end)
    mask = linear_gradient_mask(size, is_horizontal=is_horizontal)

    return Image.composite(im_start, im_end, mask)
