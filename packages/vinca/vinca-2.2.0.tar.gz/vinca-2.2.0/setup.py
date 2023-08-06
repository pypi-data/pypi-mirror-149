# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vinca', 'vinca._lib']

package_data = \
{'': ['*'],
 'vinca': ['.idea/.gitignore',
           '.idea/.gitignore',
           '.idea/.gitignore',
           '.idea/.gitignore',
           '.idea/.gitignore',
           '.idea/inspectionProfiles/*',
           '.idea/misc.xml',
           '.idea/misc.xml',
           '.idea/misc.xml',
           '.idea/misc.xml',
           '.idea/misc.xml',
           '.idea/modules.xml',
           '.idea/modules.xml',
           '.idea/modules.xml',
           '.idea/modules.xml',
           '.idea/modules.xml',
           '.idea/vcs.xml',
           '.idea/vcs.xml',
           '.idea/vcs.xml',
           '.idea/vcs.xml',
           '.idea/vcs.xml',
           '.idea/vinca.iml',
           '.idea/vinca.iml',
           '.idea/vinca.iml',
           '.idea/vinca.iml',
           '.idea/vinca.iml'],
 'vinca._lib': ['.idea/*', '.idea/inspectionProfiles/*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'prompt-toolkit>=3.0.29,<4.0.0', 'rich>=12.4.1,<13.0.0']

entry_points = \
{'console_scripts': ['vinca = vinca:run']}

setup_kwargs = {
    'name': 'vinca',
    'version': '2.2.0',
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
