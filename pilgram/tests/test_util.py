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

from pilgram import util


def test_or_convert_same_mode():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255])  # RGB
    converted = util.or_convert(im, 'RGB')

    assert converted == im  # should be the same instance
    assert converted.mode == 'RGB'


def test_or_convert_different_mode():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255, .5])  # RGBA
    converted = util.or_convert(im, 'RGB')

    assert converted != im
    assert converted.mode == 'RGB'


def test_fill():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255])

    assert list(im.getdata()) == [(0, 127, 255)] * (w * h)
    assert im.size == (w, h)
    assert im.mode == 'RGB'


def test_fill_alpha():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255, .5])

    assert list(im.getdata()) == [(0, 127, 255, 128)] * (w * h)
    assert im.size == (w, h)
    assert im.mode == 'RGBA'


def test_linear_gradient_mask_horizontal():
    w, h = (4, 4)
    mask = util.linear_gradient_mask((w, h))

    assert list(mask.getdata()) == [223, 159, 95, 31] * h
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_linear_gradient_mask_vertical():
    w, h = (4, 4)
    mask = util.linear_gradient_mask((w, h), is_horizontal=False)

    assert list(mask.getdata()) == [223] * w + [159] * w + [95] * w + [31] * w
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_linear_gradient_mask_start_end():
    w, h = (4, 4)
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask((w, h), start=start, end=end)

    assert list(mask.getdata()) == [100, 133, 167, 200] * h
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_linear_gradient_mask_start_end_vertical():
    w, h = (4, 4)
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask(
            (w, h), start=start, end=end, is_horizontal=False)

    expected = [100] * w + [133] * w + [167] * w + [200] * w

    assert list(mask.getdata()) == expected
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_linear_gradient():
    w, h = (4, 4)
    white = [255] * 3
    black = [0] * 3
    gradient = util.linear_gradient((w, h), white, black)
    expected_data = [(c,) * 3 for c in [223, 159, 95, 31]] * h

    assert list(gradient.getdata()) == expected_data
    assert gradient.size == (w, h)
    assert gradient.mode == 'RGB'


def test_radial_gradient_mask():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h))

    expected_data = [
        49,  92,  110, 93,  50,
        92,  151, 182, 152, 94,
        110, 182, 255, 183, 111,
        93,  152, 183, 153, 94,
        50,  94,  111, 94,  51,
    ]

    # TODO: test position
    # TODO: test rectangle
    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_radial_gradient_mask_length():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), length=.5)

    expected_data = [
        0,   107, 149, 107, 0,
        107, 255, 255, 255, 107,
        149, 255, 255, 255, 149,
        107, 255, 255, 255, 107,
        0,   107, 149, 107, 0,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_radial_gradient_mask_scale():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), scale=1.5)

    expected_data = [
        119, 148, 159, 148, 119,
        148, 187, 207, 187, 148,
        159, 207, 255, 207, 159,
        148, 187, 207, 187, 148,
        119, 148, 159, 148, 119,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_radial_gradient_mask_length_eq_scale():
    w, h = (5, 5)
    mask = util.radial_gradient_mask((w, h), length=.5, scale=.5)

    expected_data = [
        0, 0,   0,   0,   0,
        0, 255, 255, 255, 0,
        0, 255, 255, 255, 0,
        0, 255, 255, 255, 0,
        0, 0,   0,   0,   0,
    ]

    assert list(mask.getdata()) == expected_data
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_radial_gradient_mask_length_ge_1():
    w, h = (4, 4)
    mask = util.radial_gradient_mask((w, h), length=1)

    assert list(mask.getdata()) == [255] * (w * h)
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_radial_gradient_mask_scale_le_0():
    w, h = (4, 4)
    mask = util.radial_gradient_mask((w, h), scale=0)

    assert list(mask.getdata()) == [0] * (w * h)
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_radial_gradient():
    pass  # TODO
