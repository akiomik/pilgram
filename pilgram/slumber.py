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

from pilgram import css
from pilgram import util


def slumber(im):
    """Applies Slumber filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs1 = util.fill(cb.size, [69, 41, 12, .4])
    cm = css.blending.lighten(cb, cs1)

    cs2 = util.fill(cb.size, [125, 105, 24, .5])
    cr = css.blending.soft_light(cm, cs2)

    cr = css.saturate(cr, .66)
    cr = css.brightness(cr, 1.05)

    return cr
