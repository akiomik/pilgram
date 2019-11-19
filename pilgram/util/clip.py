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


def clip(a, a_min=0, a_max=255):
    """Clips value

    Arguments:
        a: An integer/float. The input value to clip.
        a_min: An optional integer/float. The minimum value. Defaults to 0.
        a_max: An optional integer/float. The maximum value. Defaults to 255.

    Returns:
        The clipped value.
    """

    return min(max(a, a_min), a_max)
