# c2m2-frictionless-dataclass

This repository houses two primary python package, `frictionless-dataclass` which can be used to generate python code from a frictionless datapackage specification, and `c2m2-frictionless` which contains c2m2 specific helpers along with the latest c2m2 release generated as code.

For more information about each, see the subdirectory READMEs. It's possible to install them directly or via the main package.

- [frictionless-dataclass](./frictionless-dataclass/)
- [c2m2-frictionless](./c2m2-frictionless/)

## Installation

Installing the root directory will permit installing `c2m2-frictionless` or `frictionless-dataclass` as `extras` for convenience.

```bash
# Install c2m2 frictionless
pip3 install 'c2m2-frictionless-dataclass[c2m2-frictionless] @ git+https://github.com/nih-cfde/c2m2-frictionless-dataclass'

# Install frictionless dataclass
pip3 install 'c2m2-frictionless-dataclass[frictionless-dataclass] @ git+https://github.com/nih-cfde/c2m2-frictionless-dataclass'

# Install both
pip3 install 'c2m2-frictionless-dataclass[full] @ git+https://github.com/nih-cfde/c2m2-frictionless-dataclass'
```

## Updating this package

The `Makefile` can be used to update the `c2m2-frictionless` package using the `frictionless-dataclass` package.

`make update` will download the most up to date c2m2 frictionless datapackage json schema and regenerate the relevant dataclass in that package.
