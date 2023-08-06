# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoymiles_modbus', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['plum-py==0.8.0', 'pymodbus>=2.5.3,<3.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=8.2.5,<9.0.0',
         'mkdocs-autorefs>=0.3.1'],
 'doc:python_version >= "3.7" and python_version < "4.0"': ['mkdocstrings>=0.18.0,<0.19.0'],
 'test': ['black==22.3.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'hoymiles-modbus',
    'version': '0.4.0',
    'description': 'Gather data from Hoymiles microinverters.',
    'long_description': '# hoymiles_modbus\n\n\n[![pypi](https://img.shields.io/pypi/v/hoymiles_modbus.svg)](https://pypi.org/project/hoymiles_modbus/)\n[![python](https://img.shields.io/pypi/pyversions/hoymiles_modbus.svg)](https://pypi.org/project/hoymiles_modbus/)\n[![Build Status](https://github.com/wasilukm/hoymiles_modbus/actions/workflows/dev.yml/badge.svg)](https://github.com/wasilukm/hoymiles_modbus/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/wasilukm/hoymiles_modbus/branch/main/graphs/badge.svg)](https://codecov.io/github/wasilukm/hoymiles_modbus)\n\n\n\nPython library for gathering data from Hoymiles microinverters.\n\nThe library communicates with DTU (DTU-Pro) which is a proxy/monitoring device for microinverters.\nDTU should be connected via its `Ethernet` port and should have IP address assigned by DHCP server.\n\n\n* Documentation: <https://wasilukm.github.io/hoymiles_modbus>\n* GitHub: <https://github.com/wasilukm/hoymiles_modbus>\n* PyPI: <https://pypi.org/project/hoymiles_modbus/>\n* Free software: MIT\n\n\n## Features\n\n* Communication via Modbus TCP\n* Decode all microinverter status registers, which include information such as:\n  * current production\n  * total production\n  * today production\n  * temperature\n  * alarms\n  * status\n  * grid voltage and frequency\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Foo Bar',
    'author_email': 'foo@bar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wasilukm/hoymiles_modbus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
