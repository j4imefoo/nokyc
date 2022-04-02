#!/usr/bin/env python3
import argparse
from bisq import Bisq
from fiat import Fiat
# Parsing arguments
parser = argparse.ArgumentParser(description="A script that lists all current Bisq offers in the terminal")

parser.add_argument(
    "-t",
    "--type",
    help="Type of orders (buy or sell)",
    type=str,
    choices=['buy', 'sell'],
    default='sell',
)

parser.add_argument(
    "-f",
    "--fiat",
    help="Fiat currency",
    type=str,
    choices = ['eur', 'usd', 'gbp', 'cad', 'aud', 'chf', 'brl', 'czk', 'sek', 'nzd', 'dkk', 'pln'],
    default='eur',
)

parser.add_argument(
    "-d",
    "--deviation",
    help="Max deviation from market price",
    type=int,
    default=8,
)
parser.add_argument(
        "--tor",
        help="Use TOR",
        action='store_true',
        default=False
)
args = parser.parse_args()

fiat = args.fiat
direction = args.type
LIMIT = args.deviation
tor = args.tor

# Payment methods to avoid
avoid_methods = ["F2F", "CASH_DEPOSIT", "ADVANCED_CASH", "HAL_CASH", "UPHOLD", "CASH_BY_MAIL"]

price_exch = Fiat.getfiatprice(fiat)

bisqOffers = Bisq.getOffers(fiat, direction, price_exch, tor)

print(f"Price: {price_exch} {fiat.upper()}\n")
if (direction=="sell"):
    print("BTC sell offers:\n")
else:
    print("BTC buy offers:\n")

print(f"{'Exchange':8} {'Price':12} {'Dif':6} {'BTC min':8} {'BTC max':9} {'Min':6} {'Max':5} {'Method'}") 
for offer in bisqOffers:
        if ((direction=="sell" and offer['dif']<LIMIT) or (direction=="buy" and offer['dif']>-LIMIT)) and offer['method'] not in avoid_methods:
            print(f"{offer['exchange']:8}{offer['price']:8n} {fiat.upper():4} {offer['dif']:4.1f}% {offer['min_btc']:8.4f} {offer['max_btc']:8.4f} {offer['min_amount']:7n} {offer['max_amount']:7n} {offer['method']}")
