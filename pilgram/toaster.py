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

from PIL import ImageEnhance, ImageChops

from pilgram import util


def toaster(im):
    cb = im.convert('RGB')

    cs = util.radial_gradient(cb.size, ([128, 78, 15], 0), ([59, 0, 59], 1))
    cr = ImageChops.screen(cb, cs)

    cr = ImageEnhance.Contrast(cr).enhance(1.5)
    cr = ImageEnhance.Brightness(cr).enhance(.9)

    return cr.convert(im.mode)
