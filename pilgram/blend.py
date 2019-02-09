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

import numpy as np
from PIL import Image, ImageChops


def overlay(im, im2):
    """
    B(Cb, Cs) = HardLight(Cs, Cb)

    See: https://www.w3.org/TR/compositing-1/#valdef-blend-mode-overlay
    """

    return hard_light(im2, im)


def color_dodge(im, im2):
    """
    if(Cb == 0)
        B(Cb, Cs) = 0
    else if(Cs == 1)
        B(Cb, Cs) = 1
    else
        B(Cb, Cs) = min(1, Cb / (1 - Cs))

    See: https://www.w3.org/TR/compositing-1/#blendingcolordodge
    """

    cb = np.array(im) / 255.
    cs = np.array(im2) / 255.

    _cs = np.where(cs == 1, 0, cs)  # avoid division by zero
    cr1 = np.minimum(1, cb / (1 - _cs))
    cr2 = cs

    cr = (cs < 1) * cr1 + (cs == 1) * cr2
    cr *= 255
    cr = np.clip(cr, 0, 255)

    return Image.fromarray(np.uint8(cr.round()))


def color_burn(im, im2):
    """
    if(Cb == 1)
        B(Cb, Cs) = 1
    else if(Cs == 0)
        B(Cb, Cs) = 0
    else
        B(Cb, Cs) = 1 - min(1, (1 - Cb) / Cs)

    See: https://www.w3.org/TR/compositing-1/#blendingcolorburn
    """

    cb = np.array(im) / 255.
    cs = np.array(im2) / 255.

    _cs = np.where(cs == 0, 1, cs)  # avoid division by zero
    cr1 = 1 - np.minimum(1, (1 - cb) / _cs)
    cr2 = cs

    cr = (cs > 0) * cr1 + (cs == 0) * cr2
    cr *= 255
    cr = np.clip(cr, 0, 255)

    return Image.fromarray(np.uint8(cr.round()))


def hard_light(im, im2):
    """
    if(Cs <= 0.5)
        B(Cb, Cs) = Multiply(Cb, 2 x Cs)
    else
        B(Cb, Cs) = Screen(Cb, 2 x Cs -1)

    See: https://www.w3.org/TR/compositing-1/#blendinghardlight
    """

    cs = np.array(im2)

    cs_multiply = np.clip(2. * cs, 0, 255)
    im2_multiply = Image.fromarray(np.uint8(cs_multiply.round()))
    multiply = np.array(ImageChops.multiply(im, im2_multiply))

    cs_screen = np.clip(2. * cs - 255., 0, 255)
    im2_screen = Image.fromarray(np.uint8(cs_screen.round()))
    screen = np.array(ImageChops.screen(im, im2_screen))

    cr = (cs < 127.5) * multiply + (cs >= 127.5) * screen

    return Image.fromarray(np.uint8(cr))


def soft_light(im, im2):
    """
    if(Cs <= 0.5)
        B(Cb, Cs) = Cb - (1 - 2 x Cs) x Cb x (1 - Cb)
    else
        B(Cb, Cs) = Cb + (2 x Cs - 1) x (D(Cb) - Cb)

    where

    if(Cb <= 0.25)
        D(Cb) = ((16 * Cb - 12) x Cb + 4) x Cb
    else
        D(Cb) = sqrt(Cb)

    See: https://www.w3.org/TR/compositing-1/#blendingsoftlight
    """
    def d(x):
        d1 = ((16 * x - 12) * x + 4) * x
        d2 = np.sqrt(x)
        return (x <= .25) * d1 + (x > .25) * d2

    cb = np.array(im) / 255.
    cs = np.array(im2) / 255.

    cr1 = cb - (1 - 2 * cs) * cb * (1 - cb)
    cr2 = cb + (2 * cs - 1) * (d(cb) - cb)

    cr = (cs <= .5) * cr1 + (cs > .5) * cr2
    cr *= 255
    cr = np.clip(cr, 0, 255)

    return Image.fromarray(np.uint8(cr.round()))


