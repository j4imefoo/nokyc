#!/usr/bin/env python3

import json
import requests

def get_tor_session():
    TOR_PORT = '9050'
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:' + TOR_PORT,
                       'https': 'socks5h://127.0.0.1:' + TOR_PORT}
    return session

class Bisq:
    
    def getOffers(fiat, direction, refprice, tor):

        # fiat = eur, usd, 
        # direction = buy or sell
        # refprice = int
        # tor = 1 or 0

        bisqBaseUrl = 'https://bisq.markets'
        bisqBaseUrlTor = 'http://bisqmktse2cabavbr2xjq7xw3h6g5ottemo5rolfcwt6aly6tp5fdryd.onion'

        if tor:
            session = get_tor_session()
            bisqApi = f"{bisqBaseUrlTor}/api/offers?market=btc_{fiat.upper()}&direction={direction.upper()}"
            try:
                f = session.get(bisqApi)
            except IOError:
                print("Please, make sure you are running TOR!")
                exit(1)

        else:
            bisqApi = f"{bisqBaseUrl}/api/offers?market=btc_{fiat.upper()}&direction={direction.upper()}"
            try:
                f = requests.get(bisqApi)
            except IOError:
                print("Error connecting to Bisq API.")
                exit(1)

        values = f.json()
        f.close()
    
        key = f"btc_{fiat}"
        
        alloffers = []

        for line in values[key][direction + 's' ]:
            offer = {}
            offer['exchange'] = 'Bisq'
            offer['price'] = int(float(line['price']))
            offer['dif'] = (offer['price']/refprice-1)*100
            offer['min_btc'] = float(line['min_amount'])
            offer['max_btc'] = float(line['amount'])
            offer['min_amount'] = int(offer['min_btc'] * offer['price'])
            offer['max_amount'] = int(float(line['volume']))
            offer['method'] = line['payment_method']
            alloffers.append(offer)
        alloffers.sort(key=lambda item: item.get('price'))
        return alloffers
