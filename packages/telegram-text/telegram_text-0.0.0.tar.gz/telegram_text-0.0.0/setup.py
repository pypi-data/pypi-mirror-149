# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_text']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'telegram-text',
    'version': '0.0.0',
    'description': '',
    'long_description': '# telegram_text',
    'author': 'Vladimir Alinsky',
    'author_email': 'Vladimir@Alinsky.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SKY-ALIN/telegram_text',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
