# pilgram

A python library for instagram filters.

Filter implementations are inspired by [CSSgram](https://una.im/CSSgram/).

## Requirements

- Python 3
- [Pillow](https://pillow.readthedocs.io/en/stable/)

## Usage

Available filters: `_1977`, `aden`, `brannan`, `brooklyn`, `clarendon`, `earlybird`, `gingham`, `hudson`, `inkwell`, `kelvin`, `lark`, `lofi`, `maven`, `mayfair`, `moon`, `nashville`, `perpetua`, `reyes`, `rise`, `slumber`, `stinson`, `toaster`, `valencia`, `walden`, `willow`, `xpro2`.

```python
from PIL import Image
import pilgram

im = Image.open('sample.jpg')
aden(im).save('sample-aden.jpg')
```

## Test

```sh
pipenv install --dev
pytest
```
