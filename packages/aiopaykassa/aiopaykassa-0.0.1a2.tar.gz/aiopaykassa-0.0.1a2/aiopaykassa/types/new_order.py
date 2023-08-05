import decimal

from .base import PayKassaObject
from ..enums import Currency, StrSystem


class NewOrder(PayKassaObject):
    invoice: int
    order_id: int
    amount: decimal.Decimal
    system: StrSystem
    currency: Currency
    url: str
