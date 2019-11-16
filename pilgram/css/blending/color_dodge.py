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

from pilgram.css.blending.alpha import alpha_blend
from pilgram.util import invert


def _color_dodge_image_math(cb, cs_inv):
    """Returns ImageMath operands for color dodge blend mode"""
    cb = _float(cb)
    cs_inv = _float(cs_inv)

    cm = ((cb != 0) * (cs_inv == 0) + (cb / cs_inv)) * 255
    return _convert(cm, 'L')


def _color_dodge(im1, im2):
    """The color dodge blend mode.

    Arguments:
        im1: A backdrop image (RGB).
        im2: A source image (RGB).

    Returns:
        The output image.
    """

    return Image.merge('RGB', [
        ImageMath.eval(
            'f(cb, cs_inv)', f=_color_dodge_image_math, cb=cb, cs_inv=cs_inv)
        for cb, cs_inv in zip(im1.split(), invert(im2).split())
    ])


def color_dodge(im1, im2):
    """Brightens the backdrop color to reflect the source color.

    The color dodge formula is defined as:

        if(Cb == 0)
            B(Cb, Cs) = 0
        else if(Cs == 1)
            B(Cb, Cs) = 1
        else
            B(Cb, Cs) = min(1, Cb / (1 - Cs))

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingcolordodge

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).

    Returns:
        The output image.
    """

    return alpha_blend(im1, im2, _color_dodge)
