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


def hue_rotate(im, deg=0):
    cos_hue = math.cos(deg * math.pi / 180)
    sin_hue = math.sin(deg * math.pi / 180)

    # matrix from a w3c document:
    # https://www.w3.org/TR/SVG11/filters.html#feColorMatrixValuesAttribute
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

    return im.convert('RGB').convert('RGB', matrix).convert(im.mode)
