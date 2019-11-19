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

from pilgram import util
from pilgram import css


def lofi(im):
    """Applies Lo-Fi filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.fill(cb.size, [34, 34, 34])
    cs = css.blending.multiply(cb, cs)

    mask = util.radial_gradient_mask(cb.size, length=.7, scale=1.5)
    cr = Image.composite(cb, cs, mask)

    cr = css.saturate(cr, 1.1)
    cr = css.contrast(cr, 1.5)

    return cr
