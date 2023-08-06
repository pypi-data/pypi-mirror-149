# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_preprocessors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'data-preprocessors',
    'version': '0.13.0',
    'description': 'An easy to use tool for Data Preprocessing specially for Text Preprocessing',
    'long_description': '<h1 align="center">\n    <img src="https://github.com/MusfiqDehan/data-preprocessors/raw/master/branding/logo.png">\n</h1>\n\n<p align="center">\n    An easy to use tool for Data Preprocessing specially for Text Preprocessing\n</p>\n\n## Table of Contents\n- [Installation](https://github.com/MusfiqDehan/data-preprocessors#installation)\n- [Quick Start](https://github.com/MusfiqDehan/data-preprocessors#quick-start)\n\n\n## **Installation**\nInstall the latest stable release<br>\n**For windows**<br>\n`$ pip install -U data-preprocessors`\n\n**For Linux/WSL2**<br>\n`$ pip3 install -U data-preprocessors`\n\n## **Quick Start**\n```python\nfrom data_preprocessors import text_preprocessor as tp\nsentence = "bla! bla- ?bla ?bla."\nsentence = tp.remove_punc(sentence)\nprint(sentence)\n\n>> bla bla bla bla\n```\n\n',
    'author': 'Md. Musfiqur Rahaman',
    'author_email': 'musfiqur.rahaman@northsouth.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MusfiqDehan/data-preprocessors',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
