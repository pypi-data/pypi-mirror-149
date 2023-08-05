import aiopaykassa
from ..base import PayKassaEndpoint, Request
from ...exceptions import AioPayKassaError
from ...types import ShopBalance


class GetShopBalanceEndpoint(PayKassaEndpoint):
    __returning__ = ShopBalance

    def url(self) -> str:
        return f"https://paykassa.app/api/{aiopaykassa.__api_version__}/index.php"

    def build_request(self, credentials: dict[str, str | int] = None, test_mode: bool = False) -> Request:
        if credentials is None:
            raise AioPayKassaError("Credentials are required")
        return Request(
            data=self.dict() | {"test": str(test_mode).lower(),
                                "func": "api_get_shop_balance"} | credentials
        )
