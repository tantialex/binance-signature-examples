import hmac
import time
import hashlib
import requests
import json
from urllib.parse import urlencode

""" This is a very simple script working on Binance API

- work with USER_DATA endpoint with no third party dependency
- work with testnet

Provide the API key and secret, and it's ready to go

```python

python futures.py

```

"""

KEY = ''
SECRET = ''
# BASE_URL = 'https://fapi.binance.com' # production base url
BASE_URL = 'https://testnet.binancefuture.com' # testnet base url

def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_timestamp():
    return int(time.time() * 1000)


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': KEY
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')

def send_request(http_method, url_path, payload={}):
    query_string = urlencode(payload)
    # replace single quote to double quote
    query_string = query_string.replace('%27', '%22')
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' + hashing(query_string)
    print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method)(**params)
    return response.json()

# get account informtion
# if you can see the account details, then the API key/secret is correct
response = send_request('GET', '/fapi/v2/account')
print(response)


# place an order
# if you see order response, then the parameters setting is correct
# if it has response from server saying some parameter error, please adjust the parameters according the market.
params = {
    "symbol": "BNBUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 1,
    "price": "15"
}
response = send_request('POST', '/fapi/v1/order', params)
print(response)


# place batch orders
# if you see order response, then the parameters setting is correct
# if it has response from server saying some parameter error, please adjust the parameters according the market.
params = {
    "batchOrders": [
        {
            "symbol":"BNBUSDT",
            "side": "BUY",
            "type": "STOP",
            "quantity": "1",
            "price": "9000",
            "timeInForce": "GTC",
            "stopPrice": "9100"
        },
        {
            "symbol":"BNBUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "quantity": "1",
            "price": "15",
            "timeInForce": "GTC"
        },
    ]
}
response = send_request('POST', '/fapi/v1/batchOrders', params)
print(response)
