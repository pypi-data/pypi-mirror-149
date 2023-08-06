# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yamt',
    'version': '0.0.1',
    'description': 'yet another monkey toolkit',
    'long_description': '# yamt\n yet another monkey toolkit\n',
    'author': 'lightmanLP',
    'author_email': 'liteman1000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
