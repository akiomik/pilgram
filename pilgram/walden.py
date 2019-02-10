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

from PIL import Image, ImageEnhance, ImageChops

from pilgram import css
from pilgram import util


def walden(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [0, 68, 204])
    cs = ImageChops.screen(cb, cs)
    cr = Image.blend(cb, cs, .3)

    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = css.hue_rotate(cr, -10)
    cr = css.sepia(cr, .3)
    cr = ImageEnhance.Color(cr).enhance(1.6)

    return cr.convert(im.mode)
