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


def subtract(im1: Image.Image, im2: Image.Image) -> Image.Image:
    """Subtracts two images.

    Arguments:
        im1: An image.
        im2: An image.

    Returns:
        The output image.
    """

    # NOTE: When using Vanilla Pillow,
    #       `ImageChops.subtract` is slower than numpy
    im1_array = np.asarray(im1, dtype=np.int16)  # avoid underflow
    im2_array = np.asarray(im2)
    im_array = im1_array - im2_array
    im_array = im_array.clip(0, 255).astype(np.uint8)

    return Image.fromarray(im_array)
