# model-s
[![pytest](https://github.com/ffreemt/model-s-cpu/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/model-s-cpu/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/hf_model_s_cpu.svg)](https://badge.fury.io/py/hf_model_s_cpu)

model-s served from hf spaces for torch cpu

## Install it

```shell
pip install git+https://github.com/ffreemt/model-s-cpu
# poetry add git+https://github.com/ffreemt/model-s-cpu
# git clone https://github.com/ffreemt/model-s-cpu && cd model-s-cpu
```

## Install `sentence-transformers`
Simply
```bash
pip install sentence-transformers
```
Or
```bash
pip install --no-cache-dir torch==1.8.0+cpu -f https://download.pytorch.org/whl/torch_stable.html  # adjust according to os/python
pip install transformers tqdm numpy scikit-learn nltk sentencepiece pillow
pip install --no-deps sentence-transformers
```

## Use it
```python
from hf_model_s_cpu import model_s

```
