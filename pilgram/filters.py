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

import math

from image4layer import Image4Layer
import numpy as np
from PIL import Image, ImageEnhance, ImageChops

from .grayscale import grayscale
from .hue_rotate import hue_rotate
from .sepia import sepia


def _linear_gradient_mask(shape, start, end, is_horizontal=True):
    if is_horizontal:
        row = np.linspace(start, end, shape[0], dtype=np.uint8)
        mask = np.tile(row, (shape[1], 1, 1))
    else:
        row = np.linspace(start, end, shape[1], dtype=np.uint8)
        mask = np.tile(row, (shape[0], 1, 1)).transpose(1, 0, 2)

    return Image.fromarray(mask).convert('L')


def _radial_gradient_mask(shape, length=0., end=1.):
    if (length >= 1):
        mask = np.full(shape, 255, dtype=np.uint8)
        return Image.fromarray(mask)

    w, h = shape
    x, y = np.ogrid[:w, :h]
    cx = w / 2
    cy = h / 2
    r = math.sqrt(cx ** 2 + cy ** 2)
    end_factor = (1 / end) ** 2 if end > 1 else (1 / end)  # TODO

    def adjust_length(x):
        return (((x / r) - length) / (1 - length)) * end_factor

    mask = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)  # distance from center
    mask = np.apply_along_axis(adjust_length, 0, mask)
    mask = np.clip(mask, 0, 1)
    mask = np.round(255 * (1 - mask))  # invert: distance to center

    return Image.fromarray(np.uint8(mask))


