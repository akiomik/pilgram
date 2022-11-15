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

from math import floor

import pytest
from PIL import Image, ImageMath
from PIL.ImageMath import imagemath_convert as _convert

from pilgram import util
from pilgram.css.blending.nonseparable import (
    _clip_color,
    _max3,
    _min3,
    lum,
    lum_im,
    sat,
    set_lum,
    set_sat,
)


def test_min3():
    im = util.fill((1, 1), [0, 128, 255])
    r, g, b = im.split()
    im_min = ImageMath.eval('convert(min3((r, g, b)), "L")', min3=_min3, r=r, g=g, b=b)

    assert list(im_min.getdata()) == [0]


def test_max3():
    im = util.fill((1, 1), [0, 128, 255])
    r, g, b = im.split()
    im_max = ImageMath.eval('convert(max3((r, g, b)), "L")', max3=_max3, r=r, g=g, b=b)

    assert list(im_max.getdata()) == [255]


def test_clip_color():
    im = util.fill((1, 1), [0, 128, 255])
    r, g, b = im.split()
    bands = ImageMath.eval(
        "clip_color((float(r - 64), float(g), float(b + 64)))",
        clip_color=_clip_color,
        r=r,
        g=g,
        b=b,
    )

    expected = [
        [pytest.approx(25.70517158047366, 1e-6)],
        [pytest.approx(106.8796587856024, 1e-6)],
        [pytest.approx(187.63136220320442, 1e-6)],
    ]
    assert [list(band.im.getdata()) for band in bands] == expected


def test_lum():
    im = util.fill((1, 1), [0, 128, 255])
    r, g, b = im.split()
    im_f = ImageMath.eval("lum((float(r), float(g), float(b)))", lum=lum, r=r, g=g, b=b)
    im_l = im_f.convert("L")

    assert list(im_f.getdata()) == [pytest.approx(103.57, 1e-6)]
    assert list(im_l.getdata()) == [floor(103.57)]


def test_lum_im():
    im = util.fill((1, 1), [0, 128, 255])
    im_lum = lum_im(im)

    assert list(im_lum.getdata()) == [round(103.57)]


def test_set_lum():
    im1 = util.fill((1, 1), [0, 128, 255])
    im2 = util.fill((1, 1), [128, 128, 128])
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    c1 = "(float(r1), float(g1), float(b1))"
    c2 = "(float(r2), float(g2), float(b2))"
    bands = ImageMath.eval(
        "set_lum({}, lum({}))".format(c1, c2),
        set_lum=set_lum,
        lum=lum,
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        b2=b2,
        g2=g2,
    )

    expected1 = [
        [pytest.approx(41.13881001122631, 1e-6)],
        [pytest.approx(148.48874067225782, 1e-6)],
        [255],
    ]
    assert [list(band.im.getdata()) for band in bands] == expected1

    im_set_lum = Image.merge("RGB", [_convert(band, "L").im for band in bands])
    expected2 = [(floor(41.13881001122631), floor(148.48874067225782), 255)]
    assert list(im_set_lum.getdata()) == expected2


def test_sat():
    im = util.fill((1, 1), [80, 128, 200])
    r, g, b = im.split()
    im_sat = ImageMath.eval('convert(sat((r, g, b)), "L")', sat=sat, r=r, g=g, b=b)

    assert list(im_sat.getdata()) == [120]


def test_set_sat_cmax_gt_cmin():
    im1 = util.fill((1, 1), [0, 128, 255])
    im2 = util.fill((1, 1), [64, 96, 128])  # sat = 64
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.eval(
        "set_sat((r1, g1, b1), sat((r2, g2, b2)))",
        set_sat=set_sat,
        sat=sat,
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        g2=g2,
        b2=b2,
    )

    expected = [
        [0],
        [pytest.approx(32.12549019607843, abs=1)],
        [64],
    ]
    assert [list(band.im.getdata()) for band in bands] == expected


def test_set_sat_cmax_eq_cmid_gt_cmin():
    im1 = util.fill((1, 1), [0, 128, 128])
    im2 = util.fill((1, 1), [64, 96, 128])  # sat = 64
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.eval(
        "set_sat((r1, g1, b1), sat((r2, g2, b2)))",
        set_sat=set_sat,
        sat=sat,
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        g2=g2,
        b2=b2,
    )

    expected = [[0], [64], [64]]
    assert [list(band.im.getdata()) for band in bands] == expected


def test_set_sat_cmax_eq_cmin():
    im1 = util.fill((1, 1), [128, 128, 128])
    im2 = util.fill((1, 1), [64, 96, 128])  # sat = 64
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.eval(
        "set_sat((r1, g1, b1), sat((r2, g2, b2)))",
        set_sat=set_sat,
        sat=sat,
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        g2=g2,
        b2=b2,
    )

    expected = [[0], [0], [0]]
    assert [list(band.im.getdata()) for band in bands] == expected
