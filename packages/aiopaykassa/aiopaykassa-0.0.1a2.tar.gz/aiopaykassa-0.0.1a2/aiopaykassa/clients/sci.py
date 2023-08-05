import decimal
from typing import Literal

from .base import BasePayKassaSci
from ..endpoints import ConfirmOrderEndpoint, ConfirmTransactionNotificationEndpoint, CreateOrderEndpoint, \
    CreateOrderGetDataEndpoint
from ..enums import Currency, System, ShopClient, CryptoCurrency, CryptoSystem
from ..types import ConfirmedOrder, TransactionNotification, NewOrder, NewOrderData


class PayKassaSci(BasePayKassaSci):
    async def confirm_order(self, private_hash: str) -> ConfirmedOrder:
        """
        Method to confirm order after receiving notification from PayKassa.
        More info: https://paykassa.pro/docs/#api-SCI-sci_confirm_order

        :param private_hash: private_hash sent by PayKassa in notification
        :return:
        """
        endpoint = ConfirmOrderEndpoint(private_hash=private_hash)
        return await self.request(endpoint)

    async def confirm_transaction_notification(self, private_hash: str) -> TransactionNotification:
        """
        Method to confirm transaction notification after receiving notification from PayKassa.
        More info: https://paykassa.pro/docs/#api-SCI-sci_confirm_transaction_notification

        :param private_hash: private_hash sent by PayKassa in notification
        :return:
        """
        endpoint = ConfirmTransactionNotificationEndpoint(private_hash=private_hash)
        return await self.request(endpoint)

    async def create_order(
            self,
            order_id: int,
            amount: decimal.Decimal,
            currency: Currency,
            system: System,
            comment: str,
            phone: Literal[False] = False,
            paid_commission: ShopClient = ShopClient.SHOP) -> NewOrder:
        """
        Get link for deposit
        More info: https://paykassa.pro/docs/#api-SCI-sci_create_order

        :param order_id:
        :param amount:
        :param currency:
        :param system:
        :param comment:
        :param phone:
        :param paid_commission:
        :return:
        """
        endpoint = CreateOrderEndpoint(
            order_id=order_id,
            amount=amount,
            currency=currency,
            system=system,
            comment=comment,
            phone=phone,
            paid_commission=paid_commission
        )
        return await self.request(endpoint)

    async def create_order_get_data(
            self,
            order_id: int,
            amount: decimal.Decimal,
            currency: CryptoCurrency,
            system: CryptoSystem,
            comment: str,
            phone: Literal[False] = False,
            paid_commission: ShopClient = ShopClient.SHOP) -> NewOrderData:
        """
        Get cryptocurrency address for deposit
        More info: https://paykassa.pro/docs/#api-SCI-sci_create_order_get_data

        :param order_id:
        :param amount:
        :param currency:
        :param system:
        :param comment:
        :param phone:
        :param paid_commission:
        :return:
        """
        endpoint = CreateOrderGetDataEndpoint(
            order_id=order_id,
            amount=amount,
            currency=currency,
            system=system,
            comment=comment,
            phone=phone,
            paid_commission=paid_commission
        )
        return await self.request(endpoint)
