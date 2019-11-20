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

import numpy as np
from PIL import Image


def add(im1, im2):
    """Adds two images.

    Arguments:
        im1: An image.
        im2: An image.

    Returns:
        The output image.
    """

    # NOTE: When using Vanilla Pillow, `ImageChops.add` is slower than numpy
    im1 = np.asarray(im1, dtype=np.int16)  # avoid overflow
    im2 = np.asarray(im2)
    im = im1 + im2
    im = im.clip(0, 255).astype(np.uint8)

    return Image.fromarray(im)
