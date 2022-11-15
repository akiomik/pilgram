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


def test_exclusion():
    cb = util.fill((2, 2), [0, 128, 255])
    cs_array = np.array(
        [
            [[0] * 3, [127] * 3],
            [[128] * 3, [255] * 3],
        ],
        dtype=np.uint8,
    )
    cs = Image.fromarray(cs_array)
    exclusion = css.blending.exclusion(cb, cs)

    expected = [
        (0, 128, 255),
        (127, 128, 128),
        (128, 127, 127),
        (255, 127, 0),
    ]
    expected = [pytest.approx(c, abs=1) for c in expected]

    assert list(exclusion.getdata()) == expected  # almost eq


def test_exclusion_alpha_support(mocker):
    assert_alpha_support(css.blending.exclusion)
