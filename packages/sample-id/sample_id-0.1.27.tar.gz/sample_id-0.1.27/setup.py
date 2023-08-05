# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_id',
 'sample_id.ann',
 'sample_id.deprecated',
 'sample_id.fingerprint',
 'sample_id.fingerprint.sift']

package_data = \
{'': ['*']}

install_requires = \
['annoy>=1.17.0,<2.0.0',
 'click>=7.1,<8.0',
 'joblib>=1.0.1,<2.0.0',
 'librosa>=0.8.0,<0.9.0',
 'matplotlib>=3.3.4,<4.0.0',
 'mutagen>=1.45.1,<2.0.0',
 'numba>=0.52.0,<0.53.0',
 'numpy>=1.16.0,<2.0.0',
 'pigz-python>=1.0.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'sklearn>=0.0,<0.1',
 'tabulate>=0.8.9,<0.9.0',
 'typing>=3.7,<4.0']

extras_require = \
{'docs': ['Sphinx>=3.5.4,<4.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'sphinxcontrib-apidoc>=0.3.0,<0.4.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
          'recommonmark>=0.7.1,<0.8.0',
          'toml>=0.10.2,<0.11.0',
          'sphinx-click>=2.7.1,<3.0.0'],
 'vlfeat': ['Cython>=0.29.22,<0.30.0', 'cyvlfeat>=0.7.0,<0.8.0']}

entry_points = \
{'console_scripts': ['sample_id = sample_id.cli:cli']}

setup_kwargs = {
    'name': 'sample-id',
    'version': '0.1.27',
    'description': 'Acoustic fingerprinting for Sample Identification',
    'long_description': '# Sample ID\n\n[![Build Status](https://app.travis-ci.com/Curly-Mo/sample-id.svg?branch=master)](https://app.travis-ci.com/Curly-Mo/sample-id)\n[![Coverage](https://coveralls.io/repos/github/Curly-Mo/sample-id/badge.svg)](https://coveralls.io/github/Curly-Mo/sample-id)\n[![Documentation](https://readthedocs.org/projects/sample-id/badge/?version=latest)](https://sample-id.readthedocs.org/en/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/sample-id.svg)](https://pypi.python.org/pypi/sample-id)\n[![PyPI Pythons](https://img.shields.io/pypi/pyversions/sample-id.svg)](https://pypi.python.org/pypi/sample-id)\n[![License](https://img.shields.io/pypi/l/sample-id.svg)](https://github.com/Curly-Mo/sample-id/blob/master/LICENSE)\n\nAcoustic fingerprinting for Sample Identification\n\n## Features\n\n* What it do?\n\n## Usage\n\n* TODO\n\n## Install\n\n```console\npip install sample-id\n```\n\n## Documentation\nSee https://sample-id.readthedocs.org/en/latest/\n\n## Development\n```console\npip install poetry\ncd sample-id\npoetry install\n```\n### Run\nTo run cli entrypoint:\n```console\npoetry run sample_id --help\n```\n\n### Tests\n```console\npoetry run tox\n```\n\n### Docker\nTo run with docker\n```console\ndocker build -t sample_id .\ndocker run sample_id:latest sample_id --help\n```\n',
    'author': 'Colin Fahy',
    'author_email': 'colin@cfahy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Curly-Mo/sample-id',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
