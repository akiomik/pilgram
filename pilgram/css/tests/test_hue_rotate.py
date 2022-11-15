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

from pilgram import css, util


def test_hue_rotate():
    im = util.fill((4, 4), [174, 56, 3])
    hue_rotated_im = css.hue_rotate(im)

    assert list(hue_rotated_im.getdata()) == list(im.getdata())
    assert hue_rotated_im.size == im.size
    assert hue_rotated_im.mode == im.mode


def test_hue_rotate_0():
    im = util.fill((4, 4), [174, 56, 3])
    hue_rotated_im = css.hue_rotate(im)
    hue_rotated_im2 = css.hue_rotate(im, 0)

    assert list(hue_rotated_im.getdata()) == list(hue_rotated_im2.getdata())
    assert hue_rotated_im.size == im.size
    assert hue_rotated_im.mode == im.mode


def test_hue_rotate_360():
    im = util.fill((4, 4), [174, 56, 3])
    hue_rotated_im = css.hue_rotate(im)
    hue_rotated_im2 = css.hue_rotate(im, 360)

    assert list(hue_rotated_im.getdata()) == list(hue_rotated_im2.getdata())
    assert hue_rotated_im.size == im.size
    assert hue_rotated_im.mode == im.mode


def test_hue_rotate_greater_than_0():
    im = util.fill((4, 4), [174, 56, 3])
    hue_rotated_im = css.hue_rotate(im, 42)
    hue_rotated_im2 = css.hue_rotate(im)

    assert list(hue_rotated_im.getdata()) != list(hue_rotated_im2.getdata())
    assert hue_rotated_im.size == im.size
    assert hue_rotated_im.mode == im.mode


def test_hue_rotate_less_than_0():
    im = util.fill((4, 4), [174, 56, 3])
    hue_rotated_im = css.hue_rotate(im, -42)
    hue_rotated_im2 = css.hue_rotate(im)

    assert list(hue_rotated_im.getdata()) != list(hue_rotated_im2.getdata())
    assert hue_rotated_im.size == im.size
    assert hue_rotated_im.mode == im.mode


def test_hue_rotate_hsv():
    im = util.fill((4, 4), [174, 56, 3])
    im2 = im.convert("HSV")
    hue_rotated_im = css.hue_rotate(im)
    hue_rotated_im2 = css.hue_rotate(im2)
    hue_rotated_im2_rgb = hue_rotated_im2.convert("RGB")

    hue_rotated_im_data = list(hue_rotated_im.getdata())
    hue_rotated_im2_rgb_data = list(hue_rotated_im2_rgb.getdata())

    assert hue_rotated_im_data == hue_rotated_im2_rgb_data
    assert hue_rotated_im2.size == im2.size
    assert hue_rotated_im2.mode == im2.mode
