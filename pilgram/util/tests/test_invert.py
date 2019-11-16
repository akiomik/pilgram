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

from pilgram.util import fill, invert


def test_invert():
    w, h = (4, 4)
    actual = invert(fill((w, h), [0, 127, 255]))
    expected = fill((w, h), [255, 128, 0])
    assert actual == expected


def test_invert2():
    w, h = (4, 4)
    actual = invert(fill((w, h), [0, 127, 255]))
    expected = ImageChops.invert(fill((w, h), [0, 127, 255]))
    assert actual == expected
