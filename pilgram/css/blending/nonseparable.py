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

from PIL.ImageMath import imagemath_min as _min
from PIL.ImageMath import imagemath_max as _max


def _min3(c):
    """Returns minimum value of 3 elements as ImageMath operands."""
    r, g, b = c
    return _min(_min(r, g), b)


def _max3(c):
    """Returns maximum value of 3 elements as ImageMath operands."""
    r, g, b = c
    return _max(_max(r, g), b)


def _clip_color(c):
    """Returns clipped color as ImageMath operands.

    The formula is defined as:

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

    Arguments:
        c: A tuple/list of 3 ImageMath operands. The color.

    Returns:
        A tuple/list of 3 ImageMath operands. The clipped color.
    """

    r, g, b = c

    L = lum(c)
    n = _min3(c)
    x = _max3(c)

    def fn(c):
        # C = L + ((C - L) * L) / (L - n)
        #   = (L * (L - n)) / (L - n) + ((C - L) * L) / (L - n)
        #   = ((L * (L - n)) + ((C - L) * L)) / (L - n)
        #   = (L^2 - nL + CL - L^2) / (L - n)
        #   = (CL - nL) / (L - n)
        #   = (L * (C - n)) / (L - n)
        return (n < 0) * ((L * (c - n)) / (L - n)) \
                + (n >= 0) * c

    def fx(c):
        return (x > 255) * (L + ((c - L) * (255 - L)) / (x - L)) \
                + (x <= 255) * c

    r = fx(fn(r))
    g = fx(fn(g))
    b = fx(fn(b))

    return (r, g, b)


def lum(c):
    """Returns luminosity as ImageMath operands.

    The formula is defined as:

        Lum(C) = 0.3 x Cred + 0.59 x Cgreen + 0.11 x Cblue

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable

    Arguments:
        c: A tuple/list of 3 ImageMath operands. The color.

    Returns:
        A tuple/list of 3 ImageMath operands. The luminosity.
    """

    r, g, b = c
    return r * .3 + g * .59 + b * .11


def lum_im(im):
    """Returns luminosity as image.

    The formula is defined as:

        Lum(C) = 0.3 x Cred + 0.59 x Cgreen + 0.11 x Cblue

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable

    Arguments:
        im: An input image.

    Returns:
        The luminosity image.
    """
    return im.convert('L')


def set_lum(c, l1):
    """Set luminosity to the color.

    The formula is defined as:

        SetLum(C, l)
            d = l - Lum(C)
            Cred = Cred + d
            Cgreen = Cgreen + d
            Cblue = Cblue + d
            return ClipColor(C)

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable

    Arguments:
        c: A tuple/list of 3 ImageMath operands. The color.
        l1: An ImageMath operands. The luminosity to set.

    Returns:
        A tuple/list of 3 ImageMath oerands.
    """

    r, g, b = c

    d = l1 - lum(c)
    r += d
    g += d
    b += d

    return _clip_color((r, g, b))


def set_lum_im(c, l1, l2):
    """Set luminosity to the color from image.

    The formula is defined as:

        SetLum(C, l)
            d = l - Lum(C)
            Cred = Cred + d
            Cgreen = Cgreen + d
            Cblue = Cblue + d
            return ClipColor(C)

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable

    Arguments:
        c: A tuple/list of 3 ImageMath operands. The color.
        l1: An ImageMath operands. The image of l.
        l2: An ImageMath operands. The image of Lum(C).

    Returns:
        A tuple/list of 3 ImageMath operands.
    """

    r, g, b = c
    d = l1 - l2

    return _clip_color((r + d, g + d, b + d))


def sat(c):
    """Returns saturation as ImageMath operands.

    The formula is defined as:

        Sat(C) = max(Cred, Cgreen, Cblue) - min(Cred, Cgreen, Cblue)

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable

    Arguments:
        c: A tuple/list of 3 operands. The color.

    Returns:
        A tuple/list of 3 operands. The saturation.
    """

    return _max3(c) - _min3(c)


def set_sat(c, s):
    """Set saturation to the color.

    The formula is defined as:

        SetSat(C, s)
            if(Cmax > Cmin)
                Cmid = (((Cmid - Cmin) x s) / (Cmax - Cmin))
                Cmax = s
            else
                Cmid = Cmax = 0
            Cmin = 0
            return C;

    See: https://www.w3.org/TR/compositing-1/#blendingnonseparable

    Arguments:
        c: A tuple/list of 3 ImageMath operands. The color.
        s: An ImageMath operand. The saturation to set.

    Returns:
        A tuple/list of 3 ImageMath operands.
    """

    r, g, b = c

    cmax = _max3(c)
    cmin = _min3(c)
    cmid = r + g + b - cmax - cmin
    new_cmid = ((cmid - cmin) * s) / (cmax - cmin)

    # NOTE: use cmax if cmax == cmid
    cmid_r = (cmax > cmin) * (cmax > cmid) * (cmid == r) * new_cmid
    cmid_g = (cmax > cmin) * (cmax > cmid) * (cmid == g) * new_cmid
    cmid_b = (cmax > cmin) * (cmax > cmid) * (cmid == b) * new_cmid

    cmax_r = (cmax > cmin) * (cmax == r) * s
    cmax_g = (cmax > cmin) * (cmax == g) * s
    cmax_b = (cmax > cmin) * (cmax == b) * s

    return (
        cmid_r + cmax_r,
        cmid_g + cmax_g,
        cmid_b + cmax_b,
    )
