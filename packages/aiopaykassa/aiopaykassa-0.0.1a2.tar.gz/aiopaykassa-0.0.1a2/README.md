# aiopaykassa
paykassa.pro Api Python Async Library

Wrapper for Paykassa.pro API and SCI methods

API example:
```python
from aiopaykassa.clients import PayKassaApi

api = PayKassaApi(api_id=<your_api_id>, api_key=<your_api_key>, shop=<your_merchant_id>)  # test_mode=True for testing

async def print_bitcoin_btc_balance():
    balance = await api.get_shop_balance()
    print(balance.bitcoin_btc)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_bitcoin_btc_balance())
```

SCI example:
```python
import decimal

from aiopaykassa.clients import PayKassaSci
from aiopaykassa.types import NewOrder

sci = PayKassaSci(sci_id=<your_merchant_id>, sci_key=<your_merchant_password>)  # test_mode=True for testing

async def create_order_btc(order_id: int, amount: decimal.Decimal, comment: str) -> NewOrder:
    new_order = await sci.create_order(
        order_id=order_id,
        amount=amount,
        currency=Currency.BTC,
        system=System.BITCOIN,
        comment=comment
    )
    return new_order

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_order_btc(1, decimal.Decimal(0.00001), "test"))
```
