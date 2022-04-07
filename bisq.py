#!/usr/bin/env python3

# 2022 @j4imefoo

import json


class Bisq:
    
    def getOffers(fiat, direction, refprice, session):

        # fiat = eur, usd, 
        # direction = buy or sell
        # refprice = int
        # tor = 1 or 0

        bisqBaseUrlTor = 'http://bisqmktse2cabavbr2xjq7xw3h6g5ottemo5rolfcwt6aly6tp5fdryd.onion'

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
        bisqApi = 'http://wizpriceje6q5tdrxkyiazsgu7irquiqjy2dptezqhrtu7l2qelqktid.onion/getAllMarketPrices'

        f = session.get(bisqApi)
        priceapi = f.json()
        f.close()
        for currency in priceapi['data']:
            if (currency['currencyCode'].lower()==fiat):
                return int(float(currency['price']))