def _1977(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [243, 106, 188], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = ImageChops.screen(cb, cs)

    cr = Image.blend(cb, cs, .3)

    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = ImageEnhance.Color(cr).enhance(1.3)

    return cr.convert(im.mode)


def aden(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [66, 10, 14], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = ImageChops.darker(cb, cs)

    alpha_mask = _linear_gradient_mask(cb.size, [204] * 3, [255] * 3)
    cr = Image.composite(cb, cs, alpha_mask)

    cr = hue_rotate(cr, -20)
    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = ImageEnhance.Color(cr).enhance(.85)
    cr = ImageEnhance.Brightness(cr).enhance(1.2)

    return cr.convert(im.mode)


def brannan(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [161, 44, 199], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = ImageChops.lighter(cb, cs)

    cr = Image.blend(cb, cs, .31)
    cr = sepia(cr, .5)
    cr = ImageEnhance.Contrast(cr).enhance(1.4)

    return cr.convert(im.mode)


def brooklyn(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [168, 223, 193], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [196, 183, 200], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask = _radial_gradient_mask(cb.size, length=.7)
    cs = Image.composite(cs1, cs2, gradient_mask)
    cs = Image4Layer.overlay(cb, cs)

    # TODO: improve alpha masking
    alpha_mask_array = np.array(gradient_mask) * .6
    alpha_mask = Image.fromarray(np.uint8(alpha_mask_array.round()))
    cr = Image.composite(cb, cs, alpha_mask)

    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)

    return cr.convert(im.mode)


def clarendon(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [127, 187, 227], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = Image4Layer.overlay(cb, cs)

    cr = Image.blend(cb, cs, .2)

    cr = ImageEnhance.Contrast(cr).enhance(1.2)
    cr = ImageEnhance.Color(cr).enhance(1.35)

    return cr.convert(im.mode)


def earlybird(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [208, 186, 142], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [54, 3, 9], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    cs3_array = np.full(cb.size + (3,), [29, 2, 16], dtype=np.uint8)
    cs3 = Image.fromarray(cs3_array)

    gradient_mask1 = _radial_gradient_mask(cb.size, length=.2)
    cs = Image.composite(cs1, cs2, gradient_mask1)

    gradient_mask2 = _radial_gradient_mask(cb.size, length=.85)
    cs = Image.composite(cs, cs3, gradient_mask2)

    cr = Image4Layer.overlay(cb, cs)

    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = sepia(cr, .2)

    return cr.convert(im.mode)


def gingham(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [230, 230, 250], dtype=np.uint8)
    cs = Image.fromarray(cs_array)

    cr = Image4Layer.soft_light(cb, cs)

    cr = ImageEnhance.Brightness(cr).enhance(1.05)
    cr = hue_rotate(cr, -10)

    return cr.convert(im.mode)


def hudson(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [166, 177, 255], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [52, 33, 52], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask = _radial_gradient_mask(cb.size, length=.5)
    cs = Image.composite(cs1, cs2, gradient_mask)
    cs = ImageChops.multiply(cb, cs)

    cr = Image.blend(cb, cs, .5)

    cr = ImageEnhance.Brightness(cr).enhance(1.2)
    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = ImageEnhance.Color(cr).enhance(1.1)

    return cr.convert(im.mode)


def inkwell(im):
    cb = im.convert('RGB')

    cr = sepia(cb, .3)
    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = grayscale(cr)

    return cr.convert(im.mode)


def kelvin(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [56, 44, 52], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [183, 125, 33], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    cs = Image4Layer.color_dodge(cb, cs1)
    cr = Image4Layer.overlay(cs, cs2)

    return cr.convert(im.mode)


def lark(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [34, 37, 63], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [242, 242, 242], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    cs = Image4Layer.color_dodge(cb, cs1)
    cs = ImageChops.darker(cs, cs2)

    cr = Image.blend(cb, cs, .8)

    return cr.convert(im.mode)


def lofi(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [34, 34, 34], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = ImageChops.multiply(cb, cs)

    mask = _radial_gradient_mask(cb.size, length=.7, end=1.5)
    cr = Image.composite(cb, cs, mask)

    cr = ImageEnhance.Color(cr).enhance(1.1)
    cr = ImageEnhance.Contrast(cr).enhance(1.5)

    return cr.convert(im.mode)


def maven(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [3, 230, 26], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = Image4Layer.hue(cb, cs)

    cr = Image.blend(cb, cs, .2)

    cr = sepia(cr, .25)
    cr = ImageEnhance.Brightness(cr).enhance(.95)
    cr = ImageEnhance.Contrast(cr).enhance(.95)
    cr = ImageEnhance.Color(cr).enhance(1.5)

    return cr.convert(im.mode)


def mayfair(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [255, 255, 255], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [255, 200, 200], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    cs3_array = np.full(cb.size + (3,), [17, 17, 17], dtype=np.uint8)
    cs3 = Image.fromarray(cs3_array)

    gradient_mask1 = _radial_gradient_mask(cb.size)
    cs = Image.composite(cs1, cs2, gradient_mask1)

    # TODO: improve gradient mask
    gradient_mask2 = _radial_gradient_mask(cb.size, length=.3, end=.6)
    cs = Image.composite(cs, cs3, gradient_mask2)

    cs = Image4Layer.overlay(cb, cs)

    alpha_mask1_array = np.array(gradient_mask1) * .2
    alpha_mask1 = Image.fromarray(np.uint8(alpha_mask1_array.round()))
    cs = Image.composite(cb, cs, alpha_mask1)

    alpha_mask2_array = np.array(gradient_mask2) * .4
    alpha_mask2 = Image.fromarray(np.uint8(alpha_mask2_array.round()))
    cs = Image.composite(cb, cs, alpha_mask2)

    cr = Image.blend(cb, cs, .4)

    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Color(cr).enhance(1.1)

    return cr.convert(im.mode)


def moon(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [160, 160, 160], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [56, 56, 56], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    cs = Image4Layer.soft_light(cb, cs1)
    cr = ImageChops.lighter(cs, cs2)

    cr = grayscale(cr)
    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)

    return cr.convert(im.mode)


def nashville(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [247, 176, 153], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs = ImageChops.darker(cb, cs1)
    cs = Image.blend(cb, cs, .56)

    cs2_array = np.full(cb.size + (3,), [0, 70, 150], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    cs_ = ImageChops.lighter(cs, cs2)
    cr = Image.blend(cs, cs_, .4)

    cr = sepia(cr, .2)
    cr = ImageEnhance.Contrast(cr).enhance(1.2)
    cr = ImageEnhance.Brightness(cr).enhance(1.05)
    cr = ImageEnhance.Color(cr).enhance(1.2)

    return cr.convert(im.mode)


def perpetua(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [0, 91, 154], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [230, 193, 61], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask = _linear_gradient_mask(cb.size, [255] * 3, [0] * 3, False)
    cs = Image.composite(cs1, cs2, gradient_mask)

    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .5)

    return cr.convert(im.mode)


def reyes(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [239, 205, 173], dtype=np.uint8)
    cs = Image.fromarray(cs_array)

    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .5)

    cr = sepia(cr, .22)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = ImageEnhance.Contrast(cr).enhance(.85)
    cr = ImageEnhance.Color(cr).enhance(.75)

    return cr.convert(im.mode)


def rise(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [236, 205, 169], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [50, 30, 7], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask1 = _radial_gradient_mask(cb.size, length=.55)
    cs = Image.composite(cs1, cs2, gradient_mask1)
    cs = ImageChops.multiply(cb, cs)

    # TODO
    alpha_mask1_array = np.array(gradient_mask1) * .85
    alpha_mask1 = Image.fromarray(np.uint8(alpha_mask1_array.round()))
    cs = Image.composite(cb, cs, alpha_mask1)

    alpha_mask2_array = 255. - ((255. - np.array(gradient_mask1)) * .4)
    alpha_mask2 = Image.fromarray(np.uint8(alpha_mask2_array.round()))
    cs = Image.composite(cb, cs, alpha_mask2)

    cs3_array = np.full(cb.size + (3,), [232, 197, 152], dtype=np.uint8)
    cs3 = Image.fromarray(cs3_array)

    # TODO
    alpha_mask3 = _radial_gradient_mask(cb.size, end=.9)
    gradient_mask2 = ImageChops.invert(alpha_mask3)
    cs_ = Image.composite(cs, cs3, gradient_mask2)

    cs_ = Image4Layer.overlay(cs, cs_)
    cs_ = Image.composite(cs, cs_, alpha_mask3)

    alpha_mask4_array = np.array(gradient_mask2) * .2
    alpha_mask4 = Image.fromarray(np.uint8(alpha_mask4_array.round()))
    cs_ = Image.composite(cs, cs_, alpha_mask4)

    cr = Image.blend(cs, cs_, .6)

    cr = ImageEnhance.Brightness(cr).enhance(1.05)
    cr = sepia(cr, .2)
    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = ImageEnhance.Color(cr).enhance(.9)

    return cr.convert(im.mode)


def slumber(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [69, 41, 12], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)
    cs = ImageChops.lighter(cb, cs1)
    cs = Image.blend(cb, cs, .4)

    cs2_array = np.full(cb.size + (3,), [125, 105, 24], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)
    cs_ = Image4Layer.soft_light(cs, cs2)
    cr = Image.blend(cs, cs_, .5)

    cr = ImageEnhance.Color(cr).enhance(.66)
    cr = ImageEnhance.Brightness(cr).enhance(1.05)

    return cr.convert(im.mode)


def stinson(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [240, 149, 128], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .2)

    cr = ImageEnhance.Contrast(cr).enhance(.75)
    cr = ImageEnhance.Color(cr).enhance(.85)
    cr = ImageEnhance.Brightness(cr).enhance(1.15)

    return cr.convert(im.mode)


def toaster(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [128, 78, 15], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [59, 0, 59], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask = _radial_gradient_mask(cb.size)
    cs = Image.composite(cs1, cs2, gradient_mask)
    cr = ImageChops.screen(cb, cs)

    cr = ImageEnhance.Contrast(cr).enhance(1.5)
    cr = ImageEnhance.Brightness(cr).enhance(.9)

    return cr.convert(im.mode)


def valencia(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [58, 3, 57], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = Image4Layer.exclusion(cb, cs)
    cr = Image.blend(cb, cs, .5)

    cr = ImageEnhance.Contrast(cr).enhance(1.08)
    cr = ImageEnhance.Brightness(cr).enhance(1.08)
    cr = sepia(cr, .08)

    return cr.convert(im.mode)


def walden(im):
    cb = im.convert('RGB')

    cs_array = np.full(cb.size + (3,), [0, 68, 204], dtype=np.uint8)
    cs = Image.fromarray(cs_array)
    cs = ImageChops.screen(cb, cs)
    cr = Image.blend(cb, cs, .3)

    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = hue_rotate(cr, -10)
    cr = sepia(cr, .3)
    cr = ImageEnhance.Color(cr).enhance(1.6)

    return cr.convert(im.mode)


def willow(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [212, 169, 175], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [0, 0, 0], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask = _radial_gradient_mask(cb.size, length=.55, end=1.5)
    cs = Image.composite(cs1, cs2, gradient_mask)
    cs = Image4Layer.overlay(cb, cs)

    cs3_array = np.full(cb.size + (3,), [216, 205, 203], dtype=np.uint8)
    cs3 = Image.fromarray(cs3_array)
    cr = Image4Layer.color(cs, cs3)

    cr = grayscale(cr, .5)
    cr = ImageEnhance.Contrast(cr).enhance(.95)
    cr = ImageEnhance.Brightness(cr).enhance(.9)

    return cr.convert(im.mode)


def xpro2(im):
    cb = im.convert('RGB')

    cs1_array = np.full(cb.size + (3,), [230, 231, 224], dtype=np.uint8)
    cs1 = Image.fromarray(cs1_array)

    cs2_array = np.full(cb.size + (3,), [43, 42, 161], dtype=np.uint8)
    cs2 = Image.fromarray(cs2_array)

    gradient_mask = _radial_gradient_mask(cb.size, length=.4, end=1.1)
    cs = Image.composite(cs1, cs2, gradient_mask)
    cs = Image4Layer.color_burn(cb, cs)

    alpha_mask_array = np.array(gradient_mask)
    alpha_mask_array = (255 - alpha_mask_array) * .6
    alpha_mask = Image.fromarray(np.uint8(alpha_mask_array.round()))
    cr = Image.composite(cb, cs, alpha_mask)

    cr = sepia(cr, .3)

    return cr.convert(im.mode)
