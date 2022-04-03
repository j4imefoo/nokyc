# nokyc 
A script that lists all current [Bisq](https://bisq.network), [HodlHodl](https://hodlhodl.com) and [Robosats](https://unsafe.robosats.com) offers in the terminal


# Usage
```
nokyc.py [-h] [-t {buy,sell}] [-f {eur,usd,gbp,cad,aud,chf,brl,czk,sek,nzd,dkk,pln}] [-d DEVIATION]

A script that lists all current Bisq, HodlHodl and Robosats offers in the terminal

optional arguments:
  -h, --help            show this help message and exit
  -t {buy,sell}, --type {buy,sell}
                        Type of orders (buy or sell)
  -f {eur,usd,gbp,cad,aud,chf,brl,czk,sek,nzd,dkk,pln}, --fiat {eur,usd,gbp,cad,aud,chf,brl,czk,sek,nzd,dkk,pln}
                        Fiat currency
  -d DEVIATION, --deviation DEVIATION
                        Max deviation from market price

```

# Configuration

We can modify the following parameters in our script nokyc.py:

- `TOR_PORT`: local tor port. 9050 in case of tor daemon or 9150 for Tor browser
- `avoid_methods`: payment methods to hide in order to get a cleaner output. In small caps


# Example output
```
$ nokyc -f eur -t sell -d 8

Price: 42037 EUR

BTC sell offers:

Exchange Price        Dif    BTC min  BTC max   Min    Max   Method
Bisq       42039 EUR   0.0%   0.2500   0.2500   10509   10509 SEPA
Bisq       42039 EUR   0.0%   0.1500   0.1500    6305    6305 REVOLUT
HodlHodl   42280 EUR   0.6%   0.0071   0.0142     300     600 Hal-cash
Bisq       42459 EUR   1.0%   0.1000   0.1000    4245    4245 SEPA
Bisq       42880 EUR   2.0%   0.0250   0.0250    1072    1072 F2F
HodlHodl   43042 EUR   2.4%   0.0023   0.0081     100     350 AdvCash
Bisq       43090 EUR   2.5%   0.1000   0.1000    4309    4309 REVOLUT
Bisq       43090 EUR   2.5%   0.0190   0.0215     818     926 F2F
HodlHodl   43238 EUR   2.9%   0.0104   0.2313     450   10000 TransferWise
HodlHodl   44129 EUR   5.0%   0.0045   0.0113     200     500 HalCash
Bisq       44141 EUR   5.0%   0.0250   0.3000    1103   13242 F2F
Bisq       44267 EUR   5.3%   0.0100   0.0100     442     442 REVOLUT
Robosats   44531 EUR   6.0%   0.0016   0.0056      70     250 Revolut

```

# Possible use cases
One can use this script to check on current offers and decide if connecting to Bisq, HodlHodl or Robosats in order to buy or sell bitcoin. Take into account that it is possible to run this script wherever we have Python installed, including an Android phone using Termux.

It is very easy to automate it and, eg., get an SMS notification once the script finds a quotation we might be interested in. 

# More information
https://twitter.com/j4imefoo

If you want to buy me a beer:

- https://paynym.is/+luckywood116
- https://tippin.me/@j4imefoo
