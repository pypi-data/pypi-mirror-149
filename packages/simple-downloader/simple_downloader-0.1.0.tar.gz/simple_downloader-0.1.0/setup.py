# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_downloader']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8,<2.0', 'requests>=2', 'rich>=10', 'tqdm>=4']

setup_kwargs = {
    'name': 'simple-downloader',
    'version': '0.1.0',
    'description': 'A very simple downloader package with a visual indication.',
    'long_description': '# Simple Downloader\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/simple_downloader/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
