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


def test_clip_minus_1():
    assert util.clip(-1) == 0


def test_clip_0():
    assert util.clip(0) == 0


def test_clip_255():
    assert util.clip(255) == 255


def test_clip_256():
    assert util.clip(256) == 255


def test_clip_min_minus_1000():
    assert util.clip(-1000, a_min=-1000) == -1000
    assert util.clip(-1001, a_min=-1000) == -1000


def test_clip_max_1000():
    assert util.clip(1000, a_max=1000) == 1000
    assert util.clip(1001, a_max=1000) == 1000
