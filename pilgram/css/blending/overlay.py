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

from pilgram.css.blending import hard_light


def overlay(im1, im2):
    """Multiplies or screens the colors, depending on the backdrop color value

    The overlay formula is defined as:

        B(Cb, Cs) = HardLight(Cs, Cb)

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingoverlay

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).

    Returns:
        The output image.
    """

    return hard_light(im2, im1)
