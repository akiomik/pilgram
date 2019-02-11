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
from PIL import Image, ImageEnhance, ImageChops

from pilgram import util


def slumber(im):
    """Applies Slumber filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [69, 41, 12])
    cs = ImageChops.lighter(cb, cs1)
    cs = Image.blend(cb, cs, .4)

    cs2 = util.fill(cb.size, [125, 105, 24])
    cs_ = Image4Layer.soft_light(cs, cs2)
    cr = Image.blend(cs, cs_, .5)

    cr = ImageEnhance.Color(cr).enhance(.66)
    cr = ImageEnhance.Brightness(cr).enhance(1.05)

    return cr.convert(im.mode)
