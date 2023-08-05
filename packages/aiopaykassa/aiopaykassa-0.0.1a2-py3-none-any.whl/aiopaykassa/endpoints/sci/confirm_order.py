import aiopaykassa
from ..base import PayKassaEndpoint, Request
from ...exceptions import AioPayKassaError
from ...types import ConfirmedOrder


class ConfirmOrderEndpoint(PayKassaEndpoint):
    __returning__ = ConfirmedOrder

    private_hash: str

    def url(self) -> str:
        return f"https://paykassa.app/sci/{aiopaykassa.__sci_version__}/index.php"

    def build_request(self, credentials: dict[str, str | int] = None, test_mode: bool = False) -> Request:
        if credentials is None:
            raise AioPayKassaError("Credentials are required")
        return Request(
            data=self.dict() | {"test": str(test_mode).lower(),
                                "func": "sci_confirm_order"} | credentials
        )
