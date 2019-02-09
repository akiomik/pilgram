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


def _rgb_to_rgbaw(rgb_array, a=255, w=255):
    rgbaw_array = np.pad(rgb_array,
                         [[0, 0], [0, 0], [0, 2]],
                         'constant', constant_values=[a, w])
    return rgbaw_array


def contrast(im, amount=1):
    assert amount >= 0

    # matrix from a w3c document:
    # https://www.w3.org/TR/filter-effects-1/#contrastEquivalent
    matrix = np.array([
        [amount, 0,      0,      0, -0.5 * amount + 0.5],
        [0,      amount, 0,      0, -0.5 * amount + 0.5],
        [0,      0,      amount, 0, -0.5 * amount + 0.5],
        [0,      0,      0,      1, 0],
        [0,      0,      0,      0, 1],
    ]).T

    im_array = np.array(im.convert('RGB'))
    im_array = _rgb_to_rgbaw(im_array)
    im_array = np.matmul(im_array, matrix).round()
    im_array = im_array[:, :, :3]  # to RGB
    im_array = np.clip(im_array, 0, 255)

    return Image.fromarray(np.uint8(im_array)).convert(im.mode)
