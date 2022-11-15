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
from PIL import Image

from pilgram import util
from pilgram.css.blending.alpha import alpha_blend, alpha_to_rgb, split_alpha


def _normal(cb, cs):
    """The normal blend mode"""
    return cs


def test_split_alpha_rgba():
    im = util.fill((2, 2), [0, 128, 255, 0.5])
    rgb, a = split_alpha(im)
    assert rgb == util.fill((2, 2), [0, 128, 255])
    assert a == Image.new("L", (2, 2), 128)


def test_split_alpha_rgb():
    im = util.fill((2, 2), [0, 128, 255])
    rgb, a = split_alpha(im)
    assert id(rgb) == id(im)
    assert a is None


def test_split_alpha_unsupported_mode():
    im = Image.new("L", (2, 2), 128)
    with pytest.raises(ValueError):
        split_alpha(im)


def test_alpha_to_rgb():
    im = Image.new("L", (2, 2), 128)
    im_rgb = alpha_to_rgb(im)
    assert im_rgb.mode == "RGB"

    r, g, b = im_rgb.split()
    assert r == im
    assert g == im
    assert b == im


def test_alpha_to_rgb_unsupported_mode():
    im = util.fill((2, 2), [0, 128, 255])
    with pytest.raises(ValueError):
        alpha_to_rgb(im)


def test_alpha_blend_call_blending(mocker):
    cb = util.fill((2, 2), [0, 128, 255, 1])
    cs = util.fill((2, 2), [255, 128, 0, 1])

    return_value, _ = split_alpha(cs)
    normal_stub = mocker.Mock(return_value=return_value)
    alpha_blend(cb, cs, normal_stub)

    # TODO: assert with parameters
    normal_stub.assert_called_once()


def test_alpha_blend_normal_rgb_with_rgb():
    cb = util.fill((2, 2), [0, 128, 255])
    cs = util.fill((2, 2), [255, 128, 0])
    cr = alpha_blend(cb, cs, _normal)
    assert cr == _normal(cb, cs)


def test_alpha_blend_normal_rgb_with_transparent_source():
    cb = util.fill((2, 2), [0, 128, 255])
    cs = util.fill((2, 2), [255, 128, 0, 0])
    cr = alpha_blend(cb, cs, _normal)
    assert cr == cb


def test_alpha_blend_normal_rgb_with_opaque_source():
    cb = util.fill((2, 2), [0, 128, 255])
    cs = util.fill((2, 2), [255, 128, 0, 1])
    cr = alpha_blend(cb, cs, _normal)

    expected = split_alpha(cs)[0]
    assert cr == expected


def test_alpha_blend_normal_transparent_backdrop_with_rgb():
    cb = util.fill((2, 2), [0, 128, 255, 0])
    cs = util.fill((2, 2), [255, 128, 0])
    cr = alpha_blend(cb, cs, _normal)
    assert cr == cs


def test_alpha_blend_normal_opaque_backdrop_with_rgb():
    cb = util.fill((2, 2), [0, 128, 255, 1])
    cs = util.fill((2, 2), [255, 128, 0])
    cr = alpha_blend(cb, cs, _normal)
    assert cr == cs


def test_alpha_blend_normal_transparent_backdrop_with_transparent_source():
    cb = util.fill((2, 2), [0, 128, 255, 0])
    cs = util.fill((2, 2), [255, 128, 0, 0])
    cr = alpha_blend(cb, cs, _normal)

    expected = util.fill((2, 2), [0, 0, 0])
    assert cr == expected


def test_alpha_blend_normal_transparent_backdrop_with_opaque_source():
    cb = util.fill((2, 2), [0, 128, 255, 0])
    cs = util.fill((2, 2), [255, 128, 0, 1])
    cr = alpha_blend(cb, cs, _normal)

    expected = split_alpha(cs)[0]
    assert cr == expected


def test_alpha_blend_normal_opaque_backdrop_with_transparent_source():
    cb = util.fill((2, 2), [0, 128, 255, 1])
    cs = util.fill((2, 2), [255, 128, 0, 0])
    cr = alpha_blend(cb, cs, _normal)

    expected = split_alpha(cb)[0]
    assert cr == expected


def test_alpha_blend_normal_opaque_backdrop_with_opaque_source():
    cb = util.fill((2, 2), [0, 128, 255, 1])
    cs = util.fill((2, 2), [255, 128, 0, 1])
    cr = alpha_blend(cb, cs, _normal)

    expected = split_alpha(cs)[0]
    assert cr == expected
