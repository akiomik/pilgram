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


def test_sepia():
    im = util.fill((4, 4), [174, 56, 3])
    sepiaed_im = css.sepia(im)

    assert sepiaed_im.size == im.size
    assert sepiaed_im.mode == im.mode


def test_sepia_1():
    im = util.fill((4, 4), [174, 56, 3])
    sepiaed_im = css.sepia(im, 1)
    sepiaed_im2 = css.sepia(im)

    assert list(sepiaed_im.getdata()) == list(sepiaed_im2.getdata())
    assert sepiaed_im.size == im.size
    assert sepiaed_im.mode == im.mode


def test_sepia_greater_than_1():
    im = util.fill((4, 4), [174, 56, 3])
    sepiaed_im = css.sepia(im, 2)
    sepiaed_im2 = css.sepia(im, 1)

    assert list(sepiaed_im.getdata()) == list(sepiaed_im2.getdata())
    assert sepiaed_im.size == im.size
    assert sepiaed_im.mode == im.mode


def test_sepia_0():
    im = util.fill((4, 4), [174, 56, 3])
    sepiaed_im = css.sepia(im, 0)

    assert list(sepiaed_im.getdata()) == list(im.getdata())
    assert sepiaed_im.size == im.size
    assert sepiaed_im.mode == im.mode


def test_sepia_less_than_0():
    with pytest.raises(AssertionError):
        im = util.fill((4, 4), [174, 56, 3])
        css.sepia(im, -1)


def test_sepia_hsv():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = im.convert("HSV")
    sepiaed_im = css.sepia(im)
    sepiaed_im2 = css.sepia(im2)
    sepiaed_im2_rgb = sepiaed_im2.convert("RGB")

    assert list(sepiaed_im.getdata()) == list(sepiaed_im2_rgb.getdata())
    assert sepiaed_im2.size == im2.size
    assert sepiaed_im2.mode == im2.mode
