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

from PIL import Image, ImageMath, ImageChops


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
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    cs_inverted = ImageChops.invert(im2)
    bands = [
        ImageMath.eval(
            '(cb / cs_inv) * 255', cb=cb, cs_inv=cs_inv).convert('L')
        for cb, cs_inv in zip(im1.split(), cs_inverted.split())
    ]

    return Image.merge('RGB', bands)
