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


def test_saturate():
    im = util.fill((4, 4), [174, 56, 3])
    saturated_im = css.saturate(im)

    assert saturated_im.size == im.size
    assert saturated_im.mode == im.mode


def test_saturate_1():
    im = util.fill((4, 4), [174, 56, 3])
    saturated_im = css.saturate(im, 1)
    saturated_im2 = css.saturate(im)

    assert list(saturated_im.getdata()) == list(saturated_im2.getdata())
    assert saturated_im.size == im.size
    assert saturated_im.mode == im.mode


def test_saturate_greater_than_1():
    im = util.fill((4, 4), [174, 56, 3])
    saturated_im = css.saturate(im, 2)
    saturateed_im2 = css.saturate(im, 1)

    assert list(saturated_im.getdata()) != list(saturateed_im2.getdata())
    assert saturated_im.size == im.size
    assert saturated_im.mode == im.mode


def test_saturate_0():
    im = util.fill((4, 4), [174, 56, 3])
    saturated_im = css.saturate(im, 0)
    grayscaled_im = css.grayscale(im)

    assert list(saturated_im.getdata()) == list(grayscaled_im.getdata())
    assert saturated_im.size == im.size
    assert saturated_im.mode == im.mode


def test_saturate_less_than_0():
    with pytest.raises(AssertionError):
        im = util.fill((4, 4), [174, 56, 3])
        css.saturate(im, -1)


def test_saturate_hsv():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = im.convert("HSV")
    saturated_im = css.saturate(im)
    saturated_im2 = css.saturate(im2)
    saturated_im2_rgb = saturated_im2.convert("RGB")

    assert list(saturated_im.getdata()) == list(saturated_im2_rgb.getdata())
    assert saturated_im2.size == im2.size
    assert saturated_im2.mode == im2.mode
