# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exodusutils',
 'exodusutils.exceptions',
 'exodusutils.feature_engineering',
 'exodusutils.internal',
 'exodusutils.migration',
 'exodusutils.predict',
 'exodusutils.preprocessing',
 'exodusutils.schemas']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'fastapi>=0.74.1,<0.75.0',
 'numpy==1.21',
 'pandas>=1.4.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pymongo[encryption]>=4.0.1,<5.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'exodusutils',
    'version': '0.1.23',
    'description': 'Utility functions and helper classes for Exodus project',
    'long_description': "# Exodus common utilities\n\nThis is the library defining the schemas for exodus utilities.\n\n## Structure\n\n### `exodusutils`\n\nContains helpful utility functions.\n\n### `schemas`\n\nIn the `schemas` folder you can find the following:\n- Schema definitions for the model algorithm's incoming requests\n- Schema definitions for the model algorithm's responses\n- Definitions for `RegressionScores` and `ClassificationScores`\n- Definitions for types such as `Attribute` and `Column`\n\n### `predict`\n\nThe `predict` folder contains helper functions for prediction.\n\n### `enums.py`\n\nContains enums used by Exodus. Current contains the following:\n- `TimeUnit`, with helper methods to convert timestamps to different formats\n- `DataType`, with helper methods to convert from `Pandas` types\n\n### `feature_engineering.py`\n\nContains commonly used feature engineering methods. Currently includes:\n- One-hot encoding\n- Label encoding\n- Time component encoding\nIt is recommended to use at least 1 method in this file during training.\n\n### `frame_manipulation.py`\n\nContains multiple frame manipulation methods. Used during prediction, should pick the method that corresponds to the one used during training.\n\n### `frames.py`\n\nContains definitions and helper functions for the following classes:\n- `SplitFrames`: A 3-tuple with a training dataframe, a testing dataframe, and a validation dataframe.\n- `CVFrames`: A list of `SplitFrames`. Should not be instantiated manually, user should use `CVFrames.iid` helper classmethod.\n",
    'author': 'Tsung-Ju Lii',
    'author_email': 'andylii@mobagel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
