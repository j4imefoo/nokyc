#!/usr/bin/env python3
from urllib.request import urlopen
import json
import sys
import argparse

def main():
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
        choices=["EUR", "USD", "CHF", "GBP", "AUD", "CAD", "BRL"],
        default="EUR",
    )

    parser.add_argument(
        "-d",
        "--deviation",
        help="Max deviation from market price",
        type=int,
        default=8,
    )

    parser.add_argument(
        "-m",
        "--method",
        help="Payment Method",
        nargs="*"
    )

    args = parser.parse_args()

    fiat = args.fiat
    direction = args.type
    LIMIT = args.deviation
    paymentMethods = args.method

    krakenApi = "https://api.kraken.com/0/public/Ticker?pair=XBT" + fiat
    brasilbtcApi = "https://brasilbitcoin.com.br/API/prices/BTC"
    bisqApi = "https://bisq.markets/api/offers?market=btc_" + fiat.lower() + "&direction="


    kraken = jsonget(krakenApi)
    if (fiat == "BRL"):
        brasilbtc = jsonget(brasilbtcApi)
        price_exch = int(float(brasilbtc['last']))
    else:
        kraken = jsonget(krakenApi)
        if (fiat == "CHF" or fiat == "AUD"):
            key = 'XBT' + fiat
        else:
            key = 'XXBTZ' + fiat
    price_exch = int(float(kraken['result'][key]['c'][0]))

    values = jsonget(bisqApi + direction)
    print(f"Price: {price_exch} {fiat}\n")
    if (direction=="SELL"):
        print("BTC sell offers:\n")
    else:
        print("BTC buy offers:\n")

    print(f"{'Price':14} {'Dif':6} {'BTC min':7} {'BTC max':10} {'Min':6} {'Max':7} {'Method':8}")
    key ='btc_' + fiat.lower()
    filteredOffers = filterOffers(values[key][direction.lower() + 's'], direction, price_exch, LIMIT, paymentMethods)
    for line in filteredOffers:
            price = int(float(line['price']))
            var = (price/price_exch-1)*100
            min_btc = float(line['min_amount'])
            max_btc = float(line['amount'])
            min_amount = min_btc * price
            max_amount = float(line['volume'])
            method = line['payment_method']
            print(f"{price:8n} {fiat:4} {var:4.1f}% {min_btc:8.4f} {max_btc:8.4f} {min_amount:8n} {max_amount:8n} {method}")

def jsonget(url):
    f = urlopen(url)
    jsonweb = json.load(f)
    f.close()
    return jsonweb

def filterOffers(offers, direction, indexPrice, priceDeviationLimit, methods=[],
                 avoidMethods=["F2F", "CASH_DEPOSIT", "ADVANCED_CASH", "HAL_CASH", "UPHOLD"]):
    filteredOfferes = []
    for offer in offers:
        price = int(float(offer['price']))
        var = (price / indexPrice - 1) * 100
        if (direction.upper() == "SELL" and var > priceDeviationLimit) or (direction.upper() == "BUY" and var < -priceDeviationLimit):
            continue
        if offer['payment_method'] in avoidMethods:
            continue
        if methods is not None and offer['payment_method'] not in methods:
            continue
        filteredOfferes.append(offer)
    return filteredOfferes

if __name__ == "__main__":
    main()

