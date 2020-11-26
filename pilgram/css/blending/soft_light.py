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

from __future__ import division

import math

import numpy as np
from PIL import Image, ImageChops

from pilgram.css.blending.alpha import alpha_blend
from pilgram import util


def _d_cb(cb):
    """Returns D(Cb) - Cb"""

    cb = float(cb) / 255

    if cb <= .25:
        d = ((16 * cb - 12) * cb + 4) * cb
    else:
        d = math.sqrt(cb)

    return round((d - cb) * 255)


LUT_1_2_x_cs = [util.clip(255 - 2 * i) for i in range(256)]
LUT_cb_x_1_cb = [round(util.clip(i * (1 - i / 255))) for i in range(256)]
LUT_2_x_cs_1 = [util.clip(2 * i - 255) for i in range(256)]
LUT_d_cb = [_d_cb(i) for i in range(256)]


def _soft_light(im1, im2):
    """The soft light blend mode.

    Arguments:
        im1: A backdrop image (RGB).
        im2: A source image (RGB).

    Returns:
        The output image.
    """

    _1_2_x_cs = util.apply_lut(im2, LUT_1_2_x_cs)
    cb_x_1_cb = util.apply_lut(im1, LUT_cb_x_1_cb)
    c1 = util.subtract(im1, ImageChops.multiply(_1_2_x_cs, cb_x_1_cb))

    _2_x_cs_1 = util.apply_lut(im2, LUT_2_x_cs_1)
    d_cb = util.apply_lut(im1, LUT_d_cb)
    c2 = util.add(im1, ImageChops.multiply(_2_x_cs_1, d_cb))

    cm = np.where(np.asarray(im2) <= 128, np.asarray(c1), np.asarray(c2))
    return Image.fromarray(cm)


def soft_light(im1, im2):
    """Darkens or lightens the colors, depending on the source color value.

    The soft light formula is defined as:

        if(Cs <= 0.5)
            B(Cb, Cs) = Cb - (1 - 2 x Cs) x Cb x (1 - Cb)
        else
            B(Cb, Cs) = Cb + (2 x Cs - 1) x (D(Cb) - Cb)

    where

        if(Cb <= 0.25)
            D(Cb) = ((16 * Cb - 12) x Cb + 4) x Cb
        else
            D(Cb) = sqrt(Cb)

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingsoftlight

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).

    Returns:
        The output image.
    """

    return alpha_blend(im1, im2, _soft_light)
