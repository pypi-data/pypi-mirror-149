# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netsgiro']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=17.4']

extras_require = \
{':python_version < "3.9"': ['backports.zoneinfo>=0.2.1,<0.3.0']}

setup_kwargs = {
    'name': 'netsgiro',
    'version': '2.0.0',
    'description': 'File parsers for Nets AvtaleGiro and OCR Giro',
    'long_description': '.. image:: https://img.shields.io/pypi/v/netsgiro.svg?style=flat\n    :target: https://pypi.org/project/netsgiro/\n    :alt: Latest PyPI version\n\n.. image:: https://github.com/otovo/python-netsgiro/actions/workflows/test.yml/badge.svg\n    :target: https://github.com/otovo/python-netsgiro/actions/workflows/test.yml\n    :alt: Github actions test pipeline status\n\n.. image:: https://img.shields.io/readthedocs/netsgiro.svg\n   :target: https://netsgiro.readthedocs.io/\n   :alt: Read the Docs build status\n\n.. image:: https://img.shields.io/codecov/c/github/otovo/python-netsgiro/master.svg\n   :target: https://codecov.io/gh/otovo/python-netsgiro\n   :alt: Test coverage\n\n========\nnetsgiro\n========\n\nnetsgiro is a Python library for working with `Nets <https://www.nets.eu/>`_\nAvtaleGiro and OCR Giro files.\n\nAvtaleGiro is a direct debit solution that is in widespread use in Norway, with\nmore than 15 000 companies offering it to their customers. OCR Giro is used by\nNets and Norwegian banks to update payees on recent deposits to their bank\naccounts. In combination, AvtaleGiro and OCR Giro allows for a high level of\nautomation of invoicing and payment processing.\n\nThe netsgiro library supports:\n\n- Parsing AvtaleGiro agreements\n- Creating AvtaleGiro payment requests\n- Creating AvtaleGiro cancellations\n- Parsing OCR Giro transactions\n\nnetsgiro is available from PyPI. To install it, run::\n\n    pip install netsgiro\n\nFor details and code examples, see `the netsgiro documentation\n<https://netsgiro.readthedocs.io/>`_.\n\nFor further details, please refer to the official\n`AvtaleGiro <https://www.avtalegiro.no/>`_ and\n`OCR Giro <https://www.nets.eu/no-nb/losninger/inn-og-utbetalinger/ocrgiro/Pages/default.aspx>`_\ndocumentation from Nets.\n\n\nLicense\n=======\n\nCopyright 2017-2019 `Otovo AS <https://www.otovo.com/>`_. Licensed under the\nApache License, Version 2.0. See the ``LICENSE`` file for the full license\ntext.\n\n\nProject resources\n=================\n\n- `Documentation <https://netsgiro.readthedocs.io/>`_\n- `Source code <https://github.com/otovo/python-netsgiro>`_\n- `Issue tracker <https://github.com/otovo/python-netsgiro/issues>`_\n',
    'author': 'Otovo AS',
    'author_email': 'jodal+netsgiro@otovo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/netsgiro/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
