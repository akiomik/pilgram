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


def sutro(im):
    """Applies Sutro filter inspired by instagram.css

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    radial_gradient = util.radial_gradient(
        cb.size, [[0, 0, 0, 0], [0, 0, 0, 0.50]], [0.5, 0.9]
    )

    cr = css.blending.darken(cb, radial_gradient)
    cr = css.sepia(cr, 0.4)
    cr = css.contrast(cr, 1.2)
    cr = css.brightness(cr, 0.9)
    cr = css.saturate(cr, 1.4)
    cr = css.hue_rotate(cr, -10)

    return cr
