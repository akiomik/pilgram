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


def walden(im):
    """Applies Walden filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.fill(cb.size, [0, 68, 204])
    cs = css.blending.screen(cb, cs)
    cr = Image.blend(cb, cs, .3)  # opacity

    cr = css.brightness(cr, 1.1)
    cr = css.hue_rotate(cr, -10)
    cr = css.sepia(cr, .3)
    cr = css.saturate(cr, 1.6)

    return cr
