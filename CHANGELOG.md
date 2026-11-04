# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-11-23

### Added

- Support for Python 3.11, 3.12, 3.13 and 3.14.
- Type hints for the public API, with a `py.typed` marker (PEP 561).

### Changed

- Pillow is now declared as a dependency (`Pillow>=10.3.0`) and is installed automatically.

### Removed

- Support for Python 3.9 and earlier.
- Support for Pillow < 10.3.0 and pillow-simd. Use pilgram 1.2.1 if you need them.

## [1.2.1] - 2022-02-15

### Added

- Support for Python 3.10.

## [1.2.0] - 2020-11-26

### Added

- Support for Python 3.8 and 3.9.

### Changed

- Improved performance of alpha blending.

### Removed

- Support for Python 2.7.

### Fixed

- `DeprecationWarning: an integer is required (got type float)` emitted by the `soft_light` blend mode and the filters that use it ([#16]).

## [1.1.0] - 2019-11-19

### Added

- Blend modes `darken`, `difference`, `lighten`, `multiply`, `normal` and `screen`.
- Alpha channel support for blend modes.

### Changed

- Improved performance of the `hard_light` and `soft_light` blend modes.

### Fixed

- `lark` filter missing its contrast adjustment.

## [1.0.3] - 2019-07-14

### Fixed

- `hue` blend mode producing wrong colors when two channels share the maximum value.
- `color_burn` blend mode producing wrong colors when the backdrop is white.
- Radial gradients with three or more color stops, which affected the `earlybird` filter.

## [1.0.2] - 2019-07-04

### Added

- Support for Python 2.7.

## [1.0.1] - 2019-03-22

### Added

- Support for Python 3.4 ([#1]).

## [1.0.0] - 2019-02-25

### Added

- Instagram filters: `_1977`, `aden`, `brannan`, `brooklyn`, `clarendon`, `earlybird`, `gingham`, `hudson`, `inkwell`, `kelvin`, `lark`, `lofi`, `maven`, `mayfair`, `moon`, `nashville`, `perpetua`, `reyes`, `rise`, `slumber`, `stinson`, `toaster`, `valencia`, `walden`, `willow` and `xpro2`.
- CSS filters on `pilgram.css`: `brightness`, `contrast`, `grayscale`, `hue_rotate`, `saturate` and `sepia`.
- Blend modes on `pilgram.css.blending`: `color`, `color_burn`, `color_dodge`, `exclusion`, `hard_light`, `hue`, `overlay` and `soft_light`.

[Unreleased]: https://github.com/akiomik/pilgram/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/akiomik/pilgram/compare/v1.2.1...v2.0.0
[1.2.1]: https://github.com/akiomik/pilgram/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/akiomik/pilgram/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/akiomik/pilgram/compare/v1.0.3...v1.1.0
[1.0.3]: https://github.com/akiomik/pilgram/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/akiomik/pilgram/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/akiomik/pilgram/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/akiomik/pilgram/releases/tag/v1.0.0
[#1]: https://github.com/akiomik/pilgram/issues/1
[#16]: https://github.com/akiomik/pilgram/issues/16
