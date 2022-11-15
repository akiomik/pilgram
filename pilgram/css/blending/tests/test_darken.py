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

from PIL import ImageChops

from pilgram import css, util
from pilgram.css.blending.tests.helpers import assert_alpha_support


def test_darken():
    cb = util.fill((2, 2), [255, 128, 0])
    cs = util.fill((2, 2), [0, 128, 255])

    actual = css.blending.darken(cb, cs)
    expected = ImageChops.darker(cb, cs)
    assert actual == expected


def test_overlay_alpha_support(mocker):
    assert_alpha_support(css.blending.darken)
