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


def sepia(im, amount=1):
    """Converts image to sepia.

    A sepia operation is equivalent to the following matrix operation:

    | R' |     |0.393+0.607s  0.769-0.769s  0.189-0.189s 0  0 |   | R |
    | G' |     |0.349-0.349s  0.686+0.314s  0.168-0.168s 0  0 |   | G |
    | B' |  =  |0.272-0.272g  0.534-0.534g  0.131+0.869g 0  0 | * | B |
    | A' |     |          0             0             0  1  0 |   | A |
    | 1  |     |          0             0             0  0  1 |   | 1 |

    See the W3C document:
    https://www.w3.org/TR/filter-effects-1/#sepiaEquivalent

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

    amount = 1 - min(amount, 1)
    matrix = [
        .393 + .607 * amount, .769 - .769 * amount, .189 - .189 * amount, 0,
        .349 - .349 * amount, .686 + .314 * amount, .168 - .168 * amount, 0,
        .272 - .272 * amount, .534 - .534 * amount, .131 + .869 * amount, 0,
    ]

    sepia_toned = util.or_convert(im, 'RGB').convert('RGB', matrix)
    return util.or_convert(sepia_toned, im.mode)
