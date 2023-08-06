# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hf_model_s_cpu']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'alive-progress>=2.4.1,<3.0.0',
 'huggingface-hub>=0.5.1,<0.6.0',
 'install>=1.3.5,<2.0.0',
 'joblib>=1.1.0,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'nltk>=3.7,<4.0',
 'numpy>=1.22.3,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'tqdm>=4.64.0,<5.0.0',
 'transformers>=4.18.0,<5.0.0']

setup_kwargs = {
    'name': 'hf-model-s-cpu',
    'version': '0.1.0',
    'description': 'model-s served from hf spaces using torch+cpu',
    'long_description': '# model-s\n[![pytest](https://github.com/ffreemt/model-s-cpu/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/model-s-cpu/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/hf_model_s_cpu.svg)](https://badge.fury.io/py/hf_model_s_cpu)\n\nmodel-s served from hf spaces for torch cpu\n\n## Install it\n\n```shell\npip install git+https://github.com/ffreemt/model-s-cpu\n# poetry add git+https://github.com/ffreemt/model-s-cpu\n# git clone https://github.com/ffreemt/model-s-cpu && cd model-s-cpu\n```\n\n## Install `sentence-transformers`\nSimply\n```bash\npip install sentence-transformers\n```\nOr\n```bash\npip install --no-cache-dir torch==1.8.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  # adjust according to os/python\npip install transformers tqdm numpy scikit-learn nltk sentencepiece pillow\npip install --no-deps sentence-transformers\n```\n\n## Use it\n```python\nfrom hf_model_s_cpu import model_s\n\n```\n',
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
