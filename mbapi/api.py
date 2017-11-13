"""Mercado Bitcoin's Data API."""


import json
import requests
from labels import Url, Method, Coin


class Request():
    """Implement Data API methods.

    Methods:
        ticker
        orderbook
        trades

    See method.__doc__ for method's description.
    """

    def __init__(self, coin=Coin.BTC):
        """Get value from Coin Enum's object."""
        self.__api = Url.API.value  # base API url
        self.__coin = coin.value    # coin label

    def url(self, method, params=[]):
        """Construct a full API url and return it as a string.

        Keyword argument:
            method -- method object
                - options: {Method.TICKER, Method.ORDERBOOK, Method.TRADES}
            params -- get parameters (default [])
        """
        # Group params
        parameters = map(lambda x: str(x), params)
        parameters = '/'.join(parameters)

        # Group url parts
        return '/'.join([self.__api, self.__coin, method.value, parameters])

    def get(self, url, params=None):
        """Make a GET request using the URL and return the response content as dict.

        Keyword argument:
            url -- URL to be used in the request
            params -- parameters for GET request (default None)
        """
        # Make the request
        response = requests.get(url, params=params)

        # Decode response content
        data = response.content.decode('utf-8')

        # Return a dictionary with response content
        return json.loads(data)

    def ticker(self):
        """Get request using TICKER method and return a Ticker object."""
        # Get url
        url = self.url(Method.TICKER)

        # Get request response
        response = self.get(url)

        # Return a Ticker object
        return Ticker(**response['ticker'])

    def orderbook(self):
        """Get request using ORDERBOOK method and return a Orderbook object."""
        # Get url
        url = self.url(Method.ORDERBOOK)

        # Get request response
        response = self.get(url)

        # Return a Ticker object
        return Orderbook(**response)

    def trades(self, *args, **kwargs):
        """Get data using TRADES method and return a list of Trade objects.

        Keyword arguments:
            from -- from, datetime in Unix Era (default None)
            to -- datetime in Unix Era (default None)

        Positional argument:
            tid -- trade id

        For more information:
        https://www.mercadobitcoin.com.br/api-doc/#method_trade_api_dado
        """
        # Get url
        url = self.url(Method.TRADES, args)

        # Get request response
        response = self.get(url, kwargs)

        # Return a Ticker object
        return [Trade(**trade) for trade in response]


class Ticker():
    """Represent a TICKER information.

    Properties:
        high -- highest negociation price in the last 24 hours
        low -- lowest negociation price in the last 24 hours
        vol -- negociated volume in the last 24 hours
        last -- last negociated price
        buy -- highest buy price in the last 24 hours
        sell -- highest sell price in the last 24 hours
        date -- datetime in Unix Era
    """

    def __init__(self, **kwargs):
        """Set properties."""
        # Properties' types
        types = [float, float, float, float, float, float, int]

        # For each property's name and value...
        for cast_to, prop in zip(types, kwargs):
            # Set property
            exec("self.{} = cast_to(kwargs[prop])".format(prop))


class Orderbook():
    """Represent a ORDERBOOK information.

    Properties:
        asks -- list of sell orders sorted in ascending order
        bids -- list of buy orders sorted in descending order

    The lists are structure as [<price>, <quantity>].
    """

    def __init__(self, **kwargs):
        """Set properties."""
        # For each property's name and value...
        for prop, value in kwargs.items():
            # Set property
            exec("self.{} = list(value)".format(prop))


class Trade():
    """Represent a TRADE information.

    Properties:
        date -- datetime in Unix Era
        price -- unit price
        amount -- quantity
        tid -- trade id
        type -- 'buy' or 'sell'
    """

    def __init__(self, **kwargs):
        """Set properties."""
        # Properties' types
        types = [int, float, float, int, str]

        # For each property's name and value...
        for cast_to, prop in zip(types, kwargs):
            # Set property
            exec("self.{} = cast_to(kwargs[prop])".format(prop))
