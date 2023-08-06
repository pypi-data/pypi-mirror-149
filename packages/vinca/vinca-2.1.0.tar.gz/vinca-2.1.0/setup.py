# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vinca', 'vinca._lib']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'prompt-toolkit>=3.0.29,<4.0.0']

entry_points = \
{'console_scripts': ['vinca = vinca:run']}

setup_kwargs = {
    'name': 'vinca',
    'version': '2.1.0',
    'description': 'Spaced Repetition CLI',
    'long_description': None,
    'author': 'Oscar Laird',
    'author_email': 'olaird25@gmail.com',
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
