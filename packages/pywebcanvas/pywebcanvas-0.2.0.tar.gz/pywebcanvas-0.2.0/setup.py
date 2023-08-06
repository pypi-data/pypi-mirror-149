# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywebcanvas']

package_data = \
{'': ['*']}

install_requires = \
['colour>=0.1.5,<0.2.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['pywebcanvas = pywebcanvas.cli:main']}

setup_kwargs = {
    'name': 'pywebcanvas',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Isaac Beverly',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
