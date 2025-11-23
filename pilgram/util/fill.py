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

from pilgram.types import RGBAColor, RGBColor, Size


def fill(size: Size, color: RGBColor | RGBAColor) -> Image.Image:
    """Fills new image with the color.

    Arguments:
        size: A tuple of 2 integers. The size of output image.
        color: A tuple of 3 or 4 integers. The fill color.

    Returns:
        The output image.

    Raises:
        AssertionError: if `size` and/or `color` have invalid size.
    """

    assert len(size) == 2
    assert len(color) in [3, 4]

    if len(color) == 4:
        r, g, b, a = color
        alpha_int = int(round(a * 255))
        color = (r, g, b, alpha_int)

    uniqued = list(set(color))
    cmap = {c: Image.new("L", size, c) for c in uniqued}

    if len(color) == 3:
        r, g, b = color
        return Image.merge("RGB", (cmap[r], cmap[g], cmap[b]))
    else:
        r, g, b, a = color
        return Image.merge("RGBA", (cmap[r], cmap[g], cmap[b], cmap[a]))
