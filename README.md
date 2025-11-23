# pilgram

[![DOI](https://zenodo.org/badge/169348812.svg)](https://zenodo.org/badge/latestdoi/169348812)
[![PyPI](https://img.shields.io/pypi/v/pilgram.svg)](https://python.org/pypi/pilgram)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pilgram.svg)](https://python.org/pypi/pilgram)
[![Python CI](https://github.com/akiomik/pilgram/actions/workflows/ci.yml/badge.svg)](https://github.com/akiomik/pilgram/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/akiomik/pilgram/branch/master/graph/badge.svg)](https://codecov.io/gh/akiomik/pilgram)

A python library for instagram filters.

![screenshot](screenshots/screenshot.png)

The filter implementations are inspired by [CSSgram](https://una.github.io/CSSgram/).

## Requirements

- Python >= 3.10
- [Pillow](https://pillow.readthedocs.io/en/stable/) or [pillow-simd](https://github.com/uploadcare/pillow-simd)
- [NumPy](https://numpy.org)

## Pillow Compatibility Notes

**Important**: This library requires specific Pillow versions for optimal compatibility:

- **Pillow >= 10.3.0**: Use latest pilgram version for full feature support including `ImageMath.lambda_eval`
- **Pillow < 10.3.0**: Use `pilgram==1.2.1` which supports older Pillow versions with `ImageMath.eval`
- **pillow-simd**: Use `pilgram==1.2.1` (pillow-simd lacks `ImageMath.lambda_eval` support)

### Version Selection Guide

```sh
# For Pillow >= 10.3.0
pip install pillow>=10.3.0
pip install pilgram  # Latest version

# For Pillow < 10.3.0 or pillow-simd
pip install pillow<10.3.0  # or pillow-simd
pip install pilgram==1.2.1
```

## Install

### Recommended (Latest Pillow)

```sh
pip install pillow>=10.3.0
pip install numpy
pip install pilgram  # Latest version with ImageMath.lambda_eval support
```

### For Older Pillow Versions

```sh
pip install pillow<10.3.0  # or pillow-simd
pip install numpy
pip install pilgram==1.2.1  # Last version supporting ImageMath.eval
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

## Development

### Setup development environment

```sh
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/akiomik/pilgram.git
cd pilgram

# Install dependencies (including dev dependencies)
uv sync --all-extras

# Install Pillow or pillow-simd (choose one)
uv add pillow>=9.3.0  # or uv add pillow-simd
```

### Run commands

```sh
make check       # Run all checks (lint + format-check + type-check + test)
make test        # Run tests only
make lint        # Run ruff linting
make format      # Format code with ruff
make test-benchmark  # Run performance benchmarks
```
