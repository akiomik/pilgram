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
from PIL import Image

from pilgram import css, util
from pilgram.css.blending.alpha import split_alpha
from pilgram.css.blending.tests.helpers import assert_alpha_support


def test_normal():
    cb = util.fill((2, 2), [255, 128, 0])
    cs = util.fill((2, 2), [0, 128, 255])

    actual = css.blending.normal(cb, cs)
    expected = cs
    assert actual == expected


def test_normal2():
    cb = util.fill((2, 2), [255, 128, 0, 1.0])
    cs_array = np.array(
        [
            [[0, 128, 255, 0.25], [0, 255, 128, 0.5]],
            [[128, 255, 0, 0.75], [128, 0, 255, 0.1]],
        ],
        dtype=np.uint8,
    )
    cs = Image.fromarray(cs_array)

    actual = css.blending.normal(cb, cs)
    expected, _ = split_alpha(Image.alpha_composite(cb, cs))
    assert actual == expected


def test_overlay_alpha_support(mocker):
    assert_alpha_support(css.blending.normal)
