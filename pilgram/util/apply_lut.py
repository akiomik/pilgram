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

from pilgram.types import LUT256


def apply_lut(im: Image.Image, lut: LUT256) -> Image.Image:
    """Apply LUT to an image.

    Arguments:
        im: An image.
        lut: A LUT (LookUp Table). The size must be 256.

    Returns:
        The output image.

    Raises:
        ValueError: if `lut` has invalid size.
    """

    if len(lut) != 256:
        raise ValueError(f"A size of LUT must be 256: {len(lut)}")

    return im.point(list(lut) * len(im.getbands()))
