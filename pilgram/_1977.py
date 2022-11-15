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


def _1977(im):
    """Applies 1977 filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    cs = util.fill(cb.size, [243, 106, 188, 0.3])
    cr = css.blending.screen(cb, cs)

    cr = css.contrast(cr, 1.1)
    cr = css.brightness(cr, 1.1)
    cr = css.saturate(cr, 1.3)

    return cr
