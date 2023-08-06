# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thousandwords_core']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.3.0']

setup_kwargs = {
    'name': 'thousandwords.core',
    'version': '0.7.0',
    'description': '',
    'long_description': None,
    'author': 'Edouard Godfrey',
    'author_email': 'edouard@1000words-hq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
