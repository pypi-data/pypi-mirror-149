# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['profile_python']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pytest-cov>=3.0.0,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0']

entry_points = \
{'console_scripts': ['profile-python = '
                     "profile-python=profile_python.__main__:main'"]}

setup_kwargs = {
    'name': 'profile-python',
    'version': '0.3.0',
    'description': 'Profile python is a script for you to view your data and github repositories.',
    'long_description': '# Profile Python\n\n[![CI](https://github.com/joaolfp/profile-python/actions/workflows/CI.yml/badge.svg)](https://github.com/joaolfp/profile-python/actions/workflows/CI.yml)\n[![codecov](https://codecov.io/gh/heroesofcode/profile-python/branch/master/graph/badge.svg?token=TDUTA1UY6N)](https://codecov.io/gh/heroesofcode/profile-python)\n[![Flake8](https://img.shields.io/badge/codestyle-flake8-yellow)](https://flake8.pycqa.org/en/latest/)\n[![GitHub release (latest by date)](https://img.shields.io/github/v/release/joaolfp/profile-python)](https://github.com/joaolfp/profile-python/releases)\n[![PyPI](https://img.shields.io/pypi/v/profile-python)](https://pypi.org/project/profile-python/)\n[![GitHub](https://img.shields.io/github/license/joaolfp/profile-python)](https://github.com/joaolfp/profile-python/blob/master/LICENSE)\n\n## Overview\nProfile python is a script for you to view your data and github repositories.\n\n## Installing\nInstall with pip or your favorite PyPi package manager:\n```\npython3 -m pip install profile-python\n```\n## What to use?\n```\npython3 -m profile_python\n```\n<img src="https://github.com/heroesofcode/profile-python/blob/master/assets/example.png" width="700px" height="800px">\n\n## Author\nCoded by [João Lucas](https://github.com/joaolfp)\n\n## License\n\n```\nMIT License\n\nCopyright (c) 2021 João Lucas\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n```\n',
    'author': 'João Lucas',
    'author_email': 'joaolucasfp2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/heroesofcode/profile-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
