# lsbisq
A script that lists all current Bisq offers in the terminal

[Bisq](https://bisq.network) is a decentralized bitcoin exchange that allows us to buy or sell bitcoin peer-to-peer. 

This script shows all current buy or sell offers in the Bisq network in our preferred fiat currency. 

# Parameters
We can indicate the following paramenters in our script header:
- `avoid_methods`: payment methods to hide in order to get a cleaner output

# Usage
`python3 lsbisq.py -t <type_of_order> -f <fiat> -d <max_deviation>`

Where:
- `<type_of_order>`: (string) BUY or SELL (example: `-t BUY`). Default value is `BUY`
- `<fiat>`: (string) Currency we want to exchange for bitcoin (example:`-f EUR`). Default value is `EUR`
- `<limit>`: (integer) Max deviation (in percentage) from market price (example: `-d 8`). Default value is 8 %


# Example output
```
$ lsbisq.py

Price: 37235 EUR

BTC sell offers:

Price          Dif    BTC min BTC max    Min    Max     Method  
   36854 EUR  -1.0%   0.0010   0.0010   36.854  36.8545 SEPA
   37226 EUR  -0.0%   0.0140   0.0140  521.164  521.175 SEPA_INSTANT
   37971 EUR   2.0%   0.1000   0.1000   3797.1  3797.13 REVOLUT
   38343 EUR   3.0%   0.1000   0.1000   3834.3  3834.36 SEPA
   38343 EUR   3.0%   0.0100   0.0100   383.43  383.436 SEPA
   38511 EUR   3.4%   0.0280   0.0712  1078.31  2741.99 SEPA
   38712 EUR   4.0%   0.0207   0.0207  801.338  801.341 REVOLUT
```

# Possible use cases
One can use this script to check on current offers and decide if starting the Bisq program in order to buy or sell bitcoin. Take into account that it is possible to run this script wherever we have Python installed, including an Android phone using Termux.

It is very easy to automate it and, eg., get an SMS notification once the script finds a quotation we might be interested in. 

# More information
https://twitter.com/j4imefoo

If you want to buy me a beer:

- https://paynym.is/+luckywood116
- https://tippin.me/@j4imefoo
