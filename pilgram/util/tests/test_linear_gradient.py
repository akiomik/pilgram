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


from pilgram import util


def test_linear_gradient_mask_prepared_horizontal() -> None:
    w, h = (4, 4)
    mask = util.linear_gradient_mask((w, h))

    assert list(mask.get_flattened_data()) == [222, 161, 94, 33] * h
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_linear_gradient_mask_prepared_vertical() -> None:
    w, h = (4, 4)
    mask = util.linear_gradient_mask((w, h), is_horizontal=False)

    assert (
        list(mask.get_flattened_data()) == [222] * w + [161] * w + [94] * w + [33] * w
    )
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_linear_gradient_mask_start_end() -> None:
    w, h = (4, 4)
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask((w, h), start=start, end=end)

    assert list(mask.get_flattened_data()) == [100, 133, 166, 200] * h
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_linear_gradient_mask_start_end_vertical() -> None:
    w, h = (4, 4)
    start = 100 / 255
    end = 200 / 255
    mask = util.linear_gradient_mask((w, h), start=start, end=end, is_horizontal=False)

    expected = [100] * w + [133] * w + [166] * w + [200] * w

    assert list(mask.get_flattened_data()) == expected
    assert mask.size == (w, h)
    assert mask.mode == "L"


def test_linear_gradient_prepared() -> None:
    w, h = (4, 4)
    white = (255,) * 3
    black = (0,) * 3
    gradient = util.linear_gradient((w, h), white, black)
    expected_data = [(c,) * 3 for c in [222, 161, 94, 33]] * h

    assert list(gradient.get_flattened_data()) == expected_data
    assert gradient.size == (w, h)
    assert gradient.mode == "RGB"
