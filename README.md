# Mercado Bitcoin's API Interface
A Python 3 API interface for Mercado Bitcoin's API.

`mbapi` implements all methods from Mercado Bitcoin's Data API (a.k.a. API) and Trade API (a.k.a. TAPI).
To know more about method parameters you can see the methods and classes documentation `<method>.__doc__` or
access the [API documentation](https://www.mercadobitcoin.com.br/api-doc/) and [TAPI documentation](https://www.mercadobitcoin.com.br/trade-api/).

## Instalation
```bash
sudo pip3 install mbapi
```

## Usage
### API
```python
from mbapi.api import Request
from mbapi.labels import Coin

# Requests for BTC
request = Request()

ticker = request.ticker()
orderbook = request.orderbook()

# Requests for LTC
request = Request(Coin.LTC)

ticker = request.ticker()
orderbook = request.orderbook()
```

### TAPI
```python
from mbapi.tapi import Auth, Trade

auth = Auth(id=<tapi_user_id>,
            pin=<user_pin_number>,
            secret=<user_secret_key>)

# Trade method for BTC
trade = Trade(auth)

response = trade.place_buy_order(1, 23905)  # place a buy order

trade.cancel_order(response.data['order']['order_id'])  # cancel the buy order
```

## Troubleshoot
While developing, I got a UnicodeEncodeError. You could get too. To fix it, add the following lines to your `~/.bash_profile`.
```bash
export LANGUAGE=cs_CZ.UTF-8
export LC_ALL=cs_CZ.UTF-8
```

## Note
This is a project in development. So, I apologize for the poor documentation.
In case of doubts, feel free to e-mail me: trevizanbernardo@gmail.com
