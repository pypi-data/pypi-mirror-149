# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailer']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'wafflehacks-mailer',
    'version': '0.2.0',
    'description': 'The Python SDK for the WaffleHacks mailer',
    'long_description': '# Mailer\n\nThe Python SDK for the WaffleHacks [mailer](https://github.com/WaffleHacks/mailer) service.\nThe SDK uses the HTTP API, providing blocking and non-blocking (asynchronous) variants.',
    'author': 'Alex Krantz',
    'author_email': 'alex@krantz.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
