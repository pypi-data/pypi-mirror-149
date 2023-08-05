import enum


class RatesCurrency(enum.Enum):
    USD = "USD"
    RUB = "RUB"
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DOGE = "DOGE"
    DASH = "DASH"
    BCH = "BCH"
    ZEC = "ZEC"
    XRP = "XRP"
    TRX = "TRX"
    XLM = "XLM"
    BNB = "BNB"
    USDT = "USDT"
    ADA = "ADA"
    EOS = "EOS"
    GBP = "GBP"
    EUR = "EUR"
    USDC = "USDC"
    BUSD = "BUSD"


class Currency(enum.Enum):
    USD = "USD"
    RUB = "RUB"
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DOGE = "DOGE"
    DASH = "DASH"
    BCH = "BCH"
    ZEC = "ZEC"
    XRP = "XRP"
    TRX = "TRX"
    XLM = "XLM"
    BNB = "BNB"
    USDT = "USDT"
    BUSD = "BUSD"
    USDC = "USDC"
    ADA = "ADA"
    EOS = "EOS"


class CryptoCurrency(enum.Enum):
    BTC = "BTC"
    ETH = "ETH"
    LTC = "LTC"
    DOGE = "DOGE"
    DASH = "DASH"
    BCH = "BCH"
    ZEC = "ZEC"
    XRP = "XRP"
    TRX = "TRX"
    XLM = "XLM"
    BNB = "BNB"
    USDT = "USDT"
    BUSD = "BUSD"
    USDC = "USDC"
    ADA = "ADA"
    EOS = "EOS"


class System(enum.IntEnum):
    PERFECT_MONEY = 2
    BERTY = 3
    BITCOIN = 11
    ETHEREUM = 12
    LITECOIN = 14
    DOGECOIN = 15
    DASH = 16
    BITCOIN_CASH = 18
    ZCASH = 19
    RIPPLE = 22
    TRON = 27
    STELLAR = 28
    BINANCE_COIN = 29
    TRON_TRC20 = 30
    BINANCE_SMART_CHAIN_BEP20 = 31
    ETHEREUM_ERC20 = 32


class StrSystem(enum.Enum):
    PERFECT_MONEY = "PerfectMoney"
    BERTY = "Berty"
    BITCOIN = "BitCoin"
    ETHEREUM = "Ethereum"
    LITECOIN = "Litecoin"
    DOGECOIN = "Dogecoin"
    DASH = "Dash"
    BITCOIN_CASH = "BitcoinCash"
    ZCASH = "Zcash"
    RIPPLE = "Ripple"
    TRON = "TRON"
    STELLAR = "Stellar"
    BINANCE_COIN = "BinanceCoin"
    TRON_TRC20 = "TRON_TRC20"
    BINANCE_SMART_CHAIN_BEP20 = "BinanceSmartChain_BEP20"
    ETHEREUM_ERC20 = "Ethereum_ERC20"


class CryptoSystem(enum.IntEnum):
    BITCOIN = 11
    ETHEREUM = 12
    LITECOIN = 14
    DOGECOIN = 15
    DASH = 16
    BITCOIN_CASH = 18
    ZCASH = 19
    RIPPLE = 22
    TRON = 27
    STELLAR = 28
    BINANCE_COIN = 29
    TRON_TRC20 = 30
    BINANCE_SMART_CHAIN_BEP20 = 31
    ETHEREUM_ERC20 = 32


class StrCryptoSystem(enum.Enum):
    BITCOIN = "BitCoin"
    ETHEREUM = "Ethereum"
    LITECOIN = "Litecoin"
    DOGECOIN = "Dogecoin"
    DASH = "Dash"
    BITCOIN_CASH = "BitcoinCash"
    ZCASH = "Zcash"
    RIPPLE = "Ripple"
    TRON = "TRON"
    STELLAR = "Stellar"
    BINANCE_COIN = "BinanceCoin"
    TRON_TRC20 = "TRON_TRC20"
    BINANCE_SMART_CHAIN_BEP20 = "BinanceSmartChain_BEP20"
    ETHEREUM_ERC20 = "Ethereum_ERC20"


class ShopClient(enum.Enum):
    SHOP = "shop"
    CLIENT = "client"


class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class YesNo(enum.Enum):
    YES = "yes"
    NO = "no"
