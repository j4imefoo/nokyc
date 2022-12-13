#!/usr/bin/env python3

# 2022 @j4imefoo 

import argparse
import configparser
import itertools
import requests
import sys
import signal
import threading
import time
import json

from bisq import Bisq
from robosats import Robosats
from hodlhodl import HodlHodl


# Import user configuration from nokycconfig.ini file
config = configparser.ConfigParser()
config.read('nokycconfig.ini')

def get_tor_session():
     session = requests.session()
     session.proxies = {'http':  'socks5h://127.0.0.1:' + config['DEFAULT']['TOR_PORT'],
                        'https': 'socks5h://127.0.0.1:' + config['DEFAULT']['TOR_PORT']}
     return session

def sigint_handler(signal, frame):
    print ('Cancelled.')
    sys.exit(0)

# Define a simple "loading" animation while we gather offers
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rGathering offers... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def get_user_arguments():
    parser = argparse.ArgumentParser(description="A script that lists all current Bisq, HodlHodl and Robosats offers in the terminal")

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
    args = parser.parse_args()
    fiat = args.fiat
    direction = args.type
    limit = args.deviation
    return fiat, direction, limit
    
if __name__ == "__main__":
    # Display a simple loading animation
    # Put the animation in a thread so the rest of the function can proceed
    done = False
    t = threading.Thread(target=animate)
    # Allow a user to exit out of the script and animation cleanly
    t.daemon=True
    t.start()

    signal.signal(signal.SIGINT, sigint_handler)
    fiat, direction, limit = get_user_arguments()
    session = get_tor_session()

    price_exch = Bisq.getFiatPrice(fiat, session)

    bisqOffers = Bisq.getOffers(fiat, direction, price_exch, session)
    robosatsOffers = Robosats.getOffers(fiat, direction, session)
    hodlhodlOffers = HodlHodl.getOffers(fiat, direction, price_exch, session)

    allOffers = bisqOffers + robosatsOffers + hodlhodlOffers
    if (direction=='sell'):
        allOffers.sort(key=lambda item: item.get('price'))
    else:
        allOffers.sort(key=lambda item: item.get('price'), reverse=True)

    # Stop the loading animation
    done = True

    print('\r                      ', end = '')
    print(f"\rPrice: {price_exch} {fiat.upper()}\n")
    
    print(f"BTC {direction} offers:\n")

    print(f"{'Exchange':8} {'Price':12} {'Dif':6} {'BTC min':8} {'BTC max':9} {'Min':6} {'Max':5} {'Method'}") 

    for offer in allOffers:
        if ((direction=="sell" and offer['dif']<limit) or (direction=="buy" and offer['dif']>-limit)) and offer['method'].lower() not in config['DEFAULT']['avoid_methods']:
            print(f"{offer['exchange']:8}{offer['price']:8n} {fiat.upper():4} {offer['dif']:4.1f}% {offer['min_btc']:8.4f} {offer['max_btc']:8.4f} {offer['min_amount']:7n} {offer['max_amount']:7n} {offer['method']}")
