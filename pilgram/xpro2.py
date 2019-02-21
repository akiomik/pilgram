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


def xpro2(im):
    """Applies X-pro II filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs1 = util.fill(cb.size, [230, 231, 224])
    cs2 = util.fill(cb.size, [43, 42, 161])
    cs2 = Image.blend(cb, cs2, .6)

    gradient_mask = util.radial_gradient_mask(cb.size, length=.4, scale=1.1)
    cs = Image.composite(cs1, cs2, gradient_mask)

    # TODO: improve alpha blending
    cm1 = css.blending.color_burn(cb, cs)
    cm2 = cm1.copy()
    cm2 = Image.blend(cb, cm2, .6)
    cr = Image.composite(cm1, cm2, gradient_mask)

    cr = css.sepia(cr, .3)

    return cr
