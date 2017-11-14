"""Mercado Bitcoin's Trade API implementation.

For more information about data structure, methods and stuff, go to
https://www.mercadobitcoin.com.br/trade-api
"""


import requests
import hashlib
import urllib
import hmac
import json
import time

from random import randint
from .labels import Coin, Url, Method


class Auth():
    """Athentication information."""

    def __init__(self, **kwargs):
        """Set information needed for authentication.

        Keyword arguments:
            id -- user's tapi id
            pin -- user's pin number
            secret -- user's tapi secret
        """
        self.__id = str(kwargs['id'])
        self.__pin = str(kwargs['pin'])
        self.__secret = bytes(str(kwargs['secret']), 'ASCII')

    def id(self):
        """Return user's TAPI id."""
        return self.__id

    def pin(self):
        """Return user's PIN number."""
        return self.__pin

    def secret(self):
        """Return user's TAPI secret."""
        return self.__secret


class Response():
    """Represent a TAPI response.

    Properties:
        data
        status_code
        error_msg (optional)
        server_timestamp
    """

    def __init__(self, response):
        """Set properties.

        Keyword arguments:
            response -- a dict with response
        """
        self.data = response.get('response_data', None)
        self.status_code = response['status_code']
        self.server_timestamp = response['server_unix_timestamp']
        self.error_msg = response.get('error_message', '')

    def __str__(self):
        """A string representation of Response."""
        return str({'data': self.data,
                    'status_code': self.status_code,
                    'server_timestamp': self.server_timestamp,
                    'error_msg': self.error_msg})


class Trade():
    """Implement Trade API methods.

    Methods:


    See method.__doc__ for method's description.
    """

    def __init__(self, auth, coin=Coin.BTC):
        """Set auth properties and coin type.

        Keyword argument:
            auth -- an Auth object
            coin -- coin type (Default Coin.BTC)
        """
        self.__id = auth.id()
        self.__pin = auth.pin()
        self.__secret = auth.secret()

        self.__coin = coin.value

    def list_system_messages(self, **kwargs):
        """Get the list of warnings, infos and error messages.

        Keyword arguments:
            level -- could be 'INFO', 'WARNING' or 'ERROR' (optional)
        """
        self.__params = params(Method.SYS_MSG.value, **kwargs)
        return self.__execute()

    def get_account_info(self):
        """Get user's account balance and withdrawal limits."""
        self.__params = params(Method.ACCOUNT_INFO.value)
        return self.__execute()

    def get_order(self, order_id):
        """Get an order information, according to the order id.

        Keyword arguments:
            order_id -- order id
        """
        self.__params = params(Method.GET_ORDER.value,
                               coin_pair=self.__coin,
                               order_id=order_id)

        return self.__execute()

    def list_orders(self, **kwargs):
        """Get a list of orders' information.

        Keyword arguments (optional):
            order_type -- (1)buy or (2)sell

            status_list -- (2)open, (3)cancelled or (4)filled.
            Ex.: [2,3] or [2]

            has_fills -- true or false

            from_id -- get orders FROM some id

            to_id -- get orders UP TO some id

            from_timestamp -- get orders FROM some timestamp

            to_timestamp -- get orders UP TO some timestamp
        """
        if 'status_list' in kwargs:
            kwargs['status_list'] = json.dumps(kwargs['status_list'])

        kwargs['coin_pair'] = self.__coin
        self.__params = params(Method.ORDERS.value, **kwargs)

        return self.__execute()

    def list_orderbook(self, **kwargs):
        """Get information about bids and asks at Mercado Bitcoin.

        Keyword arguments (optional):
            full -- default False
                True: 500 bids, 500 asks
                False: 20 bids, 20 asks
        """
        kwargs['coin_pair'] = self.__coin
        self.__params = params(Method.LIST_ORDERBOOK.value, **kwargs)

        return self.__execute()

    def place_buy_order(self, quantity, limit):
        """Place a buy order at Mercado Bitcoin's orderbook.

        Keyword arguments:
            quantity -- coin quantity to buy
            limit -- maximum buy value

        Ex.: buy 0.5 BTC at 25000,
        where 0.5 is the quantity and 2500 is the limit.
        """
        self.__params = params(Method.BUY.value,
                               coin_pair=self.__coin,
                               quantity=quantity,
                               limit_price=limit)

        return self.__execute()

    def place_sell_order(self, quantity, limit):
        """Place a sell order at Mercado Bitcoin's orderbook.

        Keyword arguments:
            quantity -- coin quantity to sell
            limit -- minimum sell value

        Ex.: sell 0.5 BTC at 25000,
        where 0.5 is the quantity and 2500 is the limit.
        """
        self.__params = params(Method.SELL.value,
                               coin_pair=self.__coin,
                               quantity=quantity,
                               limit_price=limit)

        return self.__execute()

    def cancel_order(self, order_id):
        """Cancel an order that has been placed.

        Keyword arguments:
            order_id -- order's id to be cancelled
        """
        self.__params = params(Method.CANCEL.value,
                               coin_pair=self.__coin,
                               order_id=order_id)

        return self.__execute()

    def get_withdrawal(self, coin, withdrawal_id):
        """Get information about a withdrawal request.

        Keyword arguments:
            coin -- withdrawal's coin
                BRL: Real
                BTC: Bitcoin
                LTC: Litecoin
                BCH: BCash

            withdrawal_id -- withdrawal's id
        """
        self.__params = params(Method.WITHDRAWAL.value,
                               coin=coin,
                               withdrawal_id=withdrawal_id)

        return self.__execute()

    def withdraw_coin(self, coin, **kwargs):
        """Get information about a withdrawal request.

        Keyword arguments:
            coin -- withdrawal's coin
                BRL: Real
                BTC: Bitcoin
                LTC: Litecoin
                BCH: BCash

            description(optional) -- withdrawal description

        To know more abotu additional parameters, see:
        https://www.mercadobitcoin.com.br/trade-api/#withdraw_coin
        """
        kwargs['coin'] = coin
        self.__params = params(Method.WITHDRAW.value, **kwargs)

        return self.__execute()

    def __mac(self):
        """Generate a MAC using the secret key."""
        mac = hmac.new(self.__secret, digestmod=hashlib.sha512)

        params = urllib.parse.urlencode(self.__params)
        params = Url.TAPI_PATH.value + '?' + params

        mac.update(params.encode('utf-8'))

        return mac.hexdigest()

    def __header(self):
        """Construct the request's header."""
        return {
            'Content-type': 'application/x-www-form-urlencoded',
            'TAPI-ID': self.__id,
            'TAPI-MAC': self.__mac()
        }

    def __execute(self):
        request = requests.post(Url.TAPI.value,
                                data=self.__params,
                                headers=self.__header())

        data = request.content.decode('utf-8')
        data = json.loads(data)

        request.close()

        return Response(data)


def params(method, **kwargs):
    """Represent a set of parameters for a Trade request.

    Keyword arguments:
        method -- TAPI method name

    Other arguments are optional.
    """
    parameters = kwargs

    # Random (but incremental) number for request.
    nonce = str(int(time.time()) - randint(1, 29))

    # Dict with params fulfill.
    parameters['tapi_nonce'] = nonce
    parameters['tapi_method'] = method

    return parameters
