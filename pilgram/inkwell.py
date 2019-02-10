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

from PIL import ImageEnhance

from pilgram import css


def inkwell(im):
    cb = im.convert('RGB')

    cr = css.sepia(cb, .3)
    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = css.grayscale(cr)

    return cr.convert(im.mode)
