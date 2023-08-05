# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmcifix']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0',
 'click>=7.0.0,<8.0.0',
 'inflection>=0.5.1,<0.6.0',
 'more-itertools>=8.12.0,<9.0.0']

entry_points = \
{'console_scripts': ['mmcifix = mmcifix:main']}

setup_kwargs = {
    'name': 'mmcifix',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Michael Milton',
    'author_email': 'michael.r.milton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
