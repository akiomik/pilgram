
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
from PIL import Image, ImageEnhance

from pilgram import css
from pilgram import util


def mayfair(im):
    """Applies Mayfair filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = im.convert('RGB')
    size = cb.size
    pos = (.4, .4)

    cs1 = util.fill(size, [255, 255, 255])
    cm1 = Image4Layer.overlay(cb, cs1)
    cm1 = Image.blend(cb, cm1, .8)

    cs2 = util.fill(size, [255, 200, 200])
    cm2 = Image4Layer.overlay(cb, cs2)
    cm2 = Image.blend(cb, cm2, .6)

    cs3 = util.fill(size, [17, 17, 17])
    cm3 = Image4Layer.overlay(cb, cs3)

    mask1 = util.radial_gradient_mask(size, scale=.3, position=pos)
    cs = Image.composite(cm1, cm2, mask1)

    mask2 = util.radial_gradient_mask(size, length=.3, scale=.6, position=pos)
    cs = Image.composite(cs, cm3, mask2)
    cr = Image.blend(cb, cs, .4)

    cr = css.contrast(cr, 1.1)
    cr = ImageEnhance.Color(cr).enhance(1.1)

    return cr.convert(im.mode)
