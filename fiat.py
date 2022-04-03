#!/usr/bin/env python3

import json

def getcgprice(fiat, session):
    coingeckoApi = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency='

    f = session.get(coingeckoApi + fiat + '&ids=bitcoin')
    priceapi = f.json()
    f.close()
    price = priceapi[0]['current_price']
    return price

def getkprice(fiat, session):
    krakenApi = 'https://api.kraken.com/0/public/Ticker?pair=XBT'

    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36'})
    f = session.get(krakenApi + fiat.upper())
    priceapi = f.json()
    f.close()

    if fiat in ['eur', 'usd', 'gbp', 'cad']:
        key = 'XXBTZ' + fiat.upper()
    else:
        key = 'XBT' + fiat.upper()
    price = int(float(priceapi['result'][key]['c'][0]))
    return price

class Fiat:
    def getfiatprice(fiat, session):
        fiat_kraken = ['eur', 'usd', 'gbp', 'cad', 'aud', 'chf']
        fiat_coingecko = ['brl', 'czk', 'sek', 'nzd', 'dkk', 'pln']

        if fiat in fiat_kraken:
            price = getkprice(fiat, session)
        else:
            price = getcgprice(fiat, session)

        return price
