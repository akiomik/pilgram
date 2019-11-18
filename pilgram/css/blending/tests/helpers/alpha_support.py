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


def _assert_alpha_backdrop_support(blending):
    cb = util.fill((2, 2), [0, 128, 255, 0])
    cs = util.fill((2, 2), [255, 128, 0])
    cr = blending(cb, cs)
    assert cr == cs


def _assert_alpha_source_support(blending):
    cb = util.fill((2, 2), [0, 128, 255])
    cs = util.fill((2, 2), [255, 128, 0, 0])
    cr = blending(cb, cs)
    assert cr == cb


def assert_alpha_support(blending):
    _assert_alpha_backdrop_support(blending)
    _assert_alpha_source_support(blending)
