# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nannyml',
 'nannyml.datasets',
 'nannyml.datasets.data',
 'nannyml.drift',
 'nannyml.drift.model_inputs',
 'nannyml.drift.model_inputs.multivariate',
 'nannyml.drift.model_inputs.multivariate.data_reconstruction',
 'nannyml.drift.model_inputs.univariate',
 'nannyml.drift.model_inputs.univariate.statistical',
 'nannyml.drift.model_outputs',
 'nannyml.drift.target',
 'nannyml.drift.target.target_distribution',
 'nannyml.performance_calculation',
 'nannyml.performance_estimation',
 'nannyml.performance_estimation.confidence_based',
 'nannyml.plots',
 'tests',
 'tests.performance_calculation',
 'tests.performance_estimation']

package_data = \
{'': ['*'], 'tests': ['manual/*']}

install_requires = \
['category-encoders>=2.3.0,<3.0.0',
 'joblib>=1.1.0,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'offset>=0.0.2,<0.0.3',
 'pandas>=1.3.0,<2.0.0',
 'plotly>=5.6.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.7.3,<1.8.0',
 'seaborn>=0.11.2,<0.12.0',
 'types-python-dateutil>=2.8.9,<3.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['Sphinx>=4.4.0,<5.0.0',
         'sphinx-rtd-theme>=1.0.0,<2.0.0',
         'jupyterlab>=3.2.9,<4.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0',
          'pytest-mock>=3.7.0,<4.0.0']}

setup_kwargs = {
    'name': 'nannyml',
    'version': '0.3.2',
    'description': 'The NannyML library, monitoring model performance since 2020.',
    'long_description': '<p align="center">\n    <img src="https://assets.website-files.com/6099466e98d9381b3f745b9a/60994ab2b5bd890780db9c84_NannyML%20logo%20horizontal%20typfont.png">\n</p>\n<p align="center">\n    <a href="https://pypi.org/project/nannyml/">\n        <img src="https://img.shields.io/pypi/v/nannyml.svg">\n    </a>\n    <a href="https://pypi.org/project/nannyml/">\n        <img src="https://img.shields.io/pypi/pyversions/nannyml.svg">\n    </a>\n    <a href="https://github.com/nannyml/nannyml/actions/workflows/dev.yml">\n        <img src="https://github.com/NannyML/nannyml/actions/workflows/dev.yml/badge.svg">\n    </a>\n    <a href="https://codecov.io/gh/NannyML/nannyml">\n        <img src="https://codecov.io/gh/NannyML/nannyml/branch/main/graph/badge.svg?token=OGpF5gVzfR">\n    </a>\n    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/nannyml?color=green">\n</p>\n\n<p align="center">\n    <strong>\n        <a href="https://nannyml.com/">Website</a>\n        •\n        <a href="https://docs.nannyml.com">Docs</a>\n        •\n        <a href="https://nannymlbeta.slack.com">Community Slack</a>\n    </strong>\n</p>\n\n# Basic overview\n\nNannyML helps you monitor your ML models in production by:\n\n* estimating performance in absence of ground truth\n* calculating realized performance metrics\n* detecting data drift on model inputs, model outputs and targets\n\n# Installing the latest stable release\n\n```python\npip install nannyml\n```\n\n\n# Installing the latest development version\n\n```python\npython -m pip install git+https://github.com/NannyML/nannyml\n```\n\n\n# Getting started\n\n```python\nimport nannyml as nml\nimport pandas as pd\n\n# Load some data\nreference_data, analysis_data, _ = nml.load_synthetic_sample()\ndata = pd.concat([reference_data, analysis_data])\nmetadata = nml.extract_metadata(reference_data)\n\n# Estimate performance\nestimator = nml.CBPE(metadata).fit(reference_data)\nestimates = estimator.estimate(data)\n\nestimates.plot(kind=\'performance\').show()\n```\n\n# Examples\n\n* [Performance estimation](<https://docs.nannyml.com/latest/guides/performance_estimation.html>)\n* [Realized performance calculation](https://docs.nannyml.com/latest/guides/performance_calculation.html)\n* [Univariate model input drift detection](https://docs.nannyml.com/latest/guides/data_drift.html#univariate-drift-detection)\n* [Multivariate model input drift detection](https://docs.nannyml.com/latest/guides/data_drift.html#drift-detection-for-model-outputs)\n* [Model output drift detection](https://docs.nannyml.com/latest/guides/data_drift.html#drift-detection-for-model-outputs)\n* [Model target distribution](https://docs.nannyml.com/latest/guides/data_drift.html#drift-detection-for-model-targets)\n\n# Development setup\n\n* Read the docs on [how to contribute](CONTRIBUTING.md)\n',
    'author': 'Niels Nuyttens',
    'author_email': 'niels@nannyml.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnansters/nannyml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
