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

from pilgram import util


def hue_rotate(im, deg=0):
    """Applies hue rotation.

    A hue rotate operation is equivalent to the following matrix operation:

        | R' |     | a00  a01  a02  0  0 |   | R |
        | G' |     | a10  a11  a12  0  0 |   | G |
        | B' |  =  | a20  a21  a22  0  0 | * | B |
        | A' |     | 0    0    0    1  0 |   | A |
        | 1  |     | 0    0    0    0  1 |   | 1 |

    where

        | a00 a01 a02 |    [+0.213 +0.715 +0.072]
        | a10 a11 a12 | =  [+0.213 +0.715 +0.072] +
        | a20 a21 a22 |    [+0.213 +0.715 +0.072]
                                [+0.787 -0.715 -0.072]
        cos(hueRotate value) *  [-0.213 +0.285 -0.072] +
                                [-0.213 -0.715 +0.928]
                                [-0.213 -0.715+0.928]
        sin(hueRotate value) *  [+0.143 +0.140-0.283]
                                [-0.787 +0.715+0.072]

    See the W3C document:
    https://www.w3.org/TR/SVG11/filters.html#feColorMatrixValuesAttribute

    Arguments:
        im: An input image.
        deg: An optional integer/float. The hue rotate value (degrees).
            Defaults to 0.

    Returns:
        The output image.
    """

    cos_hue = math.cos(math.radians(deg))
    sin_hue = math.sin(math.radians(deg))

    matrix = [
        .213 + cos_hue * .787 - sin_hue * .213,
        .715 - cos_hue * .715 - sin_hue * .715,
        .072 - cos_hue * .072 + sin_hue * .928,
        0,
        .213 - cos_hue * .213 + sin_hue * .143,
        .715 + cos_hue * .285 + sin_hue * .140,
        .072 - cos_hue * .072 - sin_hue * .283,
        0,
        .213 - cos_hue * .213 - sin_hue * .787,
        .715 - cos_hue * .715 + sin_hue * .715,
        .072 + cos_hue * .928 + sin_hue * .072,
        0,
    ]

    rotated = util.or_convert(im, 'RGB').convert('RGB', matrix)
    return util.or_convert(rotated, im.mode)
