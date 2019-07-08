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


def earlybird(im):
    """Applies Earlybird filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.radial_gradient(
            cb.size,
            [(208, 186, 142), (54, 3, 9), (29, 2, 16)],
            [.2, .85, 1])
    cr = css.blending.overlay(cb, cs)

    cr = css.contrast(cr, .9)
    cr = css.sepia(cr, .2)

    return cr
