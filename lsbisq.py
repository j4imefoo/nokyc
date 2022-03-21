#!/usr/bin/env python3
from urllib.request import urlopen
import json
import sys

# EUR, USD, CHF, GBP
fiat="EUR"

# Max deviation from market price
LIMIT = 8

# Payment methods to avoid
avoid_methods = ["F2F", "CASH_DEPOSIT", "ADVANCED_CASH", "HAL_CASH", "UPHOLD"]


direction="SELL"

krakenApi = "https://api.kraken.com/0/public/Ticker?pair=XBT" + fiat
bitstampApi = "https://www.bitstamp.net/api/v2/ticker/btc" + fiat.lower()
bisqApi = "https://bisq.markets/api/offers?market=btc_" + fiat.lower() + "&direction="

def jsonget(url):
    f = urlopen(url)
    jsonweb = json.load(f)
    f.close()
    return jsonweb

if (len(sys.argv)>1 and sys.argv[1]=="-r"):
    direction="BUY"

kraken = jsonget(krakenApi)
if (fiat=="CHF"):
    key = 'XBTCHF'
else:
    key ='XXBTZ' + fiat
price_kraken = int(float(kraken['result'][key]['c'][0]))

values = jsonget(bisqApi + direction)
print(f"Price: {price_kraken} {fiat}\n")
if (direction=="SELL"):
    print("BTC sell offers:\n")
else:
    print("BTC buy offers:\n")

print(f"{'Price':14} {'Dif':6} {'BTC min':7} {'BTC max':10} {'Min':6} {'Max':7} {'Method':8}") 
key ='btc_' + fiat.lower()
for line in values[key][direction.lower() + 's' ]:
        price = int(float(line['price']))
        var = (price/price_kraken-1)*100
        min_btc = float(line['min_amount'])
        max_btc = float(line['amount'])
        min_amount = min_btc * price
        max_amount = float(line['volume'])
        method = line['payment_method']
        if ((direction=="SELL" and var<LIMIT) or (direction=="BUY" and var>-LIMIT)) and method not in avoid_methods:
            print(f"{price:8n} {fiat:4} {var:4.1f}% {min_btc:8.4f} {max_btc:8.4f} {min_amount:8n} {max_amount:8n} {method}")
