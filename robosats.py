#!/usr/bin/env python3

# 2022 @j4imefoo

import json

currencies = {
    "1": "USD", "2": "EUR", "3": "JPY", "4": "GBP", "5": "AUD", "6": "CAD", "7": "CHF",
    "8": "CNY", "9": "HKD", "10": "NZD", "11": "SEK", "12": "KRW", "13": "SGD", "14": "NOK",
    "15": "MXN", "16": "KRW", "17": "RUB", "18": "ZAR", "19": "TRY", "20": "BRL", "21": "CLP",
    "22": "CZK", "23": "DKK", "24": "HRK", "25": "HUF", "26": "INR", "27": "ISK", "28": "PLN",
    "29": "RON", "30": "ARS", "31": "VES", "32": "COP", "33": "PEN", "34": "UYU", "35": "PYG",
    "36": "BOB", "37": "IDR", "38": "ANG", "39": "CRC", "40": "CUP", "41": "DOP", "42": "GHS",
    "43": "GTQ", "44": "ILS", "45": "JMD", "46": "KES", "47": "KZT", "48": "MYR", "49": "NAD",
    "50": "NGN", "51": "AZN", "52": "PAB", "53": "PHP", "54": "PKR", "55": "QAR", "56": "SAR",
    "57": "THB", "58": "TTD", "59": "VND", "60": "XOF", "61": "TWD", "300": "XAU", "1000": "BTC"
}


class Robosats:
    def getOffers(fiat, direction, session):

        robosatsTorAddresses = [
            'http://ngdk7ocdzmz5kzsysa3om6du7ycj2evxp2f2olfkyq37htx3gllwp2yd.onion',
            'http://mmhaqzuirth5rx7gl24d4773lknltjhik57k7ahec5iefktezv4b3uid.onion',
            'http://4t4jxmivv6uqej6xzx2jx3fxh75gtt65v3szjoqmc4ugdlhipzdat6yd.onion',
            'http://otmoonrndnrddqdlhu6b36heunmbyw3cgvadqo2oqeau3656wfv7fwad.onion'
        ]

        key_list = list(currencies.keys())
        val_list = list(currencies.values())
        position = val_list.index(fiat.upper())
        currency = key_list[position]

        if (direction == "sell"):
            typeoffer = 1
        else:
            typeoffer = 0
        command = f'/api/book/?currency={currency}&type={typeoffer}'

        alloffers = []

        for robosatsTor in robosatsTorAddresses:
            try:
                f = session.get(robosatsTor + command)
                values = f.json()
                f.close()
            except IOError:
                print(
                    f"Failed to connect to {robosatsTor}. Please, make sure you are running TOR!")
                continue

            for line in values:
                if line == "not_found":
                    break
                offer = {}
                offer['exchange'] = 'Robosats'
                offer['price'] = int(float(line['price']))
                offer['dif'] = float(line['premium'])
                if line['amount'] is not None:
                    offer['min_amount'] = int(float(line['amount']))
                    offer['max_amount'] = int(float(line['amount']))
                else:
                    offer['min_amount'] = int(float(line['min_amount']))
                    offer['max_amount'] = int(float(line['max_amount']))
                offer['min_btc'] = offer['min_amount'] / offer['price']
                offer['max_btc'] = offer['max_amount'] / offer['price']
                offer['method'] = line['payment_method']
                alloffers.append(offer)

        alloffers.sort(key=lambda item: item.get('price'))

        return alloffers
