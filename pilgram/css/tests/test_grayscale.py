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


def test_grayscale():
    im = util.fill((4, 4), [174, 56, 3])
    grayscaled_im = css.grayscale(im)

    assert grayscaled_im.size == im.size
    assert grayscaled_im.mode == im.mode


def test_grayscale_1():
    im = util.fill((4, 4), [174, 56, 3])
    grayscaled_im = css.grayscale(im, 1)
    grayscaled_im2 = css.grayscale(im)

    assert list(grayscaled_im.getdata()) == list(grayscaled_im2.getdata())
    assert grayscaled_im.size == im.size
    assert grayscaled_im.mode == im.mode


def test_grayscale_greater_than_1():
    im = util.fill((4, 4), [174, 56, 3])
    grayscaled_im = css.grayscale(im, 2)
    grayscaleed_im2 = css.grayscale(im, 1)

    assert list(grayscaled_im.getdata()) == list(grayscaleed_im2.getdata())
    assert grayscaled_im.size == im.size
    assert grayscaled_im.mode == im.mode


def test_grayscale_0():
    im = util.fill((4, 4), [174, 56, 3])
    grayscaled_im = css.grayscale(im, 0)

    assert list(grayscaled_im.getdata()) == list(im.getdata())
    assert grayscaled_im.size == im.size
    assert grayscaled_im.mode == im.mode


def test_grayscale_less_than_0():
    with pytest.raises(AssertionError):
        im = util.fill((4, 4), [174, 56, 3])
        css.grayscale(im, -1)


def test_grayscale_hsv():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = im.convert("HSV")
    grayscaled_im = css.grayscale(im)
    grayscaled_im2 = css.grayscale(im2)
    grayscaled_im2_rgb = grayscaled_im2.convert("RGB")

    assert list(grayscaled_im.getdata()) == list(grayscaled_im2_rgb.getdata())
    assert grayscaled_im2.size == im2.size
    assert grayscaled_im2.mode == im2.mode
