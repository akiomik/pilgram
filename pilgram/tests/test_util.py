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


def test_fill():
    im = util.fill((4, 4), [0, 127, 255])

    expected = [(0, 127, 255)] * (4 * 4)
    actual = list(im.getdata())

    assert actual == expected


def test_linear_gradient_mask_horizontal():
    mask = util.linear_gradient_mask((4, 4))

    expected = [255, 170, 85, 0] * 4
    actual = list(mask.getdata())

    assert actual == expected


def test_linear_gradient_mask_vertical():
    mask = util.linear_gradient_mask((4, 4), is_horizontal=False)

    expected = [255] * 4 + [170] * 4 + [85] * 4 + [0] * 4
    actual = list(mask.getdata())

    assert actual == expected


def test_linear_gradient_mask_start_end():
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask((4, 4), start=start, end=end)

    expected = [100, 133, 167, 200] * 4
    actual = list(mask.getdata())

    assert actual == expected


def test_linear_gradient():
    black = [0] * 3
    white = [255] * 3
    gradient = util.linear_gradient((4, 4), black, white)

    actual = list(gradient.getdata())
    expected = [
        (0, 0, 0),
        (85, 85, 85),
        (170, 170, 170),
        (255, 255, 255),
    ] * 4

    assert actual == expected


def test_radial_gradient_mask():
    pass  # TODO


def test_radial_gradient():
    pass  # TODO


def test_scale_color():
    im = util.fill((4, 4), [0, 127, 255])

    expected = [(0, 64, 128)] * (4 * 4)
    actual = list(util.scale_color(im, .5).getdata())

    assert actual == expected
