import decimal

from .base import PayKassaObject
from ..enums import Currency, YesNo, StrCryptoSystem


class ConfirmedOrder(PayKassaObject):
    transaction: int
    shop_id: int
    order_id: int
    amount: decimal.Decimal
    currency: Currency
    system: StrCryptoSystem
    address: str | None
    tag: str | None
    hash: str
    partial: YesNo
