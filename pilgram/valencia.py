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


def valencia(im):
    """Applies Valencia filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.fill(cb.size, [58, 3, 57])
    cs = css.blending.exclusion(cb, cs)
    cr = Image.blend(cb, cs, .5)  # opacity

    cr = css.contrast(cr, 1.08)
    cr = css.brightness(cr, 1.08)
    cr = css.sepia(cr, .08)

    return cr
