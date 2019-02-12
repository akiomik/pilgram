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


def reyes(im):
    """Applies Reyes filter.

    Arguments:
        im: An input image.

    Returns:
        The output image.
    """

    cb = im.convert('RGB')

    cs = util.fill(cb.size, [239, 205, 173])
    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .5)

    cr = css.sepia(cr, .22)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = css.contrast(cr, .85)
    cr = ImageEnhance.Color(cr).enhance(.75)

    return cr.convert(im.mode)
