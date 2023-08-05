# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitbanker_sdk']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'bitbanker-sdk',
    'version': '0.0.1',
    'description': 'Bitbanker.org API client',
    'long_description': 'bitbanker-sdk\n-----------------\n\n.. image:: https://img.shields.io/pypi/v/bitbanker-sdk.svg\n    :target: https://pypi.python.org/pypi/bitbanker-sdk\n\n.. image:: https://img.shields.io/pypi/pyversions/bitbanker-sdk.svg\n    :target: https://pypi.python.org/pypi/bitbanker-sdk\n\n.. image:: https://codecov.io/gh/melnikovsa/python-bitbanker-sdk/branch/main/graph/badge.svg\n    :target: https://app.codecov.io/gh/melnikovsa/python-bitbanker-sdk\n\n.. image:: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/tests.yml/badge.svg\n    :target: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/tests.yml\n\n.. image:: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/pypi.yml/badge.svg\n    :target: https://github.com/melnikovsa/python-bitbanker-sdk/actions/workflows/pypi.yml\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/python/black\n\n\nThis is an sync/async Python `Bitbanker`__ API client.\n\n.. _Bitbanker: https://bitbanker.org/\n\n__ Bitbanker_\n\n\nInstallation\n------------\n\nThe project is available on PyPI. Simply run::\n\n    $ pip install bitbanker-sdk\n\n\nUsage\n-----\nWith sync python application::\n\n    from bitbanker_sdk import BitbankerClient\n    from bitbanker_sdk import InvoiceData\n    from bitbanker_sdk import Currency\n\n    client = BitbankerClient(api_key="<your bitbanker api key>")\n    invoice_data = InvoiceData(\n            amount=1000,\n            payment_currencies=[Currency.ETH, Currency.BTC],\n            description=\'invoice description\',\n            header=\'invoice header\'\n        )\n\n    response = client.create_invoice(invoice_data=invoice_data)\n    print(response.link)\n\nWith async python application::\n\n    from bitbanker_sdk import AsyncBitbankerClient\n    from bitbanker_sdk import InvoiceData\n    from bitbanker_sdk import Currency\n\n    client = AsyncBitbankerClient(api_key="<your bitbanker api key>")\n    invoice_data = InvoiceData(\n            amount=1000,\n            payment_currencies=[Currency.ETH, Currency.BTC],\n            description=\'invoice description\',\n            header=\'invoice header\'\n        )\n\n    response = await client.create_invoice(invoice_data=invoice_data)\n    print(response.link)\n',
    'author': 'Evgeny Solomatin',
    'author_email': 'solgenya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/melnikovsa/python-bitbanker-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
