# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flatqube']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=8.1.2,<9.0.0',
 'humanize>=4.0.0,<5.0.0',
 'omegaconf>=2.2.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0']

entry_points = \
{'console_scripts': ['flatqube = flatqube.cli:cli']}

setup_kwargs = {
    'name': 'flatqube-client',
    'version': '0.2.4',
    'description': 'FlatQube API client library and CLI tools',
    'long_description': '# flatqube-client\n\n[![PyPI version](https://img.shields.io/pypi/v/flatqube-client.svg)](https://pypi.python.org/pypi/flatqube-client)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/flatqube-client.svg)\n[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nflatqube-client is an API client library and CLI tools for [FlatQube](https://app.flatqube.io) DEX service in [Everscale](https://everscale.network) blockchain network.\n\n## Installing\n\n```\npip3 install -U flatqube-client\n```\n\n## Usage\n\nMain CLI help:\n\n```\nflatqube --help\n```\n\n### Show Currency Info\n\nShow selected currencies:\n\n```\nflatqube currency show wever qube bridge\n```\n\nShow the default (`whitelist`) list of currencies:\n\n```\nflatqube currency show\n```\n\nAlso, we can show some list, "everscale" for example:\n\n```\nflatqube currency show -l everscale\n```\n\nOr we can show meme tokens sorted by price change:\n\n```\nflatqube currency show -l meme -s price-ch\n```\n\nWe can show currencies by names and currencies from multiple lists jointly:\n\n```\nflatqube currency show weth wbtc -l everscale -l stable\n```\n\nAlso, we can run cli in "auto-update" mode with interval 3 seconds (by default update interval is 5 seconds):\n\n```\nflatqube currency show -s price-ch -u -i3\n```\n\nSee help for more info about `currency show` command:\n\n```\nflatqube currency show --help\n```\n\n## License\n\n[MIT](https://opensource.org/licenses/MIT)\n',
    'author': 'Evgeny Prilepin',
    'author_email': 'esp.home@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
