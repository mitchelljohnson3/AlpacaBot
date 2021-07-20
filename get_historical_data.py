import alpaca_trade_api as alpaca
import requests, json
from config import *

SYMBOL = "AAPL"
BARS_URL = '{}/v2/stocks/{}/bars'.format(DATA_URL, SYMBOL)
parameters = {
    'start': '2020-01-01T17:30:00+00:00',
    'end': '2021-01-01T00:00:00+00:00',
    'page_token': '',
    'timeframe': '1Day'
}
r = requests.get(BARS_URL, params=parameters, headers=HEADERS)
response = json.loads(r.content)
data = json.dumps(response, indent=4)
print(data)