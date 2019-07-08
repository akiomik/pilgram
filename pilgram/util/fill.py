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

from PIL import Image


def fill(size, color):
    """Fills new image with the color.

    Arguments:
        size: A tuple/list of 2 integers. The size of output image.
        color: A tuple/list of 3 or 4 integers. The fill color.

    Returns:
        The output image.

    Raises:
        AssertionError: if `size` and/or `color` have invalid size.
    """

    assert len(size) == 2
    assert len(color) in [3, 4]

    if len(color) == 4:
        color[3] = int(round(color[3] * 255))  # alpha

    uniqued = list(set(color))
    cmap = {c: Image.new('L', size, c) for c in uniqued}

    if len(color) == 3:
        r, g, b = color
        return Image.merge('RGB', (cmap[r], cmap[g], cmap[b]))
    else:
        r, g, b, a = color
        return Image.merge('RGBA', (cmap[r], cmap[g], cmap[b], cmap[a]))
