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

"""Common type definitions for pilgram."""

from collections.abc import Callable, Sequence

from PIL import Image
from PIL.ImageMath import _Operand

# Color types
RGBColor = tuple[int, int, int]
RGBAColor = tuple[int, int, int, float]

# Image size
Size = tuple[int, int]

# Blending function type
BlendingFunction = Callable[[Image.Image, Image.Image], Image.Image]

# ImageMath operand types
RGBOperands = tuple[_Operand, _Operand, _Operand]  # RGB color as ImageMath operands

# LUT types
LUT256 = Sequence[int]  # Look-up table with exactly 256 elements
