# pilgram

[![PyPI](https://img.shields.io/pypi/v/pilgram.svg)](https://python.org/pypi/pilgram)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pilgram.svg)](https://python.org/pypi/pilgram)
[![Python CI](https://github.com/akiomik/pilgram/workflows/Python%20CI/badge.svg)](https://github.com/akiomik/pilgram/actions?query=workflow%3A%22Python+CI%22)
[![codecov](https://codecov.io/gh/akiomik/pilgram/branch/master/graph/badge.svg)](https://codecov.io/gh/akiomik/pilgram)

A python library for instagram filters.

![screenshot](screenshots/screenshot.png)

The filter implementations are inspired by [CSSgram](https://una.im/CSSgram/).

## Requirements

- Python >= 3.4
- [Pillow](https://pillow.readthedocs.io/en/stable/) or [pillow-simd](https://github.com/uploadcare/pillow-simd)

## Install

```sh
pip install pillow>=4.1.0 # or pip install pillow-simd
pip install pilgram
```

## Usage

Available instagram filters on `pilgram`:
- `_1977`
- `aden`
- `brannan`
- `brooklyn`
- `clarendon`
- `earlybird`
- `gingham`
- `hudson`
- `inkwell`
- `kelvin`
- `lark`
- `lofi`
- `maven`
- `mayfair`
- `moon`
- `nashville`
- `perpetua`
- `reyes`
- `rise`
- `slumber`
- `stinson`
- `toaster`
- `valencia`
- `walden`
- `willow`
- `xpro2`

```python
from PIL import Image
import pilgram

im = Image.open('sample.jpg')
pilgram.aden(im).save('sample-aden.jpg')
```

Similarly, pilgram provides css filters and blend modes as a by-product.

Available css filters on `pilgram.css`:
- `contrast`
- `grayscale`
- `hue_rotate`
- `saturate`
- `sepia`

```python
from PIL import Image
import pilgram.css

im = Image.open('sample.jpg')
pilgram.css.sepia(im).save('sample-sepia.jpg')
```

Available blend modes on `pilgram.css.blending`:
- `color`
- `color_burn`
- `color_dodge`
- `darken`
- `difference`
- `exclusion`
- `hard_light`
- `hue`
- `lighten`
- `multiply`
- `normal`
- `overlay`
- `screen`
- `soft_light`

```python
from PIL import Image
import pilgram.css.blending

backdrop = Image.open('backdrop.jpg')
source = Image.open('source.jpg')
pilgram.css.blending.color(backdrop, source).save('blending.jpg')
```

## Demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/akiomik/pilgram/blob/master/notebooks/example.ipynb)

- [notebooks/example.ipynb](notebooks/example.ipynb)

## Filter performance comparison with [instagram-filters](https://github.com/acoomans/instagram-filters)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/akiomik/pilgram/blob/master/notebooks/filter-performance-comparison.ipynb)

- [notebooks/filter-performance-comparison.ipynb](notebooks/filter-performance-comparison.ipynb)

![filter performance comparison](screenshots/filter-performance-comparison.png)

## Test

```sh
pipenv install --dev
make test     # pytest
make test-tox # pytest with tox
```
