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


def saturate(im, amount=1):
    """Saturates image.

    A saturate operation is equivalent to the following matrix operation:

        | R' |     |0.213+0.787s  0.715-0.715s  0.072-0.072s 0  0 |   | R |
        | G' |     |0.213-0.213s  0.715+0.285s  0.072-0.072s 0  0 |   | G |
        | B' |  =  |0.213-0.213s  0.715-0.715s  0.072+0.928s 0  0 | * | B |
        | A' |     |           0            0             0  1  0 |   | A |
        | 1  |     |           0            0             0  0  1 |   | 1 |

    See the W3C document:
    https://www.w3.org/TR/SVG11/filters.html#feColorMatrixValuesAttribute

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

    matrix = [
        .213 + .787 * amount, .715 - .715 * amount, .072 - .072 * amount, 0,
        .213 - .213 * amount, .715 + .285 * amount, .072 - .072 * amount, 0,
        .213 - .213 * amount, .715 - .715 * amount, .072 + .928 * amount, 0,
    ]

    saturated = util.or_convert(im, 'RGB').convert('RGB', matrix)
    return util.or_convert(saturated, im.mode)