def exclusion(im, im2):
    """
    B(Cb, Cs) = Cb + Cs - 2 x Cb x Cs

    See: https://www.w3.org/TR/compositing-1/#blendingexclusion
    """

    cb = np.array(im) / 255.
    cs = np.array(im2) / 255.

    cr = cb + cs - 2 * cb * cs
    cr *= 255
    cr = np.clip(cr, 0, 255)

    return Image.fromarray(np.uint8(cr.round())).convert(im.mode)


def _lum(c):
    """
    Lum(C) = 0.3 x Cred + 0.59 x Cgreen + 0.11 x Cblue

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """
    return np.matmul(c, np.array([.298912, .586611, .114478]).T)[:, :, None]


def _clip_color(c):
    """
    ClipColor(C)
        L = Lum(C)
        n = min(Cred, Cgreen, Cblue)
        x = max(Cred, Cgreen, Cblue)
        if(n < 0)
            C = L + (((C - L) * L) / (L - n))

        if(x > 1)
            C = L + (((C - L) * (1 - L)) / (x - L))

        return C

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """

    L = _lum(c)
    n = c.min(axis=2, keepdims=True)
    n = np.where(n < 0, n, 2)  # avoid division by zero
    x = c.max(axis=2, keepdims=True)
    x = np.where(x > 1, x, -2)  # avoid division by zero

    c_ = L + (((c - L) * L) / (L - n))
    c_ = np.where(n < 0, c_, c)
    c_ = L + (((c_ - L) * (1 - L)) / (x - L))
    c_ = np.where(x > 1, c_, c)

    return c_


def _set_lum(c, l):
    """
    SetLum(C, l)
        d = l - Lum(C)
        Cred = Cred + d
        Cgreen = Cgreen + d
        Cblue = Cblue + d
        return ClipColor(C)

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """

    d = l - _lum(c)
    return _clip_color(c + d)


def _sat(c):
    """
    Sat(C) = max(Cred, Cgreen, Cblue) - min(Cred, Cgreen, Cblue)

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """

    return c.max(axis=2, keepdims=True) - c.min(axis=2, keepdims=True)


def _set_sat(c, s):
    """
    SetSat(C, s)
        if(Cmax > Cmin)
            Cmid = (((Cmid - Cmin) x s) / (Cmax - Cmin))
            Cmax = s
        else
            Cmid = Cmax = 0
        Cmin = 0
        return C;

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """

    cmin = c.min(axis=2, keepdims=True)
    cmax = c.max(axis=2, keepdims=True)
    cmid_idx = (c < cmax) & (c > cmin)
    cmid = np.maximum(cmid_idx * c, cmin).max(axis=2, keepdims=True)

    never_match = -1  # `c` does not have this value
    cmid1 = np.where(cmax > cmin, cmid, never_match)
    cmid2 = np.where(cmax <= cmin, cmid, never_match)
    cmax1 = np.where(cmax > cmin, cmax, never_match)
    cmax2 = np.where(cmax <= cmin, cmax, never_match)

    # avoid division by zero
    cmax_safe = np.where(cmax == cmin, never_match, cmax)

    c_ = np.where(c == cmid1, ((cmid - cmin) * s) / (cmax_safe - cmin), c)
    c_ = np.where(c == cmid2, 0, c_)
    c_ = np.where(c == cmax1, s, c_)
    c_ = np.where(c == cmax2, 0, c_)
    c_ = np.where(c == cmin, 0, c_)

    return c_


def hue(im, im2):
    """
    B(Cb, Cs) = SetLum(SetSat(Cs, Sat(Cb)), Lum(Cb))

    See: https://www.w3.org/TR/compositing-1/#blendinghue
    """

    cb = np.array(im) / 255.
    cs = np.array(im2) / 255.

    cr = _set_lum(_set_sat(cs, _sat(cb)), _lum(cb)) * 255
    cr = np.clip(cr, 0, 255)

    return Image.fromarray(np.uint8(cr.round())).convert(im.mode)


def color(im, im2):
    """
    B(Cb, Cs) = SetLum(Cs, Lum(Cb))

    See: https://www.w3.org/TR/compositing-1/#valdef-blend-mode-color
    """

    cb = np.array(im) / 255.
    cs = np.array(im2) / 255.

    cr = _set_lum(cs, _lum(cb)) * 255
    cr = np.clip(cr, 0, 255)

    return Image.fromarray(np.uint8(cr.round())).convert(im.mode)
