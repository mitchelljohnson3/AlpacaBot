import alpaca_trade_api as alpaca
import requests, json
from config import *

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return r.content

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    
    return json.loads(r.content)

def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)
    
    return json.loads(r.content)

# response = create_order("MSFT", 1000, "buy", "market", "gtc")
response = get_orders()
print(response)