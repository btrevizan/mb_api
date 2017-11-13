"""Enumerate available coins."""


from enum import Enum


class Url(Enum):
    """Each URL represents a base PATH for API requests."""

    HOST = 'https://www.mercadobitcoin.net'
    API_PATH = '/api/'
    TAPI_PATH = '/tapi/v3/'

    API = HOST + API_PATH
    TAPI = HOST + TAPI_PATH


class Coin(Enum):
    """Each coin represents its value for API params."""

    BRL = 'BRL'
    BTC = 'BRLBTC'
    LTC = 'BRLLTC'
    BCH = 'BRLBCH'


class Method(Enum):
    """Each method represents its name for API and TAPI params."""

    TICKER = 'ticker'
    ORDERBOOK = 'orderbook'
    TRADES = 'trades'

    SYS_MSG = 'list_system_messages'
    ACCOUNT_INFO = 'get_account_info'
    GET_ORDER = 'get_order'
    ORDERS = 'list_orders'
    LIST_ORDERBOOK = 'list_orderbook'
    BUY = 'place_buy_order'
    SELL = 'place_sell_order'
    CANCEL = 'cancel_order'
    WITHDRAWAL = 'get_withdrawal'
    WITHDRAW = 'withdraw_coin'
