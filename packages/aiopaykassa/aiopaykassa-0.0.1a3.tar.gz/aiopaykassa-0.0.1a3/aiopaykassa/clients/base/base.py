import abc
import asyncio
from http import HTTPStatus

from aiohttp import ClientSession, ClientError

from aiopaykassa.endpoints.base import PayKassaEndpoint, PayKassaType
from aiopaykassa.exceptions import PayKassaNetworkError, PayKassaExternalError, PayKassaBadRequestError
from aiopaykassa.utils import json

DEFAULT_TIMEOUT = 300.0


class BasePayKassaClient:
    def __init__(
            self,
            session: ClientSession = None,
            requests_timeout: float | int = DEFAULT_TIMEOUT,
            test_mode: bool = False,
    ):
        self._session = session
        self._default_timeout = requests_timeout
        self.test_mode = test_mode

    @abc.abstractmethod
    def credentials(self) -> dict[str, str | int]:
        raise NotImplementedError

    async def get_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession()
        return self._session

    async def request(self, endpoint: PayKassaEndpoint, timeout: int = None) -> PayKassaType:
        request = endpoint.build_request(test_mode=self.test_mode, credentials=self.credentials())

        try:
            session = await self.get_session()
            async with session.post(
                endpoint.url(),
                data=request.data,
                timeout=self._default_timeout if timeout is None else timeout,
            ) as resp:
                raw_result = await resp.text()

        except asyncio.TimeoutError:
            raise PayKassaNetworkError(endpoint, "Request timeout error")
        except ClientError as e:
            raise PayKassaNetworkError(endpoint, f"{type(e).__name__}: {e}")
        response = self.check_response(endpoint=endpoint, status_code=resp.status, content=raw_result)
        return response.data

    @staticmethod
    def check_response(endpoint: PayKassaEndpoint, status_code: int, content: str):
        json_data = json.loads(content)
        response = endpoint.build_response(json_data)
        if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED and response.error is False:
            return response

        if status_code == HTTPStatus.BAD_REQUEST:
            raise PayKassaBadRequestError(endpoint, response.message)

        # TODO add exceptions
        # if status_code == HTTPStatus.TOO_MANY_REQUESTS:
        #     raise CpTooManyRequests(endpoint, response.message)
        #
        raise PayKassaExternalError(endpoint, response.message)

    async def disconnect(self):
        if self._session is not None and self._session.closed is False:
            await self._session.close()
