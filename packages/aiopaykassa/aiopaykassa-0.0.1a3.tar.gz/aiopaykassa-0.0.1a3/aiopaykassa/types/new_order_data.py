import decimal

from pydantic import Field

from .base import PayKassaObject
from ..enums import CryptoCurrency, StrCryptoSystem


class NewOrderData(PayKassaObject):
    invoice: int
    order_id: int
    wallet: str
    amount: decimal.Decimal
    system: StrCryptoSystem
    currency: CryptoCurrency
    url: str
    tag: bool | str = Field(False, api_mutation=lambda v: str(v).lower() if isinstance(v, bool) else v)
