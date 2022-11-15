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

import pytest

from pilgram import css, util


def test_brightness():
    im = util.fill((4, 4), [174, 56, 3])
    im_b = css.brightness(im)

    assert list(im_b.getdata()) == list(im.getdata())
    assert im_b.size == im.size
    assert im_b.mode == im.mode


def test_brightness_1():
    im = util.fill((4, 4), [174, 56, 3])
    im_b = css.brightness(im, 1)
    im_b2 = css.brightness(im)

    assert list(im_b.getdata()) == list(im_b2.getdata())
    assert im_b.size == im.size
    assert im_b.mode == im.mode


def test_brightness_greater_than_1():
    im = util.fill((4, 4), [174, 56, 3])
    im_b = css.brightness(im, 2)
    im_b2 = css.brightness(im, 1)

    assert list(im_b.getdata()) != list(im_b2.getdata())
    assert im_b.size == im.size
    assert im_b.mode == im.mode


def test_brightness_0():
    im = util.fill((4, 4), [174, 56, 3])
    black = util.fill((4, 4), [0] * 3)
    im_b = css.brightness(im, 0)

    assert list(im_b.getdata()) == list(black.getdata())
    assert im_b.size == im.size
    assert im_b.mode == im.mode


def test_brightness_less_than_0():
    with pytest.raises(AssertionError):
        im = util.fill((4, 4), [174, 56, 3])
        css.brightness(im, -1)


def test_brightness_hsv():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = im.convert("HSV")
    im_b = css.brightness(im)
    im_b2 = css.brightness(im2)
    im_b2_rgb = im_b2.convert("RGB")

    assert list(im_b.getdata()) == list(im_b2_rgb.getdata())
    assert im_b2.size == im2.size
    assert im_b2.mode == im2.mode
