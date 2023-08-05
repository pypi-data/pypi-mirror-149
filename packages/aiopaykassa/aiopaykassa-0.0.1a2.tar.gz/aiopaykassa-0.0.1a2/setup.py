# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopaykassa',
 'aiopaykassa.clients',
 'aiopaykassa.clients.base',
 'aiopaykassa.endpoints',
 'aiopaykassa.endpoints.api',
 'aiopaykassa.endpoints.sci',
 'aiopaykassa.types',
 'aiopaykassa.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{'ujson': ['ujson>=5.2.0,<6.0.0']}

setup_kwargs = {
    'name': 'aiopaykassa',
    'version': '0.0.1a2',
    'description': 'Paykassa.pro asyncio python client',
    'long_description': '# aiopaykassa\npaykassa.pro Api Python Async Library\n\nWrapper for Paykassa.pro API and SCI methods\n\nAPI example:\n```python\nfrom aiopaykassa.clients import PayKassaApi\n\napi = PayKassaApi(api_id=<your_api_id>, api_key=<your_api_key>, shop=<your_merchant_id>)  # test_mode=True for testing\n\nasync def print_bitcoin_btc_balance():\n    balance = await api.get_shop_balance()\n    print(balance.bitcoin_btc)\n\ndef main():\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(print_bitcoin_btc_balance())\n```\n\nSCI example:\n```python\nimport decimal\n\nfrom aiopaykassa.clients import PayKassaSci\nfrom aiopaykassa.types import NewOrder\n\nsci = PayKassaSci(sci_id=<your_merchant_id>, sci_key=<your_merchant_password>)  # test_mode=True for testing\n\nasync def create_order_btc(order_id: int, amount: decimal.Decimal, comment: str) -> NewOrder:\n    new_order = await sci.create_order(\n        order_id=order_id,\n        amount=amount,\n        currency=Currency.BTC,\n        system=System.BITCOIN,\n        comment=comment\n    )\n    return new_order\n\ndef main():\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(create_order_btc(1, decimal.Decimal(0.00001), "test"))\n```\n',
    'author': 'drforse',
    'author_email': 'george.lifeslice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drforse/aiopaykassa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
