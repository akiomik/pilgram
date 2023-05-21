# Copyright 2023 Michael G.
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


def ludwig(im):
    """Applies ludwig filter inspired by instagram.css

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    cs = util.fill(cb.size, [125, 105, 24, 0.1])

    cr = css.blending.overlay(cb, cs)
    cr = css.sepia(cr, 0.25)
    cr = css.contrast(cr, 1.05)
    cr = css.brightness(cr, 1.05)
    cr = css.saturate(cr, 2)

    return cr
