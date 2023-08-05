from .base import BasePayKassaApi
from ..endpoints import CurrencyRateEndpoint, GetShopBalanceEndpoint, PaymentEndpoint
from ..enums import RatesCurrency, Currency, System, ShopClient, Priority
from ..types import CurrencyRate, ShopBalance, Payment


class PayKassaApi(BasePayKassaApi):
    async def currency_rate(
            self,
            currency_in: RatesCurrency,
            currency_out: RatesCurrency) -> CurrencyRate:
        """get currency rate for pair"""
        endpoint = CurrencyRateEndpoint(currency_in=currency_in, currency_out=currency_out)
        return await self.request(endpoint)

    async def get_shop_balance(self) -> ShopBalance:
        """get balance of merchant"""
        endpoint = GetShopBalanceEndpoint()
        return await self.request(endpoint)

    async def payment(
            self,
            amount: int | float,
            currency: Currency,
            system: System,
            number: str,
            tag: int | float | None = None,
            paid_commission: ShopClient = ShopClient.SHOP,
            priority: Priority = Priority.MEDIUM) -> Payment:
        """Instant payment. Method for making automatic masspayments from your merchant account."""
        endpoint = PaymentEndpoint(
            amount=amount,
            currency=currency,
            system=system,
            paid_commission=paid_commission,
            number=number,
            tag=tag,
            priority=priority
        )
        return await self.request(endpoint)
