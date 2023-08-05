import decimal
from datetime import datetime
from typing import Literal

from .base import PayKassaObject
from ..enums import Currency, YesNo, CryptoSystem, StrCryptoSystem


class TransactionNotification(PayKassaObject):
    transaction: int
    txid: str
    shop_id: int
    order_id: int  # TODO: check type
    amount: decimal.Decimal
    fee: decimal.Decimal
    currency: Currency
    system: StrCryptoSystem
    address_from: str
    address: str
    tag: str
    confirmations: int
    required_confirmations: int
    status: YesNo
    static: Literal["yes"] = "yes"  # check if it is static
    date_update: datetime  # TODO: check serialization/deseialization
    explorer_address_link: str
    explorer_transaction_link: str
