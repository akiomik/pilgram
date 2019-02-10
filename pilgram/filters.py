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
import numpy as np
from PIL import Image, ImageEnhance, ImageChops

from .grayscale import grayscale
from .hue_rotate import hue_rotate
from .sepia import sepia
from . import util


def _1977(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [243, 106, 188])
    cs = ImageChops.screen(cb, cs)
    cr = Image.blend(cb, cs, .3)

    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = ImageEnhance.Color(cr).enhance(1.3)

    return cr.convert(im.mode)


def aden(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [66, 10, 14])
    cs = ImageChops.darker(cb, cs)

    alpha_mask = util.linear_gradient_mask(cb.size, start=.8, end=1)
    cr = Image.composite(cb, cs, alpha_mask)

    cr = hue_rotate(cr, -20)
    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = ImageEnhance.Color(cr).enhance(.85)
    cr = ImageEnhance.Brightness(cr).enhance(1.2)

    return cr.convert(im.mode)


def brannan(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [161, 44, 199])
    cs = ImageChops.lighter(cb, cs)
    cr = Image.blend(cb, cs, .31)

    cr = sepia(cr, .5)
    cr = ImageEnhance.Contrast(cr).enhance(1.4)

    return cr.convert(im.mode)


def brooklyn(im):
    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [168, 223, 193])
    cs2 = util.fill(cb.size, [196, 183, 200])

    gradient_mask = util.radial_gradient_mask(cb.size, length=.7)
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

    cs = util.fill(cb.size, [127, 187, 227])
    cs = Image4Layer.overlay(cb, cs)
    cr = Image.blend(cb, cs, .2)

    cr = ImageEnhance.Contrast(cr).enhance(1.2)
    cr = ImageEnhance.Color(cr).enhance(1.35)

    return cr.convert(im.mode)


def earlybird(im):
    cb = im.convert('RGB')

    cs = util.radial_gradient(cb.size, [208, 186, 142], [54, 3, 9], length=.2)

    gradient_mask2 = util.radial_gradient_mask(cb.size, length=.85)
    cs3 = util.fill(cb.size, [29, 2, 16])
    cs = Image.composite(cs, cs3, gradient_mask2)
    cr = Image4Layer.overlay(cb, cs)

    cr = ImageEnhance.Contrast(cr).enhance(.9)
    cr = sepia(cr, .2)

    return cr.convert(im.mode)


def gingham(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [230, 230, 250])
    cr = Image4Layer.soft_light(cb, cs)

    cr = ImageEnhance.Brightness(cr).enhance(1.05)
    cr = hue_rotate(cr, -10)

    return cr.convert(im.mode)


def hudson(im):
    cb = im.convert('RGB')

    cs = util.radial_gradient(
            cb.size, [166, 177, 255], [52, 33, 52], length=.5)
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

    cs1 = util.fill(cb.size, [56, 44, 52])
    cs = Image4Layer.color_dodge(cb, cs1)

    cs2 = util.fill(cb.size, [183, 125, 33])
    cr = Image4Layer.overlay(cs, cs2)

    return cr.convert(im.mode)


def lark(im):
    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [34, 37, 63])
    cs = Image4Layer.color_dodge(cb, cs1)

    cs2 = util.fill(cb.size, [242, 242, 242])
    cs = ImageChops.darker(cs, cs2)
    cr = Image.blend(cb, cs, .8)

    return cr.convert(im.mode)


def lofi(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [34, 34, 34])
    cs = ImageChops.multiply(cb, cs)

    mask = util.radial_gradient_mask(cb.size, length=.7, scale=1.5)
    cr = Image.composite(cb, cs, mask)

    cr = ImageEnhance.Color(cr).enhance(1.1)
    cr = ImageEnhance.Contrast(cr).enhance(1.5)

    return cr.convert(im.mode)


def maven(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [3, 230, 26])
    cs = Image4Layer.hue(cb, cs)
    cr = Image.blend(cb, cs, .2)

    cr = sepia(cr, .25)
    cr = ImageEnhance.Brightness(cr).enhance(.95)
    cr = ImageEnhance.Contrast(cr).enhance(.95)
    cr = ImageEnhance.Color(cr).enhance(1.5)

    return cr.convert(im.mode)


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

    cs1 = util.fill(cb.size, [160, 160, 160])
    cs = Image4Layer.soft_light(cb, cs1)

    cs2 = util.fill(cb.size, [56, 56, 56])
    cr = ImageChops.lighter(cs, cs2)

    cr = grayscale(cr)
    cr = ImageEnhance.Contrast(cr).enhance(1.1)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)

    return cr.convert(im.mode)


def nashville(im):
    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [247, 176, 153])
    cs = ImageChops.darker(cb, cs1)
    cs = Image.blend(cb, cs, .56)

    cs2 = util.fill(cb.size, [0, 70, 150])
    cs_ = ImageChops.lighter(cs, cs2)
    cr = Image.blend(cs, cs_, .4)

    cr = sepia(cr, .2)
    cr = ImageEnhance.Contrast(cr).enhance(1.2)
    cr = ImageEnhance.Brightness(cr).enhance(1.05)
    cr = ImageEnhance.Color(cr).enhance(1.2)

    return cr.convert(im.mode)


