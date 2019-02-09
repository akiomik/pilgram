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


def grayscale(im, amount=1):
    assert amount >= 0
    amount = 1 - min(amount, 1)

    # matrix from a w3c document:
    # https://www.w3.org/TR/filter-effects-1/#grayscaleEquivalent
    matrix = [
        .2126 + .7874 * amount,
        .7152 - .7152 * amount,
        .0722 - .0722 * amount,
        0,
        .2126 - .2126 * amount,
        .7152 + .2848 * amount,
        .0722 - .0722 * amount,
        0,
        .2126 - .2126 * amount,
        .7152 - .7152 * amount,
        .0722 + .9278 * amount,
        0,
    ]

    return im.convert('RGB', matrix)
