#!/usr/bin/env python3

# 2022 @j4imefoo

import json


class Bisq:
    
    def getOffers(fiat, direction, refprice, session):

        # fiat = eur, usd, 
        # direction = buy or sell
        # refprice = int
        # tor = 1 or 0

        bisqBaseUrlTor = 'http://bisqmktwih46lbda65e27uefnn2nznnk5oygdwyqcdrpo7yy7i5qd7ad.onion'

        bisqApi = f"{bisqBaseUrlTor}/api/offers?market=btc_{fiat.upper()}&direction={direction.upper()}"
        try:
            f = session.get(bisqApi)
        except IOError:
            print("Please, make sure you are running TOR!")
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

    def getFiatPrice(fiat, session):
        bisqApi = 'http://ro7nv73awqs3ga2qtqeqawrjpbxwarsazznszvr6whv7tes5ehffopid.onion/getAllMarketPrices'

        f = session.get(bisqApi)
        priceapi = f.json()
        f.close()
        for currency in priceapi['data']:
            if (currency['currencyCode'].lower()==fiat):
                return int(float(currency['price']))

