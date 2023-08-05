# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcapi']

package_data = \
{'': ['*'], 'gcapi': ['schemas/*']}

install_requires = \
['Click>=6.0', 'httpx>=0.22.0,<0.23.0', 'jsonschema[format_nongpl]>=3.0']

entry_points = \
{'console_scripts': ['gcapi = gcapi.cli:main']}

setup_kwargs = {
    'name': 'gcapi',
    'version': '0.7.0',
    'description': 'Python client for the grand-challenge.org REST API',
    'long_description': '# Grand Challenge API Client\n\n[![CI](https://github.com/DIAGNijmegen/rse-gcapi/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DIAGNijmegen/rse-gcapi/actions/workflows/ci.yml?query=branch%3Amain)\n[![PyPI](https://img.shields.io/pypi/v/gcapi)](https://pypi.org/project/gcapi/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gcapi)](https://pypi.org/project/gcapi/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython client for the grand-challenge.org REST API\n\n  - Free software: Apache Software License 2.0\n\n## Features\n\nThis client library is a handy way to interact with the REST API for\ngrand-challenge.org from python, and provides some convenience methods.\nDocumentation and examples can be found on [Grand\nChallenge](https://grand-challenge.org/documentation/grand-challenge-api/).\n\n## Tests\nThis client is tested using the `tox` framework. This enables testing\nthe client in various python-version environments.\n\nFor example, running a specific `your_test` for only the python 3.6\nenvironment can be done as follows:\n```bash\ntox -e py36 -- -k your_test\n```\n',
    'author': 'James Meakin',
    'author_email': 'gcapi@jmsmkn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-gcapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
