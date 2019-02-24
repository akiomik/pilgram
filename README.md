# pilgram

A python library for instagram filters.

![screenshot](screenshot.png)

Filter implementations are inspired by [CSSgram](https://una.im/CSSgram/).

## Requirements

- Python 3
- [Pillow](https://pillow.readthedocs.io/en/stable/) or [pillow-simd](https://github.com/uploadcare/pillow-simd)

## Usage

Available instagram filters on `pilgram`: `_1977`, `aden`, `brannan`, `brooklyn`, `clarendon`, `earlybird`, `gingham`, `hudson`, `inkwell`, `kelvin`, `lark`, `lofi`, `maven`, `mayfair`, `moon`, `nashville`, `perpetua`, `reyes`, `rise`, `slumber`, `stinson`, `toaster`, `valencia`, `walden`, `willow`, `xpro2`

```python
from PIL import Image
import pilgram

im = Image.open('sample.jpg')
pilgram.aden(im).save('sample-aden.jpg')
```

Similarly, pilgram provides css filters as as by-product.
Available css filters on `pilgram.css`: `contrast`, `grayscale`, `hue_rotate`, `saturate`, `sepia`

```python
from PIL import Image
import pilgram.css

im = Image.open('sample.jpg')
pilgram.css.sepia(im).save('sample-sepia.jpg')
```

## Test

```sh
pipenv install --dev
pipenv run pytest
pipenv run flake8 pilgram  # lint
```
