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

from pilgram.css.blending.nonseparable import set_lum_im, lum_im
from pilgram.css.blending.alpha import alpha_blend


def _color_image_math(cs, lum_cb, lum_cs):
    """Returns ImageMath operands for color blend mode"""
    cs = [_float(c) for c in cs]
    lum_cb = _float(lum_cb)
    lum_cs = _float(lum_cs)

    return set_lum_im(cs, lum_cb, lum_cs)


def _color(im1, im2):
    """The color blend mode.

    Arguments:
        im1: A backdrop image (RGB).
        im2: A source image (RGB).

    Returns:
        The output image.
    """

    r, g, b = im2.split()  # Cs
    lum_cb = lum_im(im1)   # Lum(Cb)
    lum_cs = lum_im(im2)   # Lum(C) in SetLum

    bands = ImageMath.eval(
        'f((r, g, b), lum_cb, lum_cs)',
        f=_color_image_math, r=r, g=g, b=b, lum_cb=lum_cb, lum_cs=lum_cs)
    bands = [_convert(band, 'L').im for band in bands]

    return Image.merge('RGB', bands)


def color(im1, im2):
    """Creates a color with the hue and saturation of the source color
    and the luminosity of the backdrop color.

    The color formula is defined as:

        B(Cb, Cs) = SetLum(Cs, Lum(Cb))

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingcolor

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).

    Returns:
        The output image.
    """

    return alpha_blend(im1, im2, _color)
