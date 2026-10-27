# Changelog

## 0.1.1

- Make fresh Hermes Git plugin installations load by including the directory manifest and entry point.
- Bundle the registry in Python wheels, including wheels built from source distributions, and resolve source/package paths correctly.
- Fix discovery metadata parsing, provider selection, numeric price ceilings, missing-key errors, and variable/unknown prices.
- Report malformed registries and provider failures clearly; clean up interrupted session suggestions.
- Correct installation instructions and add offline regression and installed-package checks across Python 3.9, 3.11, and 3.13 on Windows and Linux.

The source tag and GitHub artifacts contain these fixes. PyPI publication is pending an authorized publishing route; the existing PyPI 0.1.0 does not contain them.

## 0.1.0

- Initial published package.
