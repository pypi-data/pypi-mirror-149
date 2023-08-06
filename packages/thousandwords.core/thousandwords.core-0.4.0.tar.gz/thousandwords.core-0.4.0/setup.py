# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thousandwords_core']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'thousandwords.core',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Gai Luron',
    'author_email': 'gai.luron.1964@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
