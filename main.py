import alpaca_trade_api as alp

alpaca_endpoint = 'https://paper-api.alpaca.markets'
api = alp.REST('PKBKGUIQ0WJ6RMF2IIJ2', 'xavXrFtnn0f9vuEtji8jQ3kKsmedkCVshP20qfIp', alpaca_endpoint)

account = api.get_account()
print(account.status)