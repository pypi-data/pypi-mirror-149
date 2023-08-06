# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typeval']

package_data = \
{'': ['*']}

extras_require = \
{':python_full_version <= "3.9.0"': ['typing-extensions>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'typeval',
    'version': '0.1.0',
    'description': 'Prototype of annotated-types + pydantic-core',
    'long_description': None,
    'author': 'Adrian Garcia Badaracco',
    'author_email': '1755071+adriangb@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
