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


def test_min3() -> None:
    im = util.fill((1, 1), (0, 128, 255))
    r, g, b = im.split()
    im_min = ImageMath.lambda_eval(
        lambda args: _convert(_min3((args["r"], args["g"], args["b"])), "L"),
        r=r,
        g=g,
        b=b,
    )

    assert list(im_min.getdata()) == [0]


def test_max3() -> None:
    im = util.fill((1, 1), (0, 128, 255))
    r, g, b = im.split()
    im_max = ImageMath.lambda_eval(
        lambda args: _convert(_max3((args["r"], args["g"], args["b"])), "L"),
        r=r,
        g=g,
        b=b,
    )

    assert list(im_max.getdata()) == [255]


def test_clip_color() -> None:
    im = util.fill((1, 1), (0, 128, 255))
    r, g, b = im.split()
    bands = ImageMath.lambda_eval(
        lambda args: _clip_color((args["r"] - 64, args["g"], args["b"] + 64)),
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


def test_lum() -> None:
    im = util.fill((1, 1), (0, 128, 255))
    r, g, b = im.split()
    im_f = ImageMath.lambda_eval(
        lambda args: lum((args["r"], args["g"], args["b"])), r=r, g=g, b=b
    )
    im_l = im_f.convert("L")

    assert list(im_f.getdata()) == [pytest.approx(103.57, 1e-6)]
    assert list(im_l.getdata()) == [floor(103.57)]


def test_lum_im() -> None:
    im = util.fill((1, 1), (0, 128, 255))
    im_lum = lum_im(im)

    assert list(im_lum.getdata()) == [round(103.57)]


def test_set_lum() -> None:
    im1 = util.fill((1, 1), (0, 128, 255))
    im2 = util.fill((1, 1), (128, 128, 128))
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.lambda_eval(
        lambda args: set_lum(
            (args["r1"], args["g1"], args["b1"]),
            lum((args["r2"], args["g2"], args["b2"])),
        ),
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        g2=g2,
        b2=b2,
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


def test_sat() -> None:
    im = util.fill((1, 1), (80, 128, 200))
    r, g, b = im.split()
    im_sat = ImageMath.lambda_eval(
        lambda args: _convert(sat((args["r"], args["g"], args["b"])), "L"),
        r=r,
        g=g,
        b=b,
    )

    assert list(im_sat.getdata()) == [120]


def test_set_sat_cmax_gt_cmin() -> None:
    im1 = util.fill((1, 1), (0, 128, 255))
    im2 = util.fill((1, 1), (64, 96, 128))  # sat = 64
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.lambda_eval(
        lambda args: set_sat(
            (args["r1"], args["g1"], args["b1"]),
            sat((args["r2"], args["g2"], args["b2"])),
        ),
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


def test_set_sat_cmax_eq_cmid_gt_cmin() -> None:
    im1 = util.fill((1, 1), (0, 128, 128))
    im2 = util.fill((1, 1), (64, 96, 128))  # sat = 64
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.lambda_eval(
        lambda args: set_sat(
            (args["r1"], args["g1"], args["b1"]),
            sat((args["r2"], args["g2"], args["b2"])),
        ),
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        g2=g2,
        b2=b2,
    )

    expected = [[0], [64], [64]]
    assert [list(band.im.getdata()) for band in bands] == expected


def test_set_sat_cmax_eq_cmin() -> None:
    im1 = util.fill((1, 1), (128, 128, 128))
    im2 = util.fill((1, 1), (64, 96, 128))  # sat = 64
    r1, g1, b1 = im1.split()
    r2, g2, b2 = im2.split()
    bands = ImageMath.lambda_eval(
        lambda args: set_sat(
            (args["r1"], args["g1"], args["b1"]),
            sat((args["r2"], args["g2"], args["b2"])),
        ),
        r1=r1,
        g1=g1,
        b1=b1,
        r2=r2,
        g2=g2,
        b2=b2,
    )

    expected = [[0], [0], [0]]
    assert [list(band.im.getdata()) for band in bands] == expected
