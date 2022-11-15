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
from PIL import ImageChops

from pilgram import util


def test_apply_lut_identity():
    im = util.fill((2, 2), [0, 127, 255])
    lut_identity = [i for i in range(256)]
    assert util.apply_lut(im, lut_identity) == im


def test_apply_lut_invert():
    im = util.fill((2, 2), [0, 127, 255])
    lut_invert = [255 - i for i in range(256)]
    assert util.apply_lut(im, lut_invert) == ImageChops.invert(im)


def test_apply_lut_value_error():
    im = util.fill((2, 2), [0, 127, 255])
    lut = [255 - i for i in range(255)]
    with pytest.raises(ValueError):
        util.apply_lut(im, lut)
