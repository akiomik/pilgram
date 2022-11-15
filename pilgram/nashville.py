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

from pilgram import css, util


def nashville(im):
    """Applies Nashville filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    cs1 = util.fill(cb.size, [247, 176, 153, 0.56])
    cm1 = css.blending.darken(cb, cs1)

    cs2 = util.fill(cb.size, [0, 70, 150, 0.4])
    cr = css.blending.lighten(cm1, cs2)

    cr = css.sepia(cr, 0.2)
    cr = css.contrast(cr, 1.2)
    cr = css.brightness(cr, 1.05)
    cr = css.saturate(cr, 1.2)

    return cr
