# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepts_forecasting',
 'deepts_forecasting.datasets',
 'deepts_forecasting.logging',
 'deepts_forecasting.metrics',
 'deepts_forecasting.models',
 'deepts_forecasting.models.autoformer',
 'deepts_forecasting.models.darnn',
 'deepts_forecasting.models.deepar',
 'deepts_forecasting.models.informer',
 'deepts_forecasting.models.lstnet',
 'deepts_forecasting.models.modules',
 'deepts_forecasting.models.mqrnn',
 'deepts_forecasting.models.nbeats',
 'deepts_forecasting.models.seq2seq',
 'deepts_forecasting.models.tcn',
 'deepts_forecasting.models.tft',
 'deepts_forecasting.models.transformer',
 'deepts_forecasting.utils',
 'deepts_forecasting.utils.data',
 'tests']

package_data = \
{'': ['*'], 'deepts_forecasting.datasets': ['data/*', 'data/Store_Demand/*']}

install_requires = \
['livereload>=2.6.3,<3.0.0',
 'mkdocs-jupyter>=0.20.1,<0.21.0',
 'pandas==1.3.4',
 'pytorch-lightning==1.5.10',
 'scikit-learn>=0.24.0',
 'torch==1.8.1']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material==8.0.0',
         'mkdocstrings>=0.18.1,<0.19.0'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'deepts-forecasting',
    'version': '0.1.2',
    'description': 'Deep Learning Models for time series prediction..',
    'long_description': '# DeepTS_Forecasting\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/deepts_forecasting">\n    <img src="https://img.shields.io/pypi/v/deepts_forecasting.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/yunxileo/deepts_forecasting/actions">\n    <img src="https://github.com/yunxileo/deepts_forecasting/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://deepts-forecasting.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/deepts-forecasting/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\n**Deepts_forecasting** is a Easy-to-use package for time series forecasting with deep Learning models.\nIt contains a variety of models, from classics such as seq2seq to more complex deep neural networks.\nThe models can all be used in the same way, using `fit()` and `predict()` functions,\n\n\n* Free software: MIT\n\n##  Documentation\n\n* <https://yunxileo.github.io/deepts_forecasting/>\n\n\n## Features\n\n* TODO\n\n\n## Models list\n\n| Model        |        Paper                            |\n|--------------|-----------------------------------------|\n| Seq2Seq      |   [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/pdf/1409.3215.pdf)                                      |\n| DeepAR       |[DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks](https://arxiv.org/abs/1704.04110)                                         |\n| Lstnet       |[Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks](https://arxiv.org/pdf/1703.07015.pdf)                                         |\n| MQ-RNN       |  [A Multi-Horizon Quantile Recurrent Forecaster](https://arxiv.org/pdf/1711.11053.pdf)                                       |\n| N-Beats      | [N-BEATS: Neural basis expansion analysis for interpretable time series forecasting](https://arxiv.org/abs/1905.10437)                                |\n| TCN          |  [An empirical evaluation of generic convolutional and recurrent networks for sequence modeling](https://arxiv.org.1803.01271)                                     |\n| Transformer  |    [Attention Is All You Need](https://arxiv.org/abs/1706.03762)                                     |\n| Informer     |[Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting](https://arxiv.org/abs/2012.07436)                                         |\n| Autoformer   | [Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting](https://arxiv.org/abs/2106.13008)                                        |\n| TFT          | [Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting](https://arxiv.org/pdf/1912.09363.pdf)                                        |\n| MAE          |  [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/pdf/2111.06377.pdf)                                       |\n\n\n## LICENSE\n\nThis project is licensed under the MIT License - see the LICENSE file for details.\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Will Wei',
    'author_email': 'weiwillstat@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yunxileo/deepts_forecasting',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
