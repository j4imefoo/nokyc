#!/usr/bin/env python3
from urllib.request import urlopen
import json
import sys
import argparse

# Parsing arguments
parser = argparse.ArgumentParser(description="A script that lists all current Bisq offers in the terminal")

parser.add_argument(
    "-t",
    "--type",
    help="Type of orders (BUY or SELL)",
    type=str,
    choices=["BUY", "SELL"],
    default="SELL",
)

parser.add_argument(
    "-f",
    "--fiat",
    help="Fiat currency",
    type=str,
    choices=["EUR", "USD", "CHF", "GBP", "AUD"],
    default="EUR",
)

parser.add_argument(
    "-d",
    "--deviation",
    help="Max deviation from market price",
    type=int,
    default=8,
)

args = parser.parse_args()

fiat = args.fiat
direction = args.type
LIMIT = args.deviation

# Payment methods to avoid
avoid_methods = ["F2F", "CASH_DEPOSIT", "ADVANCED_CASH", "HAL_CASH", "UPHOLD"]

krakenApi = "https://api.kraken.com/0/public/Ticker?pair=XBT" + fiat
bisqApi = "https://bisq.markets/api/offers?market=btc_" + fiat.lower() + "&direction="

def jsonget(url):
    f = urlopen(url)
    jsonweb = json.load(f)
    f.close()
    return jsonweb

kraken = jsonget(krakenApi)
if (fiat=="CHF" or fiat=="AUD"):
    key = 'XBT' + fiat
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
