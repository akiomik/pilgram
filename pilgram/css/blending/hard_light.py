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
from PIL import Image, ImageChops

from pilgram.css.blending.alpha import alpha_blend
from pilgram import util


LUT_2x = [util.clip(2 * i) for i in range(256)]
LUT_2x_1 = [util.clip(2 * i - 255) for i in range(256)]


def _hard_light(im1, im2):
    """The hard light blend mode.

    Arguments:
        im1: A backdrop image (RGB).
        im2: A source image (RGB).

    Returns:
        The output image.
    """

    im2_multiply = util.apply_lut(im2, LUT_2x)
    multiply = np.asarray(ImageChops.multiply(im1, im2_multiply))

    im2_screen = util.apply_lut(im2, LUT_2x_1)
    screen = np.asarray(ImageChops.screen(im1, im2_screen))

    cm = np.where(np.asarray(im2) < 128, multiply, screen)
    return Image.fromarray(cm)


def hard_light(im1, im2):
    """Multiplies or screens the colors, depending on the source color value

    The hard light formula is defined as:

        if(Cs <= 0.5)
            B(Cb, Cs) = Multiply(Cb, 2 x Cs)
        else
            B(Cb, Cs) = Screen(Cb, 2 x Cs -1)

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendinghardlight

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).

    Returns:
        The output image.
    """

    return alpha_blend(im1, im2, _hard_light)
