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

from pilgram import css, util


def hudson(im):
    """Applies Hudson filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = util.or_convert(im, "RGB")

    cs = util.radial_gradient(cb.size, [(166, 177, 255), (52, 33, 52)], [0.5, 1])
    cs = css.blending.multiply(cb, cs)
    cr = Image.blend(cb, cs, 0.5)  # opacity

    cr = css.brightness(cr, 1.2)
    cr = css.contrast(cr, 0.9)
    cr = css.saturate(cr, 1.1)

    return cr
