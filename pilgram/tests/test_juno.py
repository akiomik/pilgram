# Copyright 2023 Michael G.
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

from PIL import Image

from pilgram import juno, util


def test_juno():
    im = util.fill((32, 32), [255] * 3)
    juno(im)


def test_juno_benchmark(benchmark):
    with Image.open("examples/mtjimba.jpg") as im:
        benchmark(juno, im)
