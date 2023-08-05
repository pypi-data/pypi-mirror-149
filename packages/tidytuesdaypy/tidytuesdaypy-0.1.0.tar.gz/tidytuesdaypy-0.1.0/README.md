# TidyTuesdayPy

A Python library to download TidyTuesday data, inspired by the [{tidytuesdayR}](https://github.com/thebioengineer/tidytuesdayR) package for R.

:warning: _This package is currently under development_

## Get Started

### Installing

The easiest way to install `tidytuesdaypy` is via `pip`:

```console
pip install tidytuesdaypy
```

## Deep Dive

### Contributing

1. Clone this repository `git clone git@github.com:alwinw/tidytuesdaypy.git`
2. Install the development version `pip install -v -e .[<extras>]` (`-e` needs pip >= 22.0 for pyproject.toml) or `poetry install --extras "<extras>"`
3. Make your changes and commit using [commitizen](https://commitizen-tools.github.io/commitizen/#installation) and ensure [pre-commit](https://pre-commit.com/#install) is active
4. When ready, bump the version and run `poetry build -v`. If deploying, run `poetry publish --build -v`

## Acknowledgements

This package is heavily inspired by [{tidytuesdayR}](https://github.com/thebioengineer/tidytuesdayR). It would not be possible without [R4DS](https://github.com/rfordatascience) and of course [tidytuesday](https://github.com/rfordatascience/tidytuesday)
