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


def _clip(a, a_min=0, a_max=255):
    """Clips value

    Arguments:
        a: An integer/float. The input value to clip.
        a_min: An optional integer/float. The minimum value. Defaults to 0.
        a_max: An optional integer/float. The maximum value. Defaults to 255.

    Returns:
        The clipped value.
    """

    return min(max(a, a_min), a_max)


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
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    im2_multiply = im2.point(lambda x: _clip(2 * x))
    multiply = np.asarray(ImageChops.multiply(im1, im2_multiply))

    im2_screen = im2.point(lambda x: _clip(2 * x - 255))
    screen = np.asarray(ImageChops.screen(im1, im2_screen))

    cm = np.where(np.asarray(im2) < 128, multiply, screen)
    return Image.fromarray(cm)
