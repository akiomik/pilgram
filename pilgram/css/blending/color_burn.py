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
from PIL.ImageMath import imagemath_float as _int
from PIL.ImageMath import imagemath_min as _min


def _color_burn(cb, cs):
    rb, gb, bb = cb
    rs, gs, bs = cs

    r = _int(rs > 0) * (255 - _min((255 - rb) * 255 / rs, 255))
    g = _int(gs > 0) * (255 - _min((255 - gb) * 255 / gs, 255))
    b = _int(bs > 0) * (255 - _min((255 - bb) * 255 / bs, 255))

    return (r, g, b)


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
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()

    bands = ImageMath.eval(
            'f((r1, g1, b1), (r2, g2, b2))',
            f=_color_burn, r1=r1, g1=g1, b1=b1, r2=r2, g2=g2, b2=b2)

    return Image.merge('RGB', [_convert(band, 'L').im for band in bands])
