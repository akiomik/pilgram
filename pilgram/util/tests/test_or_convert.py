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

from pilgram import util


def test_or_convert_same_mode():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255])  # RGB
    converted = util.or_convert(im, "RGB")

    assert converted == im  # should be the same instance
    assert converted.mode == "RGB"


def test_or_convert_different_mode():
    w, h = (4, 4)
    im = util.fill((w, h), [0, 127, 255, 0.5])  # RGBA
    converted = util.or_convert(im, "RGB")

    assert converted != im
    assert converted.mode == "RGB"
