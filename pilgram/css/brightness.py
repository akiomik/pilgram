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


def brightness(im, amount=1):
    """Adjusts the brightness.

    A brightness operation is equivalent to the following matrix operation:

        | R' |     | c  0  0 |   | R |
        | G' |  =  | 0  c  0 | * | G |
        | B' |     | 0  0  c |   | B |

    See the W3C document:
    https://www.w3.org/TR/filter-effects-1/#brightnessEquivalent

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

    return im.point(lambda x: round(x * amount))
