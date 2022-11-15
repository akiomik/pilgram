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

import numpy as np
import pytest
from PIL import Image

from pilgram import css, util
from pilgram.css.blending.tests.helpers import assert_alpha_support


def test_hue1():
    cb_array = np.array(
        [
            [[0, 128, 255], [0, 255, 128]],
            [[128, 255, 0], [128, 0, 255]],
        ],
        dtype=np.uint8,
    )
    cb = Image.fromarray(cb_array)
    cs = util.fill((2, 2), [0, 128, 255])
    hue = css.blending.hue(cb, cs)

    expected = [(0, 128, 255), (102, 179, 255), (143, 199, 255), (0, 82, 163)]
    expected = [pytest.approx(c, abs=3) for c in expected]  # TODO

    assert list(hue.getdata()) == expected  # almost eq


def test_hue2():
    cb = util.fill((2, 2), [0, 128, 255])
    cs_array = np.array(
        [
            [[0, 128, 255], [0, 255, 128]],
            [[128, 255, 0], [128, 0, 255]],
        ],
        dtype=np.uint8,
    )
    cs = Image.fromarray(cs_array)
    hue = css.blending.hue(cb, cs)

    expected = [(0, 128, 255), (0, 160, 80), (70, 139, 0), (153, 50, 255)]
    expected = [pytest.approx(c, abs=1) for c in expected]

    assert list(hue.getdata()) == expected  # almost eq


def test_hue_alpha_support(mocker):
    assert_alpha_support(css.blending.hue)
