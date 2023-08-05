from aiohttp import ClientSession

from .base import BasePayKassaClient, DEFAULT_TIMEOUT


class BasePayKassaSci(BasePayKassaClient):
    def __init__(
            self,
            sci_id: int,
            sci_key: str,
            session: ClientSession = None,
            requests_timeout: float | int = DEFAULT_TIMEOUT,
            test_mode: bool = False,
    ):
        super().__init__(
            session=session,
            requests_timeout=requests_timeout,
            test_mode=test_mode
        )
        self._sci_id = sci_id
        self._sci_key = sci_key

    def credentials(self) -> dict[str, str | int]:
        return {"sci_id": self._sci_id, "sci_key": self._sci_key}
