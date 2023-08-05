from ..base import PayKassaEndpoint, Request
from ...enums import RatesCurrency
from ...types import CurrencyRate


class CurrencyRateEndpoint(PayKassaEndpoint):
    __returning__ = CurrencyRate

    currency_in: RatesCurrency
    currency_out: RatesCurrency

    def url(self) -> str:
        return "https://currency.paykassa.pro/index.php"

    def build_request(self, credentials: dict[str, str | int] = None, test_mode: bool = False) -> Request:
        return Request(
            data=self.dict()
        )
