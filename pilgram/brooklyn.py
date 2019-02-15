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

from image4layer import Image4Layer
from PIL import Image, ImageEnhance

from pilgram import css
from pilgram import util


def brooklyn(im):
    """Applies Brooklyn filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [168, 223, 193, .4])
    cm1 = Image4Layer.overlay(cb, cs1)

    cs2 = util.fill(cb.size, [196, 183, 200])
    cm2 = Image4Layer.overlay(cb, cs2)

    gradient_mask = util.radial_gradient_mask(cb.size, length=.7)
    cr = Image.composite(cm1, cm2, gradient_mask)

    cr = css.contrast(cr, .9)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)

    return cr.convert(im.mode)