def perpetua(im):
    cb = im.convert('RGB')

    cs = util.linear_gradient(cb.size, [0, 91, 154], [230, 193, 61], False)
    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .5)

    return cr.convert(im.mode)


def reyes(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [239, 205, 173])
    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .5)

    cr = sepia(cr, .22)
    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = ImageEnhance.Contrast(cr).enhance(.85)
    cr = ImageEnhance.Color(cr).enhance(.75)

    return cr.convert(im.mode)


def rise(im):
    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [236, 205, 169])
    cs2 = util.fill(cb.size, [50, 30, 7])
    cs3 = util.fill(cb.size, [232, 197, 152])

    gradient_mask1 = util.radial_gradient_mask(cb.size, length=.55)
    cs = Image.composite(cs1, cs2, gradient_mask1)
    cs = ImageChops.multiply(cb, cs)

    # TODO
    alpha_mask1_array = np.array(gradient_mask1) * .85
    alpha_mask1 = Image.fromarray(np.uint8(alpha_mask1_array.round()))
    cs = Image.composite(cb, cs, alpha_mask1)

    alpha_mask2_array = 255. - ((255. - np.array(gradient_mask1)) * .4)
    alpha_mask2 = Image.fromarray(np.uint8(alpha_mask2_array.round()))
    cs = Image.composite(cb, cs, alpha_mask2)

    # TODO
    alpha_mask3 = util.radial_gradient_mask(cb.size, scale=.9)
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

    cs1 = util.fill(cb.size, [69, 41, 12])
    cs = ImageChops.lighter(cb, cs1)
    cs = Image.blend(cb, cs, .4)

    cs2 = util.fill(cb.size, [125, 105, 24])
    cs_ = Image4Layer.soft_light(cs, cs2)
    cr = Image.blend(cs, cs_, .5)

    cr = ImageEnhance.Color(cr).enhance(.66)
    cr = ImageEnhance.Brightness(cr).enhance(1.05)

    return cr.convert(im.mode)


def stinson(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [240, 149, 128])
    cs = Image4Layer.soft_light(cb, cs)
    cr = Image.blend(cb, cs, .2)

    cr = ImageEnhance.Contrast(cr).enhance(.75)
    cr = ImageEnhance.Color(cr).enhance(.85)
    cr = ImageEnhance.Brightness(cr).enhance(1.15)

    return cr.convert(im.mode)


def toaster(im):
    cb = im.convert('RGB')

    cs = util.radial_gradient(cb.size, [128, 78, 15], [59, 0, 59])
    cr = ImageChops.screen(cb, cs)

    cr = ImageEnhance.Contrast(cr).enhance(1.5)
    cr = ImageEnhance.Brightness(cr).enhance(.9)

    return cr.convert(im.mode)


def valencia(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [58, 3, 57])
    cs = Image4Layer.exclusion(cb, cs)
    cr = Image.blend(cb, cs, .5)

    cr = ImageEnhance.Contrast(cr).enhance(1.08)
    cr = ImageEnhance.Brightness(cr).enhance(1.08)
    cr = sepia(cr, .08)

    return cr.convert(im.mode)


def walden(im):
    cb = im.convert('RGB')

    cs = util.fill(cb.size, [0, 68, 204])
    cs = ImageChops.screen(cb, cs)
    cr = Image.blend(cb, cs, .3)

    cr = ImageEnhance.Brightness(cr).enhance(1.1)
    cr = hue_rotate(cr, -10)
    cr = sepia(cr, .3)
    cr = ImageEnhance.Color(cr).enhance(1.6)

    return cr.convert(im.mode)


def willow(im):
    cb = im.convert('RGB')

    cs = util.radial_gradient(
            cb.size,
            [212, 169, 175], [0, 0, 0],
            length=.55, scale=1.5)
    cs = Image4Layer.overlay(cb, cs)

    cs3 = util.fill(cb.size, [216, 205, 203])
    cr = Image4Layer.color(cs, cs3)

    cr = grayscale(cr, .5)
    cr = ImageEnhance.Contrast(cr).enhance(.95)
    cr = ImageEnhance.Brightness(cr).enhance(.9)

    return cr.convert(im.mode)


def xpro2(im):
    cb = im.convert('RGB')

    cs1 = util.fill(cb.size, [230, 231, 224])
    cs2 = util.fill(cb.size, [43, 42, 161])

    gradient_mask = util.radial_gradient_mask(cb.size, length=.4, scale=1.1)
    cs = Image.composite(cs1, cs2, gradient_mask)
    cs = Image4Layer.color_burn(cb, cs)

    alpha_mask_array = np.array(gradient_mask)
    alpha_mask_array = (255 - alpha_mask_array) * .6
    alpha_mask = Image.fromarray(np.uint8(alpha_mask_array.round()))
    cr = Image.composite(cb, cs, alpha_mask)

    cr = sepia(cr, .3)

    return cr.convert(im.mode)
