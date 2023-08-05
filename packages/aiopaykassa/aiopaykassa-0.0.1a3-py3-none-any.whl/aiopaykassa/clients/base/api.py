from aiohttp import ClientSession

from .base import BasePayKassaClient, DEFAULT_TIMEOUT


class BasePayKassaApi(BasePayKassaClient):
    def __init__(
            self,
            api_id: int,
            api_key: str,
            shop: str,
            session: ClientSession = None,
            requests_timeout: float | int = DEFAULT_TIMEOUT,
            test_mode: bool = False,
    ):
        super().__init__(
            session=session,
            requests_timeout=requests_timeout,
            test_mode=test_mode
        )
        self._api_id = api_id
        self._api_key = api_key
        self._shop = shop

    def credentials(self) -> dict[str, str | int]:
        return {"api_id": self._api_id, "api_key": self._api_key, "shop": self._shop}
