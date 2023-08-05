import decimal

from .base import PayKassaObject


class CurrencyRate(PayKassaObject):
    value: decimal.Decimal
