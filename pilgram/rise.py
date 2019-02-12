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

from image4layer import Image4Layer
from PIL import Image, ImageEnhance, ImageChops

from pilgram import css
from pilgram import util


def rise(im):
    """Applies Rise filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [236, 205, 169])
    cs2 = util.fill(cb.size, [50, 30, 7])
    cs3 = util.fill(cb.size, [232, 197, 152])

    gradient_mask1 = util.radial_gradient_mask(cb.size, length=.55)
    cs = Image.composite(cs1, cs2, gradient_mask1)
    cs = ImageChops.multiply(cb, cs)

    # TODO
    alpha_mask1 = util.scale_color(gradient_mask1, .85)
    cs = Image.composite(cb, cs, alpha_mask1)

    alpha_mask2 = util.scale_color(gradient_mask1, .4)
    cs = Image.composite(cb, cs, alpha_mask2)

    # TODO
    alpha_mask3 = util.radial_gradient_mask(cb.size, scale=.9)
    gradient_mask2 = ImageChops.invert(alpha_mask3)
    cs_ = Image.composite(cs, cs3, gradient_mask2)

    cs_ = Image4Layer.overlay(cs, cs_)
    cs_ = Image.composite(cs, cs_, alpha_mask3)

    alpha_mask4 = util.scale_color(gradient_mask2, .2)
    cs_ = Image.composite(cs, cs_, alpha_mask4)
    cr = Image.blend(cs, cs_, .6)

    cr = ImageEnhance.Brightness(cr).enhance(1.05)
    cr = css.sepia(cr, .2)
    cr = css.contrast(cr, .9)
    cr = ImageEnhance.Color(cr).enhance(.9)

    return cr.convert(im.mode)
