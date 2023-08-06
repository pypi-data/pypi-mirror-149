# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hf_model_s']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=2.4.1,<3.0.0',
 'huggingface-hub>=0.5.1,<0.6.0',
 'joblib>=1.1.0,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'sentence-transformers>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'hf-model-s',
    'version': '0.1.0',
    'description': 'model-s served from hf spaces',
    'long_description': '# model-s\n[![pytest](https://github.com/ffreemt/model-s/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/model-s/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/model_s.svg)](https://badge.fury.io/py/model_s)\n\nmodel-s served from hf spaces\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/model-s\n# poetry add git+https://github.com/ffreemt/model-s\n# git clone https://github.com/ffreemt/model-s && cd model-s\n```\n\n## Use it\n```python\nfrom model_s import model_s\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/model-s',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
