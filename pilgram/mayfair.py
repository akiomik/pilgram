
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

from PIL import Image

from pilgram import css
from pilgram import util


def mayfair(im):
    """Applies Mayfair filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')
    size = cb.size
    pos = (.4, .4)

    cs1 = util.fill(size, [255, 255, 255, .8])
    cm1 = css.blending.overlay(cb, cs1)

    cs2 = util.fill(size, [255, 200, 200, .6])
    cm2 = css.blending.overlay(cb, cs2)

    cs3 = util.fill(size, [17, 17, 17])
    cm3 = css.blending.overlay(cb, cs3)

    mask1 = util.radial_gradient_mask(size, scale=.3, center=pos)
    cs = Image.composite(cm1, cm2, mask1)

    mask2 = util.radial_gradient_mask(size, length=.3, scale=.6, center=pos)
    cs = Image.composite(cs, cm3, mask2)
    cr = Image.blend(cb, cs, .4)  # opacity

    cr = css.contrast(cr, 1.1)
    cr = css.saturate(cr, 1.1)

    return cr
