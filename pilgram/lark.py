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
from PIL import Image, ImageChops

from pilgram import util


def lark(im):
    """Applies Lark filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [34, 37, 63])
    cs = Image4Layer.color_dodge(cb, cs1)

    cs2 = util.fill(cb.size, [242, 242, 242])
    cs = ImageChops.darker(cs, cs2)
    cr = Image.blend(cb, cs, .8)

    return cr.convert(im.mode)
