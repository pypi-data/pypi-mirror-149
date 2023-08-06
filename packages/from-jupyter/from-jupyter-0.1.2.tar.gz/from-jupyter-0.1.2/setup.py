# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['from_jupyter']

package_data = \
{'': ['*']}

install_requires = \
['imgkit>=1.2.2,<2.0.0', 'jupytext>=1.13.8,<2.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['from-jupyter = from_jupyter.__main__:cli']}

setup_kwargs = {
    'name': 'from-jupyter',
    'version': '0.1.2',
    'description': 'Blogging from Jupyter notebooks',
    'long_description': '(Blogging) from Jupyter\n=======================\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fferegrino/from-jupyter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
