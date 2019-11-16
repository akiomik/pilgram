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

from pilgram.css.blending.alpha import alpha_blend


def _color_burn_image_math(cb, cs):
    """Returns ImageMath operands for color burn blend mode"""
    cm = (cb == 255) * 255 + \
        (cb < 255) * (cs > 0) * (255 - ((255 - cb) * 255 / cs))
    return _convert(cm, 'L')


def _color_burn(im1, im2):
    """The color burn blend mode.

    Arguments:
        im1: A backdrop image (RGB).
        im2: A source image (RGB).

    Returns:
        The output image.
    """

    return Image.merge('RGB', [
        ImageMath.eval('f(cb, cs)', f=_color_burn_image_math, cb=cb, cs=cs)
        for cb, cs in zip(im1.split(), im2.split())
    ])


def color_burn(im1, im2):
    """Darkens the backdrop color to reflect the source color.

    The color burn formula is defined as:

        if(Cb == 1)
            B(Cb, Cs) = 1
        else if(Cs == 0)
            B(Cb, Cs) = 0
        else
            B(Cb, Cs) = 1 - min(1, (1 - Cb) / Cs)

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingcolorburn

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).

    Returns:
        The output image.
    """

    return alpha_blend(im1, im2, _color_burn)
