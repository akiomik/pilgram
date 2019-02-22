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

from PIL import Image, ImageMath
from PIL.ImageMath import imagemath_convert as _convert
from PIL.ImageMath import imagemath_float as _float
from PIL.ImageMath import imagemath_min as _min
from PIL.ImageMath import imagemath_max as _max


def _min3(c):
    """Returns minimum value of 3 elements as ImageMath operands."""
    r, g, b = c
    return _min(_min(r, g), b)


def _max3(c):
    """Returns maximum value of 3 elements as ImageMath operands."""
    r, g, b = c
    return _max(_max(r, g), b)


def _lum_(c):
    """Returns luminosity as ImageMath operands.

    The formula is defined as:

        Lum(C) = 0.3 x Cred + 0.59 x Cgreen + 0.11 x Cblue

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """
    r, g, b = c
    return r * .3 + g * .59 + b * .11


def _lum(im):
    """Returns luminosity as image."""
    matrix = [
        .3, .59, .11, 0,
        .3, .59, .11, 0,
        .3, .59, .11, 0,
    ]
    return im.convert('RGB', matrix).split()[0]


def _clip_color(c):
    """Returns clipped color as ImageMath operands.

    The formula is defined as:

        ClipColor(C)
            L = Lum(C)
            n = min(Cred, Cgreen, Cblue)
            x = max(Cred, Cgreen, Cblue)
            if(n < 0)
                C = L + (((C - L) * L) / (L - n))

            if(x > 1)
                C = L + (((C - L) * (1 - L)) / (x - L))

            return C

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """

    r, g, b = c

    L = _lum_(c)
    n = _min3(c)
    x = _max3(c)

    # C = L + ((C - L) * L) / (L - n)
    #   = (L * (L - n)) / (L - n) + ((C - L) * L) / (L - n)
    #   = ((L * (L - n)) + ((C - L) * L)) / (L - n)
    #   = (L^2 - nL + CL - L^2) / (L - n)
    #   = (CL - nL) / (L - n)
    #   = (L * (C - n)) / (L - n)
    r = (n < 0) * ((L * (r - n)) / (L - n)) + (n >= 0) * r
    g = (n < 0) * ((L * (g - n)) / (L - n)) + (n >= 0) * g
    b = (n < 0) * ((L * (b - n)) / (L - n)) + (n >= 0) * b

    r = (x > 1) * (L + ((r - L) * (1 - L)) / (x - L)) + (x <= 1) * r
    g = (x > 1) * (L + ((g - L) * (1 - L)) / (x - L)) + (x <= 1) * g
    b = (x > 1) * (L + ((b - L) * (1 - L)) / (x - L)) + (x <= 1) * b

    return (r, g, b)


def _set_lum(c, l1, l2):
    """Set luminosity to the color

    The formula is defined as:

        SetLum(C, l)
            d = l - Lum(C)
            Cred = Cred + d
            Cgreen = Cgreen + d
            Cblue = Cblue + d
            return ClipColor(C)

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """

    r, g, b = c
    d = l1 - l2

    return _clip_color((r + d, g + d, b + d))


def _color(cs, lum_cb, lum_cs):
    """Returns ImageMath operands for color"""
    cs = [_float(c) / 255 for c in cs]
    lum_cb = _float(lum_cb) / 255
    lum_cs = _float(lum_cs) / 255

    cm = _set_lum(cs, lum_cb, lum_cs)
    return [c * 255 for c in cm]


def color(im1, im2):
    """Creates a color with the hue and saturation of the source color
    and the luminosity of the backdrop color.

    The color formula is defined as:

        B(Cb, Cs) = SetLum(Cs, Lum(Cb))

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingcolor

    Arguments:
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    r, g, b = im2.split()  # Cs
    lum_cb = _lum(im1)     # Lum(Cb)
    lum_cs = _lum(im2)     # Lum(C) in SetLum

    bands = ImageMath.eval(
            'f((r, g, b), lum_cb, lum_cs)',
            f=_color, r=r, g=g, b=b, lum_cb=lum_cb, lum_cs=lum_cs)
    bands = [_convert(band, 'L').im for band in bands]

    return Image.merge('RGB', bands)
