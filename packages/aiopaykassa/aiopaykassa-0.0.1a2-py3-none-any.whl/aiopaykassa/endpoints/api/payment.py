import aiopaykassa
from ..base import PayKassaEndpoint, Request
from ...enums import Currency, System, ShopClient, Priority
from ...exceptions import AioPayKassaError
from ...types import Payment


class PaymentEndpoint(PayKassaEndpoint):
    __returning__ = Payment

    amount: int | float
    currency: Currency
    system: System
    paid_commission: ShopClient = ShopClient.SHOP
    number: str
    tag: int | float | None = None
    priority: Priority = Priority.MEDIUM

    def url(self) -> str:
        return f"https://paykassa.app/api/{aiopaykassa.__api_version__}/index.php"

    def build_request(self, credentials: dict[str, str | int] = None, test_mode: bool = False) -> Request:
        if credentials is None:
            raise AioPayKassaError("Credentials are required")
        return Request(
            data=self.dict(exclude_none=True) | {"test": str(test_mode).lower(),
                                                 "func": "api_payment"} | credentials
        )
