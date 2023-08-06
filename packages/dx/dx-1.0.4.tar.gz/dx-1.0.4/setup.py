# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dx', 'dx.tests']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.31.1', 'pandas>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'dx',
    'version': '1.0.4',
    'description': 'Python wrapper for Data Explorer',
    'long_description': 'A Pythonic Data Explorer.\n\n# Install\n\nFor Python 3.8+:\n```\npip install dx>=1.0.3\n```\n\n# Usage\n\nThe `dx` library currently enables DEX media type visualization of pandas `DataFrames` in two ways:\n- individual calls to `dx.display()`\n- updating the current IPython display formatter for a session\n\n## Importing\n```python\nimport dx\n```\n\n## With `dx.display()`\n`dx.display()` will display a single dataset using the DEX media type. It currently supports:\n- pandas `DataFrame` objects\n  ```python\n  import pandas as pd\n  import random\n\n  df = pd.DataFrame({\n      \'random_ints\': [random.randint(0, 100) for _ in range(500)],\n      \'random_floats\': [random.random() for _ in range(500)],\n  })\n  dx.display(df)\n  ```\n  ![](docs/dx_display_sample1.png)\n\n- tabular data as `dict` or `list` types\n  ```python\n  dx.display([\n    [1, 5, 10, 20, 500],\n    [1, 2, 3, 4, 5],\n    [0, 0, 0, 0, 1]\n  ])\n  ```\n  ![](docs/dx_display_sample2.png)\n\n- `.csv` or `.json` filepaths \n\n  ![](docs/dx_display_sample3.png)\n\n## With `dx.register()` and `dx.deregister()`\n`dx` will update the current `IPython` display formatters to allow DEX media type visualization of pandas `DataFrame` objects for an entire notebook / kernel session instead of the default `DataFrame` display output.\n> Note: this **only** affects pandas DataFrames; it does not affect the display of `.csv`/`.json` file data, or `dict`/`list` outputs\n\n- `dx.register()`\n  \n  ```python\n  import pandas as pd\n\n  # enable DEX display outputs from now on\n  dx.register()\n\n  df = pd.read_csv("examples/sample_data.csv")\n  df\n  ```\n  ```python\n  df2 = pd.DataFrame(\n      [\n          [1, 5, 10, 20, 500],\n          [1, 2, 3, np.nan, 5],\n          [0, 0, 0, np.nan, 1]\n      ],\n      columns=[\'a\', \'b\', \'c\', \'d\', \'e\']\n  )\n  df2\n  ```\n  ![](docs/dx_register_sample1.png)\n\n- `dx.deregister()`\n  \n  ```python\n  df2 = pd.DataFrame(\n      [\n          [1, 5, 10, 20, 500],\n          [1, 2, 3, np.nan, 5],\n          [0, 0, 0, np.nan, 1]\n      ],\n      columns=[\'a\', \'b\', \'c\', \'d\', \'e\']\n  )\n  df2\n  ```\n  ```python\n  dx.deregister()\n  df2\n  ```\n  ![](docs/dx_deregister_sample1.png)\n\n\n# Develop\n\n```\ngit clone https://github.com/noteable-io/dx\ncd ./dx\npip install -e .\n```\n\n\n# Code of Conduct\n\nWe follow the noteable.io code of conduct.\n\n# LICENSE\n\nSee [LICENSE.md](LICENSE.md).',
    'author': 'Dave Shoup',
    'author_email': 'dave.shoup@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://app.noteable.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
