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


def test_contrast():
    im = util.fill((4, 4), [174, 56, 3])
    contrasted_im = css.contrast(im)

    assert list(contrasted_im.getdata()) == list(im.getdata())
    assert contrasted_im.size == im.size
    assert contrasted_im.mode == im.mode


def test_contrast_1():
    im = util.fill((4, 4), [174, 56, 3])
    contrasted_im = css.contrast(im, 1)
    contrasted_im2 = css.contrast(im)

    assert list(contrasted_im.getdata()) == list(contrasted_im2.getdata())
    assert contrasted_im.size == im.size
    assert contrasted_im.mode == im.mode


def test_contrast_greater_than_1():
    im = util.fill((4, 4), [174, 56, 3])
    contrasted_im = css.contrast(im, 2)
    contrasted_im2 = css.contrast(im, 1)

    assert list(contrasted_im.getdata()) != list(contrasted_im2.getdata())
    assert contrasted_im.size == im.size
    assert contrasted_im.mode == im.mode


def test_contrast_0():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = util.fill((4, 4), [128] * 3)
    contrasted_im = css.contrast(im, 0)

    assert list(contrasted_im.getdata()) == list(im2.getdata())
    assert contrasted_im.size == im.size
    assert contrasted_im.mode == im.mode


def test_contrast_less_than_0():
    with pytest.raises(AssertionError):
        im = util.fill((4, 4), [174, 56, 3])
        css.contrast(im, -1)


def test_contrast_hsv():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = im.convert("HSV")
    contrasted_im = css.contrast(im)
    contrasted_im2 = css.contrast(im2)
    contrasted_im2_rgb = contrasted_im2.convert("RGB")

    assert list(contrasted_im.getdata()) == list(contrasted_im2_rgb.getdata())
    assert contrasted_im2.size == im2.size
    assert contrasted_im2.mode == im2.mode
