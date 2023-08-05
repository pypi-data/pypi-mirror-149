import decimal

from .base import PayKassaObject


class ShopBalance(PayKassaObject):
    berty_rub: decimal.Decimal
    perfectmoney_usd: decimal.Decimal
    berty_usd: decimal.Decimal
    bitcoin_btc: decimal.Decimal
    ethereum_eth: decimal.Decimal
    litecoin_ltc: decimal.Decimal
    dogecoin_doge: decimal.Decimal
    dash_dash: decimal.Decimal
    bitcoincash_bch: decimal.Decimal
    zcash_zec: decimal.Decimal
    ripple_xrp: decimal.Decimal
    tron_trx: decimal.Decimal
    stellar_xlm: decimal.Decimal
    binancecoin_bnb: decimal.Decimal
    tron_trc20_usdt: decimal.Decimal
    binancesmartchain_bep20_usdt: decimal.Decimal
    ethereum_erc20_usdt: decimal.Decimal
    binancesmartchain_bep20_busd: decimal.Decimal
    binancesmartchain_bep20_usdc: decimal.Decimal
    binancesmartchain_bep20_ada: decimal.Decimal
    binancesmartchain_bep20_eos: decimal.Decimal
    binancesmartchain_bep20_btc: decimal.Decimal
    binancesmartchain_bep20_eth: decimal.Decimal
    binancesmartchain_bep20_doge: decimal.Decimal
