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

from PIL import Image, ImageMath
from PIL.ImageMath import imagemath_convert as _convert
from PIL.ImageMath import imagemath_float as _float


def _soft_light(cb, cs, d_cb):
    """Returns ImageMath operands for soft light"""

    cb = _float(cb) / 255
    cs = _float(cs) / 255
    d_cb = _float(d_cb) / 255

    c1 = (cs <= .5) * (cb - (1 - 2 * cs) * cb * (1 - cb))
    c2 = (cs > .5) * (cb + (2 * cs - 1) * d_cb)

    return _convert((c1 + c2) * 255, 'L')


def _d_cb(cb):
    """Returns D(Cb) - Cb"""

    cb /= 255

    if cb <= .25:
        d = ((16 * cb - 12) * cb + 4) * cb
    else:
        d = math.sqrt(cb)

    return round((d - cb) * 255)


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
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    inputs = zip(
        im1.split(),               # Cb
        im2.split(),               # Cs
        im1.point(_d_cb).split(),  # D(Cb) - Cb
    )

    return Image.merge('RGB', [
        ImageMath.eval(
            'f(cb, cs, d_cb)', f=_soft_light, cb=cb, cs=cs, d_cb=d_cb)
        for cb, cs, d_cb in inputs
    ])
