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


def aden(im):
    """Applies Aden filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.fill(cb.size, [66, 10, 14])
    cs = css.blending.darken(cb, cs)

    alpha_mask = util.linear_gradient_mask(cb.size, start=.8)
    cr = Image.composite(cs, cb, alpha_mask)

    cr = css.hue_rotate(cr, -20)
    cr = css.contrast(cr, .9)
    cr = css.saturate(cr, .85)
    cr = css.brightness(cr, 1.2)

    return cr
