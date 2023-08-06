# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy_config', 'classy_config.loader']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'typing-inspect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'classy-config',
    'version': '0.2.2',
    'description': 'ClassyConfig is a Python3 package aiming to remove the need for a config.py or settings.py file.',
    'long_description': '<div align="center">\n    <img align="center" src="https://raw.githubusercontent.com/GDWR/classy-config/main/docs/favicon.ico" alt="ClassyConfig Logo">\n    <h1 align="center">ClassyConfig</h1>\n</div>\n\n<div align="center">\n    <strong>ClassyConfig</strong> is a Python3 package aiming to remove the need for a <strong>config.py</strong> or <strong>settings.py</strong> file.\n</div>\n\n<br>\n\n<div align="center">\n    <a href="https://github.com/GDWR/classy-config/actions"><img alt="Checks Pipeline Badge" src="https://github.com/GDWR/classy-config/actions/workflows/checks.yml/badge.svg?branch=main"></a>\n    <a href="https://github.com/GDWR/classy-config/actions"><img alt="Create Documentation Badge" src="https://github.com/GDWR/classy-config/actions/workflows/create-documentation.yml/badge.svg?branch=main"></a>\n    <a href="https://github.com/GDWR/classy-config/actions"><img alt="Build and Publish Badge" src="https://github.com/GDWR/classy-config/actions/workflows/build-and-publish.yml/badge.svg?branch=main"></a>\n</div>\n<div align="center">\n    <a href="https://pypi.org/project/classy-config/"><img alt="PyPI" src="https://img.shields.io/pypi/v/classy-config"></a>\n    <a href="https://github.com/GDWR/classy-config/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>\n    <a href="https://pepy.tech/project/classy-config"><img alt="Downloads" src="https://pepy.tech/badge/classy-config"></a>\n</div> \n\n---\n\n## [Documentation](https://gdwr.github.io/classy-config/)\n\n## Installation\n\n**ClassyConfig** is avliable via Pypi, so it can be installed using **pip**\n\n```shell\n$ pip install classy_config\n```\n\n## Usage\n\n[View on the docs](https://gdwr.github.io/classy-config/source/getting-started/index.html)\n\n```python\nfrom classy_config import ConfigValue, register_config\nfrom pydantic import BaseModel\n\n# Register your config file to be used\nregister_config(filepath="config.toml")\n\n# Resolve default values based on your config\ndef print_current_version(version: str = ConfigValue("package", str)) -> None:\n    print(version)\n\n# Use Pydantic Models for your config\nclass Author(BaseModel):\n    username: str\n    email: str\n    lucky_number: int\n\n# Resolve default values based on your config\ndef print_author(author: Author = ConfigValue("author", Author)) -> None:\n    print(author)\n\n# Allows for nested values\ndef print_value(value: int = ConfigValue("nested.value", int)) -> None:\n    print(value)\n```\n',
    'author': 'GDWR',
    'author_email': 'gregory.dwr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GDWR/classy-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
