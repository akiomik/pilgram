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

from __future__ import division

from pilgram import util


def test_radial_gradient_mask_prepared():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h))

    expected_data = [
        52,
        93,
        111,
        94,
        53,
        93,
        150,
        182,
        151,
        94,
        111,
        182,
        231,
        183,
        113,
        94,
        151,
        183,
        152,
        95,
        53,
        94,
        113,
        95,
        54,
    ]

    # TODO: test rectangle
    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient_mask_length():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), length=0.5)

    expected_data = [
        0,
        107,
        149,
        107,
        0,
        107,
        255,
        255,
        255,
        107,
        149,
        255,
        255,
        255,
        149,
        107,
        255,
        255,
        255,
        107,
        0,
        107,
        149,
        107,
        0,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient_mask_prepared_scale():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), scale=1.5)

    expected_data = [
        118,
        147,
        158,
        148,
        119,
        147,
        187,
        207,
        188,
        148,
        158,
        207,
        239,
        209,
        160,
        148,
        188,
        209,
        189,
        149,
        119,
        148,
        160,
        149,
        120,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient_mask_position():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), center=(0, 0))

    expected_data = [
        255,
        210,
        165,
        120,
        75,
        210,
        191,
        154,
        112,
        69,
        165,
        154,
        128,
        92,
        53,
        120,
        112,
        92,
        64,
        30,
        75,
        69,
        53,
        30,
        0,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient_mask_length_eq_scale():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), length=0.5, scale=0.5)

    expected_data = [
        0,
        0,
        0,
        0,
        0,
        0,
        255,
        255,
        255,
        0,
        0,
        255,
        255,
        255,
        0,
        0,
        255,
        255,
        255,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient_mask_length_ge_1():
    w, h = (4, 4)
    mask = util.radial_gradient_mask((w, h), length=1)

    assert list(mask.getdata()) == [255] * (w * h)
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient_mask_scale_le_0():
    w, h = (4, 4)
    mask = util.radial_gradient_mask((w, h), scale=0)

    assert list(mask.getdata()) == [0] * (w * h)
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_radial_gradient():
    pass  # TODO


def test_radial_gradient_255_to_0():
    # this case is the same as radial_gradient_mask
    w, h = (5, 5)
    gradient = util.radial_gradient((w, h), [[255, 255, 255], [0, 0, 0]])

    expected = util.radial_gradient_mask((w, h))
    assert list(gradient.getdata(0)) == list(expected.getdata())
    assert list(gradient.getdata(1)) == list(expected.getdata())
    assert list(gradient.getdata(2)) == list(expected.getdata())
    assert gradient.size == (w, h)
    assert gradient.mode == "RGB"
