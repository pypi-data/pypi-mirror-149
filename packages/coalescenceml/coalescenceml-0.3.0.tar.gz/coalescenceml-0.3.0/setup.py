# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coalescenceml',
 'coalescenceml.artifact_store',
 'coalescenceml.artifacts',
 'coalescenceml.cli',
 'coalescenceml.config',
 'coalescenceml.container_registry',
 'coalescenceml.integrations',
 'coalescenceml.integrations.mlflow',
 'coalescenceml.integrations.sklearn',
 'coalescenceml.integrations.sklearn.producers',
 'coalescenceml.integrations.sklearn.step',
 'coalescenceml.integrations.statsmodels',
 'coalescenceml.integrations.statsmodels.producers',
 'coalescenceml.integrations.tensorflow',
 'coalescenceml.integrations.tensorflow.producers',
 'coalescenceml.integrations.tensorflow.step',
 'coalescenceml.integrations.xgboost',
 'coalescenceml.integrations.xgboost.producers',
 'coalescenceml.io',
 'coalescenceml.metadata_store',
 'coalescenceml.orchestrator',
 'coalescenceml.pipeline',
 'coalescenceml.post_execution',
 'coalescenceml.producers',
 'coalescenceml.stack',
 'coalescenceml.stack_store',
 'coalescenceml.stack_store.model',
 'coalescenceml.step',
 'coalescenceml.step_operator',
 'coalescenceml.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'distro>=1.7.0,<2.0.0',
 'ml-pipelines-sdk>=1.6.1,<2.0.0',
 'numpy>=1.21.6,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'rich[jupyter]>=12.0.0,<13.0.0',
 'semver>=2.13.0,<3.0.0',
 'sqlmodel>=0.0.6,<0.1.0']

entry_points = \
{'console_scripts': ['coml = coalescenceml.cli.cli:cli']}

setup_kwargs = {
    'name': 'coalescenceml',
    'version': '0.3.0',
    'description': 'An open-source MLOps framework to develop industry-grade production ML pipelines coalescing the MLOps stack under one umbrella.',
    'long_description': '# CoalescenceML\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/coalescenceml)](https://pypi.org/project/coalescenceml/)\n[![PyPI Status](https://pepy.tech/badge/coalescenceml)](https://pepy.tech/project/coalescenceml)\n[![codecov](https://codecov.io/gh/bayoumi17m/CoalescenceML/branch/main/graph/badge.svg?token=7QNV6GV4B3)](https://codecov.io/gh/bayoumi17m/CoalescenceML)\n![GitHub](https://img.shields.io/github/license/bayoumi17m/CoalescenceML)\n[![Interrogate](docs/interrogate.svg)](https://interrogate.readthedocs.io/en/latest/)\n![Main Workflow Tests](https://github.com/bayoumi17m/CoalescenceML/actions/workflows/main.yml/badge.svg)\n\n# What is Coalescence ML?\n\n# Why use Coalescence ML?\n\n# Learn more about Coalescence ML\n\n## Learn more about MLOps\n\n# Features\n\n# Getting Started\n\n## Install Coalescence ML\n\n## Quickstart\n\n',
    'author': 'Magd Bayoumi, Rafael Chaves, Connor Chen, Elva Gao, Sanjali Jha, Iris Li, Jerry Sun, Emily Wang',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.9',
}


setup(**setup_kwargs)
