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


def saturate(im, amount=1):
    assert amount >= 0

    # matrix from a w3c document:
    # https://www.w3.org/TR/SVG11/filters.html#feColorMatrixValuesAttribute
    matrix = [
        .213 + .787 * amount,
        .715 - .715 * amount,
        .072 - .072 * amount,
        0,
        .213 - .213 * amount,
        .715 + .285 * amount,
        .072 - .072 * amount,
        0,
        .213 - .213 * amount,
        .715 - .715 * amount,
        .072 + .928 * amount,
        0,
    ]

    return im.convert('RGB').convert('RGB', matrix).convert(im.mode)
