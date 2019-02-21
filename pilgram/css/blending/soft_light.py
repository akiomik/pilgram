import math

from PIL import Image, ImageMath
from PIL.ImageMath import imagemath_int as _int
from PIL.ImageMath import imagemath_float as _float


def _soft_light(cb, cs, d_cb):
    """Returns ImageMath operands for soft light"""

    cb = [_float(c) / 255 for c in cb]
    cs = [_float(c) / 255 for c in cs]
    d_cb = [_float(c) / 255 for c in d_cb]

    rb, gb, bb = cb
    rs, gs, bs = cs
    d_rd, d_gd, d_bd = d_cb

    r1 = _int(rs <= .5) * (rb - (1 - 2 * rs) * rb * (1 - rb))
    r2 = _int(rs > .5) * (rb + (2 * rs - 1) * d_rd)
    g1 = _int(gs <= .5) * (gb - (1 - 2 * gs) * gb * (1 - gb))
    g2 = _int(gs > .5) * (gb + (2 * gs - 1) * d_gd)
    b1 = _int(bs <= .5) * (bb - (1 - 2 * bs) * bb * (1 - bb))
    b2 = _int(bs > .5) * (bb + (2 * bs - 1) * d_bd)

    return (r1 + r2, g1 + g2, b1 + b2)


def _d_cb(cb):
    """Returns D(Cb) - Cb"""

    cb /= 255

    if cb <= .25:
        d_cb = ((16 * cb - 12) * cb + 4) * cb - cb
    else:
        d_cb = math.sqrt(cb) - cb

    return round(d_cb * 255)


def soft_light(im1, im2):
    """Darkens or lightens the colors, depending on the source color value.

    The soft light formula is defined as:

        if(Cs <= 0.5)
            B(Cb, Cs) = Cb - (1 - 2 x Cs) x Cb x (1 - Cb)
        else
            B(Cb, Cs) = Cb + (2 x Cs - 1) x (D(Cb) - Cb)

    where

        if(Cb <= 0.25)
            D(Cb) = ((16 * Cb - 12) x Cb + 4) x Cb
        else
            D(Cb) = sqrt(Cb)

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blendingsoftlight

    Arguments:
        im1: A backdrop image.
        im2: A source image.

    Returns:
        The output image.
    """

    r1, g1, b1 = im1.split()  # cb
    r2, g2, b2 = im2.split()  # cs
    d_rd, d_gd, d_bd = im1.point(_d_cb).split()  # d(cb) - cb

    c = ImageMath.eval(
            'f((r1, g1, b1), (r2, g2, b2), (d_rd, d_gd, d_bd))',
            f=_soft_light, r1=r1, g1=g1, b1=b1, r2=r2, g2=g2, b2=b2,
            d_rd=d_rd, d_gd=d_gd, d_bd=d_bd)
    rgb = [ImageMath.imagemath_convert(c_ * 255, 'L').im for c_ in c]

    return Image.merge('RGB', rgb)
