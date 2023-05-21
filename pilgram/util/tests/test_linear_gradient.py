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


def test_linear_gradient_mask_start_end():
    w, h = (4, 4)
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask((w, h), start=start, end=end)

    assert list(mask.getdata()) == [100, 133, 166, 200] * h
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_linear_gradient_mask_start_end_vertical():
    w, h = (4, 4)
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask((w, h), start=start, end=end, is_horizontal=False)

    expected = [100] * w + [133] * w + [166] * w + [200] * w

    assert list(mask.getdata()) == expected
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_linear_gradient():
    w, h = (4, 4)
    start = [255, 0, 0]  # red
    end = [0, 0, 255]  # blue
    gradient = util.linear_gradient((w, h), start, end)
    expected_data = [
        (255, 0, 0),
        (170, 0, 85),
        (85, 0, 170),
        (0, 0, 255),
        (255, 0, 0),
        (170, 0, 85),
        (85, 0, 170),
        (0, 0, 255),
        (255, 0, 0),
        (170, 0, 85),
        (85, 0, 170),
        (0, 0, 255),
        (255, 0, 0),
        (170, 0, 85),
        (85, 0, 170),
        (0, 0, 255),
    ]

    assert list(gradient.getdata()) == expected_data
    assert gradient.size == (w, h)
    assert gradient.mode == "RGB"


def test_linear_gradient_vertical():
    w, h = (4, 4)
    start = [255, 0, 0]  # red
    end = [0, 0, 255]  # blue
    gradient = util.linear_gradient((w, h), start, end, False)
    expected_data = [
        (255, 0, 0),
        (255, 0, 0),
        (255, 0, 0),
        (255, 0, 0),
        (170, 0, 85),
        (170, 0, 85),
        (170, 0, 85),
        (170, 0, 85),
        (85, 0, 170),
        (85, 0, 170),
        (85, 0, 170),
        (85, 0, 170),
        (0, 0, 255),
        (0, 0, 255),
        (0, 0, 255),
        (0, 0, 255),
    ]

    assert list(gradient.getdata()) == expected_data
    assert gradient.size == (w, h)
    assert gradient.mode == "RGB"
