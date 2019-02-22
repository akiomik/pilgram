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

from pilgram.css.blending.nonseparable import set_lum, set_sat, sat, lum_im


def _hue(cb, cs, lum_cb):
    """Returns ImageMath operands for hue blend mode"""
    cb = [_float(c) for c in cb]
    cs = [_float(c) for c in cs]
    lum_cb = _float(lum_cb)

    return set_lum(set_sat(cs, sat(cb)), lum_cb)


def hue(im1, im2):
    """Creates a color with the hue of the source color
    and the saturation and luminosity of the backdrop color.

    The hue formula is defined as:

        B(Cb, Cs) = SetLum(SetSat(Cs, Sat(Cb)), Lum(Cb))

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendinghue

    Arguments:
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    r1, g1, b1 = im1.split()  # Cb
    r2, g2, b2 = im2.split()  # Cs
    lum_cb = lum_im(im1)      # Lum(Cb)

    bands = ImageMath.eval(
            'f((r1, g1, b1), (r2, g2, b2), lum_cb)',
            f=_hue, r1=r1, g1=g1, b1=b1, r2=r2, g2=g2, b2=b2, lum_cb=lum_cb)
    bands = [_convert(band, 'L').im for band in bands]

    return Image.merge('RGB', bands)
