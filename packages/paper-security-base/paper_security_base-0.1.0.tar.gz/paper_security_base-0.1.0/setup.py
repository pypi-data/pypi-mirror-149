# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paper_security_base', 'paper_security_base.interface']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'paper-security-base',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'wlsantos',
    'author_email': 'rengaw.luiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
