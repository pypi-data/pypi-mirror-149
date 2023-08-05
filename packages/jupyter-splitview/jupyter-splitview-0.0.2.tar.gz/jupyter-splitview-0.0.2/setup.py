# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyter_splitview']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=6.13.0,<7.0.0', 'jupyterlab>=3.3.4,<4.0.0']

setup_kwargs = {
    'name': 'jupyter-splitview',
    'version': '0.0.2',
    'description': 'Making before/after image sliders in JupyterLab',
    'long_description': None,
    'author': 'kolibril13',
    'author_email': '44469195+kolibril13@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
