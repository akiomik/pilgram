
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

from pilgram import util


def mayfair(im):
    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [255, 255, 255])
    cs2 = util.fill(cb.size, [255, 200, 200])
    cs3 = util.fill(cb.size, [17, 17, 17])

    mask_pos = (.4, .4)
    mask_scale = .6

    gradient_mask1 = util.radial_gradient_mask(
            cb.size, scale=mask_scale, position=mask_pos)
    cs = Image.composite(cs1, cs2, gradient_mask1)

    gradient_mask2 = util.radial_gradient_mask(
            cb.size, length=.3, scale=mask_scale, position=mask_pos)
    cs = Image.composite(cs, cs3, gradient_mask2)
    cs = Image4Layer.overlay(cb, cs)

    # TODO: improve alpha masking
    alpha_mask1 = util.scale_color(gradient_mask1, .2)
    cs = Image.composite(cb, cs, alpha_mask1)

    # TODO: improve alpha masking
    alpha_mask2 = util.scale_color(gradient_mask2, .4)
    cs = Image.composite(cb, cs, alpha_mask2)
    cr = Image.blend(cb, cs, .4)

    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Color(cr).enhance(1.1)

    return cr.convert(im.mode)
