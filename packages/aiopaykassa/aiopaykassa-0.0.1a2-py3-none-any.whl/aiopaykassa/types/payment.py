import decimal

from .base import PayKassaObject
from ..enums import Currency, StrSystem


class Payment(PayKassaObject):
    shop_id: int
    transaction: str
    txid: str
    amount: str
    amount_pay: str
    system: StrSystem
    currency: Currency
    number: str
    shop_comission_percent: decimal.Decimal
    shop_comission_amount: decimal.Decimal
    paid_commission: str
