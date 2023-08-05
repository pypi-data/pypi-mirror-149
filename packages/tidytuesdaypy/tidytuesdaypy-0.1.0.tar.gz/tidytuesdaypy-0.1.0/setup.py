# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tidytuesdaypy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tidytuesdaypy',
    'version': '0.1.0',
    'description': 'Extract weekly TidyTuesday Data/Readme',
    'long_description': '# TidyTuesdayPy\n\nA Python library to download TidyTuesday data, inspired by the [{tidytuesdayR}](https://github.com/thebioengineer/tidytuesdayR) package for R.\n\n:warning: _This package is currently under development_\n\n## Get Started\n\n### Installing\n\nThe easiest way to install `tidytuesdaypy` is via `pip`:\n\n```console\npip install tidytuesdaypy\n```\n\n## Deep Dive\n\n### Contributing\n\n1. Clone this repository `git clone git@github.com:alwinw/tidytuesdaypy.git`\n2. Install the development version `pip install -v -e .[<extras>]` (`-e` needs pip >= 22.0 for pyproject.toml) or `poetry install --extras "<extras>"`\n3. Make your changes and commit using [commitizen](https://commitizen-tools.github.io/commitizen/#installation) and ensure [pre-commit](https://pre-commit.com/#install) is active\n4. When ready, bump the version and run `poetry build -v`. If deploying, run `poetry publish --build -v`\n\n## Acknowledgements\n\nThis package is heavily inspired by [{tidytuesdayR}](https://github.com/thebioengineer/tidytuesdayR). It would not be possible without [R4DS](https://github.com/rfordatascience) and of course [tidytuesday](https://github.com/rfordatascience/tidytuesday)\n',
    'author': 'alwinw',
    'author_email': '16846521+alwinw@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alwinw/tidytuesdaypy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
