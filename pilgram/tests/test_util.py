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
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255])

    assert list(im.getdata()) == [(0, 127, 255)] * (w * h)
    assert im.size == (w, h)
    assert im.mode == 'RGB'


def test_linear_gradient_mask_horizontal():
    w, h = (4, 4)
    mask = util.linear_gradient_mask((w, h))

    assert list(mask.getdata()) == [255, 170, 85, 0] * h
    assert mask.size == (w, h)
    assert mask.mode == 'L'


def test_linear_gradient_mask_vertical():
    w, h = (4, 4)
    mask = util.linear_gradient_mask((w, h), is_horizontal=False)

    assert list(mask.getdata()) == [255] * w + [170] * w + [85] * w + [0] * w
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


def test_linear_gradient():
    w, h = (4, 4)
    black = [0] * 3
    white = [255] * 3
    gradient = util.linear_gradient((w, h), black, white)
    expected_data = [(c,) * 3 for c in [0, 85, 170, 255]] * h

    assert list(gradient.getdata()) == expected_data
    assert gradient.size == (w, h)
    assert gradient.mode == 'RGB'


def test_radial_gradient_mask():
    pass  # TODO


def test_radial_gradient():
    pass  # TODO


def test_scale_color():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255])
    scaled_im = util.scale_color(im, .5)

    assert list(scaled_im.getdata()) == [(0, 64, 128)] * (w * h)
    assert scaled_im.mode == im.mode
    assert scaled_im.size == im.size
