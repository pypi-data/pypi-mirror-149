from aiopaykassa.endpoints.base import PayKassaEndpoint


class AioPayKassaError(Exception):
    """Base exception for all exceptions raised by aiopaykassa."""
    pass


class PayKassaExternalError(AioPayKassaError):
    def __init__(
        self,
        endpoint: PayKassaEndpoint,
        message: str,
    ) -> None:
        self.message = message
        self.endpoint = endpoint
        super().__init__(message)


class PayKassaNetworkError(PayKassaExternalError):
    """Exception for network errors"""
    pass


class PayKassaBadRequestError(PayKassaExternalError):
    """Exception for bad request errors"""
    pass
