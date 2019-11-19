# coding:utf-8

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

from PIL import ImageChops

from pilgram.util import invert


def split_alpha(im):
    """Splits alpha channel

    Arguments:
        im: An image (RGB or RGBA).

    Returns:
        A tuple of the RGB and alpha image.
    """

    if im.mode == 'RGBA':
        # NOTE: `merge` is slower than `convert` when using Vanilla Pillow
        a = im.split()[3]
        im = im.convert('RGB')
        return im, a
    elif im.mode == 'RGB':
        return im, None
    else:
        raise ValueError('Unsupported mode: ' + im.mode)


def alpha_to_rgb(im):
    """Converts alpha image to rgb image.

    Arguments:
        im: An image (L only).

    Returns:
        A tuple of the RGB and alpha image.
    """
    if im.mode == 'L':
        # NOTE: `merge` is slower than `convert` when using Vanilla Pillow
        im = im.convert('RGB')
        return im
    else:
        raise ValueError('Unsupported mode: ' + im.mode)


def alpha_blend(im1, im2, blending):
    """Simple alpha blending

    The formula is defined as:

        simple alpha compositing:
        co = cs + cb x (1 - αs)

        written as non-premultiplied:
        αo x Co = αs x Cs + (1 - αs) x αb x Cb

        now substitute the result of blending for Cs:
        αo x Co = αs x ((1 - αb) x Cs + αb x B(Cb, Cs)) + (1 - αs) x αb x Cb
                = αs x (1 - αb) x Cs + αs x αb x B(Cb, Cs) + (1 - αs) x αb x Cb

    See the W3C document:
    https://www.w3.org/TR/compositing-1/#blending

    Arguments:
        im1: A backdrop image (RGB or RGBA).
        im2: A source image (RGB or RGBA).
        blending: The blending method.

    Returns:
        The output image.
    """

    im1, a1 = split_alpha(im1)
    if a1 is not None:
        a1_rgb = alpha_to_rgb(a1)
        a1_invert_rgb = alpha_to_rgb(invert(a1))

    im2, a2 = split_alpha(im2)
    if a2 is not None:
        a2_rgb = alpha_to_rgb(a2)
        a2_invert_rgb = alpha_to_rgb(invert(a2))

    im_blended = blending(im1, im2)

    if a1 is not None and a2 is not None:
        im_blended_alpha = ImageChops.multiply(a1_rgb, a2_rgb)
        im1_alpha = ImageChops.multiply(a1_rgb, a2_invert_rgb)
        im2_alpha = ImageChops.multiply(a2_rgb, a1_invert_rgb)
        im_blended = ImageChops.add(
            ImageChops.multiply(im_blended_alpha, im_blended),
            ImageChops.add(
                ImageChops.multiply(im1_alpha, im1),
                ImageChops.multiply(im2_alpha, im2)))
    elif a1 is not None:
        im_blended = ImageChops.add(
            ImageChops.multiply(a1_rgb, im_blended),
            ImageChops.multiply(a1_invert_rgb, im2))
    elif a2 is not None:
        im_blended = ImageChops.add(
            ImageChops.multiply(a2_rgb, im_blended),
            ImageChops.multiply(a2_invert_rgb, im1))

    return im_blended
