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

from pilgram import util


def grayscale(im, amount=1):
    """Converts image to grayscale.

    A grayscale operation is equivalent to the following matrix operation:

    | R' |     |0.2126+0.7874g  0.7152-0.7152g  0.0722-0.0722g 0  0 |   | R |
    | G' |     |0.2126-0.2126g  0.7152+0.2848g  0.0722-0.0722g 0  0 |   | G |
    | B' |  =  |0.2126-0.2126g  0.7152-0.7152g  0.0722+0.9278g 0  0 | * | B |
    | A' |     |            0               0               0  1  0 |   | A |
    | 1  |     |            0               0               0  0  1 |   | 1 |

    See the W3C document:
    https://www.w3.org/TR/filter-effects-1/#grayscaleEquivalent

    Arguments:
        im: An input image.
        amount: An optional integer/float. The filter amount (percentage).
            Defaults to 1.

    Returns:
        The output image.

    Raises:
        AssertionError: if `amount` is less than 0.
    """

    assert amount >= 0

    g = 1 - min(amount, 1)
    matrix = [
        .2126 + .7874 * g, .7152 - .7152 * g, .0722 - .0722 * g, 0,
        .2126 - .2126 * g, .7152 + .2848 * g, .0722 - .0722 * g, 0,
        .2126 - .2126 * g, .7152 - .7152 * g, .0722 + .9278 * g, 0,
    ]

    grayscaled = util.or_convert(im, 'RGB').convert('RGB', matrix)
    return util.or_convert(grayscaled, im.mode)
