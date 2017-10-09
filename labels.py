"""Enumerate available coins."""


from enum import Enum


class Url(Enum):
    """Each URL represents a base PATH for API requests."""

    API = 'https://www.mercadobitcoin.net/api'


class Coin(Enum):
    """Each coin represents its value for API params."""

    BTC = 'BTC'
    LTC = 'LTC'
    BCH = 'BCH'


class Method(Enum):
    """Each method represents its name for API params."""

    TICKER = 'ticker'
    ORDERBOOK = 'orderbook'
    TRADES = 'trades'
